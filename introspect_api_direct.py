#!/usr/bin/env python3
"""Direct GraphQL introspection using synchronous requests."""

import os
import sys
import json
import requests

API_URL = "https://graphql.app-api.prod.aws.mybirdbuddy.com/graphql"

def authenticate():
    """Authenticate and get access token."""
    email = os.getenv("BB_USER", "")
    password = os.getenv("BB_PWD", "")

    # Remove surrounding quotes if present
    if email.startswith('"') and email.endswith('"'):
        email = email[1:-1]
    if password.startswith('"') and password.endswith('"'):
        password = password[1:-1]

    if not email or not password:
        print("❌ BB_USER and BB_PWD must be set")
        sys.exit(1)

    query = """
    mutation emailSignIn($emailSignInInput: EmailSignInInput!) {
      authEmailSignIn(emailSignInInput: $emailSignInInput) {
        ... on Auth {
          accessToken
          refreshToken
          __typename
        }
        __typename
      }
    }
    """

    variables = {
        "emailSignInInput": {
            "email": email,
            "password": password
        }
    }

    print(f"🔑 Authenticating as {email}...")

    try:
        response = requests.post(
            API_URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            print(f"❌ GraphQL errors: {data['errors']}")
            sys.exit(1)

        auth_data = data.get("data", {}).get("authEmailSignIn", {})
        token = auth_data.get("accessToken")

        if not token:
            print(f"❌ No access token in response: {json.dumps(data, indent=2)}")
            sys.exit(1)

        print("✅ Authenticated successfully!\n")
        return token

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)


def introspect_type(token, type_name):
    """Introspect a specific GraphQL type."""
    query = """
    query IntrospectType($typeName: String!) {
      __type(name: $typeName) {
        name
        kind
        description
        fields {
          name
          description
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
      }
    }
    """

    variables = {"typeName": type_name}

    print(f"{'='*70}")
    print(f"Introspecting: {type_name}")
    print(f"{'='*70}")

    try:
        response = requests.post(
            API_URL,
            json={"query": query, "variables": variables},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            print(f"❌ Errors: {data['errors']}\n")
            return None

        type_info = data.get("data", {}).get("__type")
        if not type_info:
            print(f"⚠️  Type '{type_name}' not found\n")
            return None

        # Print fields
        fields = type_info.get("fields", [])
        if fields:
            print(f"\n📋 Found {len(fields)} fields:\n")
            for field in fields:
                field_name = field["name"]
                field_type = field["type"]
                type_str = format_type(field_type)
                print(f"  • {field_name}: {type_str}")
        else:
            print(f"⚠️  No fields found (might be an enum or scalar)\n")

        print()
        return type_info

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}\n")
        return None


def format_type(type_info):
    """Format a GraphQL type for display."""
    if not type_info:
        return "Unknown"

    kind = type_info.get("kind")
    name = type_info.get("name")
    of_type = type_info.get("ofType")

    if kind == "NON_NULL":
        return f"{format_type(of_type)}!"
    elif kind == "LIST":
        return f"[{format_type(of_type)}]"
    elif name:
        return name
    elif of_type:
        return format_type(of_type)
    else:
        return "Unknown"


def introspect_enum(token, enum_name):
    """Introspect a GraphQL enum type."""
    query = """
    query IntrospectEnum($enumName: String!) {
      __type(name: $enumName) {
        name
        kind
        description
        enumValues {
          name
          description
          isDeprecated
          deprecationReason
        }
      }
    }
    """

    variables = {"enumName": enum_name}

    print(f"{'='*70}")
    print(f"Introspecting Enum: {enum_name}")
    print(f"{'='*70}")

    try:
        response = requests.post(
            API_URL,
            json={"query": query, "variables": variables},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            print(f"❌ Errors: {data['errors']}\n")
            return None

        type_info = data.get("data", {}).get("__type")
        if not type_info:
            print(f"⚠️  Enum '{enum_name}' not found\n")
            return None

        # Print enum values
        enum_values = type_info.get("enumValues", [])
        if enum_values:
            print(f"\n🔢 Found {len(enum_values)} values:\n")
            for value in enum_values:
                name = value["name"]
                deprecated = " (DEPRECATED)" if value.get("isDeprecated") else ""
                print(f"  • {name}{deprecated}")

        print()
        return type_info

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}\n")
        return None


def introspect_mutations(token):
    """Introspect all mutations to discover writable fields."""
    query = """
    query IntrospectMutations {
      __schema {
        mutationType {
          name
          fields {
            name
            description
          }
        }
      }
    }
    """

    print(f"{'='*70}")
    print(f"Introspecting Mutations (Writable Operations)")
    print(f"{'='*70}")

    try:
        response = requests.post(
            API_URL,
            json={"query": query},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            print(f"❌ Errors: {data['errors']}\n")
            return None

        mutation_type = data.get("data", {}).get("__schema", {}).get("mutationType")
        if not mutation_type:
            print(f"⚠️  No mutations found\n")
            return None

        # Print mutations
        fields = mutation_type.get("fields", [])
        if fields:
            print(f"\n🔐 Found {len(fields)} mutations:\n")

            # Group by category
            media_mutations = []
            feeder_mutations = []
            species_mutations = []
            other_mutations = []

            for field in fields:
                name = field["name"]
                if "media" in name.lower() or "sighting" in name.lower():
                    media_mutations.append(name)
                elif "feeder" in name.lower():
                    feeder_mutations.append(name)
                elif "species" in name.lower():
                    species_mutations.append(name)
                else:
                    other_mutations.append(name)

            if feeder_mutations:
                print(f"  📡 Feeder Mutations ({len(feeder_mutations)}):")
                for m in feeder_mutations:
                    print(f"     • {m}")
                print()

            if media_mutations:
                print(f"  🎥 Media/Sighting Mutations ({len(media_mutations)}):")
                for m in media_mutations:
                    print(f"     • {m}")
                print()

            if species_mutations:
                print(f"  🦅 Species Mutations ({len(species_mutations)}):")
                for m in species_mutations:
                    print(f"     • {m}")
                print()

            if other_mutations:
                print(f"  🔧 Other Mutations ({len(other_mutations)}):")
                for m in other_mutations:
                    print(f"     • {m}")
                print()

        print()
        return mutation_type

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}\n")
        return None


def main():
    """Main introspection routine."""
    print("\n" + "="*70)
    print("BIRD BUDDY API INTROSPECTION")
    print("="*70 + "\n")

    # Authenticate
    token = authenticate()

    # Introspect types we care about
    types_to_check = [
        "SpeciesBird",
        "Species",
        "FeederForPrivate",
        "FeederForOwner",
        "MediaVideo",
        "MediaImage",
        "FeedItemNewPostcard",
    ]

    results = {}
    for type_name in types_to_check:
        result = introspect_type(token, type_name)
        if result:
            results[type_name] = result

    # Check enums
    enums_to_check = [
        "MediaVideoQuality",
        "MediaState",
        "FeederHousingType",
        "FeederDeviceVersion",
    ]

    for enum_name in enums_to_check:
        enum_result = introspect_enum(token, enum_name)
        if enum_result:
            results[enum_name] = enum_result

    # Introspect mutations to discover writable fields
    mutations = introspect_mutations(token)
    if mutations:
        results["_mutations"] = mutations

    # Save results
    output_file = "api_introspection_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print("="*70)
    print(f"✅ Introspection complete!")
    print(f"📄 Results saved to: {output_file}")
    print(f"📊 Types introspected: {len(results)}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
