# PyBirdBuddy Documentation Guide

The pybirdbuddy library is now fully documented with comprehensive docstrings compatible with both pydoc and Sphinx documentation generators.

## Viewing Documentation

### Using pydoc (Built-in Python Documentation)

Pydoc is included with Python and requires no additional installation.

**View module documentation:**
```bash
python -m pydoc birdbuddy
```

**View specific class documentation:**
```bash
python -m pydoc birdbuddy.client.BirdBuddy
python -m pydoc birdbuddy.feeder.Feeder
python -m pydoc birdbuddy.feed.Feed
python -m pydoc birdbuddy.media.Media
python -m pydoc birdbuddy.birds.Species
```

**Start an interactive documentation server:**
```bash
python -m pydoc -b
```
This will open your browser with a searchable documentation interface.

### Using Sphinx (Professional Documentation)

For generating professional HTML documentation with Sphinx:

**1. Install Sphinx:**
```bash
pip install sphinx sphinx-rtd-theme
```

**2. Create Sphinx configuration (if not already present):**
```bash
cd docs  # or create a docs directory
sphinx-quickstart
```

**3. Configure `conf.py` to include your package:**
```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
    'sphinx.ext.viewcode',
]

html_theme = 'sphinx_rtd_theme'
```

**4. Generate API documentation:**
```bash
sphinx-apidoc -o docs/source birdbuddy
```

**5. Build HTML documentation:**
```bash
cd docs
make html
```

Documentation will be available in `docs/_build/html/index.html`.

## Documentation Features

### Module-Level Documentation

Each module has comprehensive documentation explaining its purpose:
- `birdbuddy` - Main package overview with usage examples
- `birdbuddy.client` - BirdBuddy API client
- `birdbuddy.feeder` - Feeder devices and metrics
- `birdbuddy.feed` - Activity feed and feed items
- `birdbuddy.media` - Media and collections
- `birdbuddy.birds` - Bird species information
- `birdbuddy.sightings` - Sighting data and recognition

### Class Documentation

All classes include:
- Detailed class descriptions
- Usage examples
- Attribute documentation
- Inheritance information

### Method Documentation

All methods document:
- Parameter types and descriptions (`:param:`, `:type:`)
- Return values (`:return:`, `:rtype:`)
- Raised exceptions (`:raises:`)
- Usage examples (code blocks)
- Important notes and warnings

### Sphinx Directives Used

The documentation uses Sphinx reStructuredText directives:
- `.. code-block:: python` - Code examples
- `.. note::` - Important information
- `.. warning::` - Warnings about restrictions or caveats
- `:param:`, `:type:`, `:return:`, `:rtype:` - Parameter/return documentation
- `:meth:`, `:class:` - Cross-references

## Quick Examples from Documentation

### Getting Started
```python
from birdbuddy import BirdBuddy

# Initialize and authenticate
bb = BirdBuddy(email="user@example.com", password="secret")
await bb.refresh()

# Access feeders
for feeder in bb.feeders.values():
    print(f"{feeder.name}: {feeder.battery.percentage}%")
```

### Working with Postcards
```python
# Get new postcards
postcards = await bb.new_postcards()
for postcard in postcards:
    print(f"Expires: {postcard.expires_at}")
    print(f"Has video: {postcard.has_video_media}")
    print(f"Images: {postcard.media_image_count}")
```

### Collections and Species
```python
# Refresh collections
collections = await bb.refresh_collections()
for coll in collections.values():
    species = coll.species
    print(f"{species.name} ({species.scientific_name})")
    print(f"Visits: {coll.total_visits}")
    if species.favorite_foods:
        print(f"Favorite foods: {', '.join(species.favorite_foods)}")
```

### Video Capabilities
```python
# Check feeder video capabilities
feeder = bb.feeders["feeder-id"]
if feeder.supports_audio:
    print(f"Audio enabled: {feeder.is_audio_enabled}")
if feeder.supports_webrtc:
    print("WebRTC streaming supported")
print(f"Video quality: {feeder.video_quality}")
```

## Interactive Python Help

You can also use Python's built-in help system:
```python
from birdbuddy import BirdBuddy
help(BirdBuddy)

from birdbuddy.feeder import Feeder
help(Feeder)
```

## Documentation Coverage

All public APIs are documented:
- ✅ Main BirdBuddy client class
- ✅ Feeder management and configuration
- ✅ Feed and feed items
- ✅ Media and collections
- ✅ Species information
- ✅ Sighting handling
- ✅ All enums (FeedNodeType, FeederState, PowerProfile, etc.)
- ✅ All properties with type hints
- ✅ All methods with parameters and returns

The documentation follows Python best practices and is compatible with all major documentation tools.
