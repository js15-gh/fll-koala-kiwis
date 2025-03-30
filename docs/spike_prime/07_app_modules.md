# App Modules

## Overview

The SPIKE App provides several modules for enhanced functionality:
- Bargraph: Create bar graphs
- Display: Show images and text
- Linegraph: Create line graphs
- Music: Play music and sounds

## Bargraph Module

Create and manipulate bar graphs:

```python
from app import bargraph
import color

# Set a value for a colored bar
bargraph.set_value(color.RED, 75)

# Change value
bargraph.change(color.BLUE, 25)

# Get current value
value = await bargraph.get_value(color.GREEN)

# Clear all bars
bargraph.clear_all()

# Show/hide the graph
bargraph.show(fullscreen=True)
bargraph.hide()
```

## Display Module

Show images and text in the app:

```python
from app import display

# Show text
display.text("Hello SPIKE!")

# Show predefined images
display.image(display.IMAGE_ROBOT_1)
display.image(display.IMAGE_AMUSEMENT_PARK)

# Show/hide display
display.show(fullscreen=True)
display.hide()
```

### Available Images

```python
# Robot images
display.IMAGE_ROBOT_1
display.IMAGE_ROBOT_2
display.IMAGE_ROBOT_3
display.IMAGE_ROBOT_4
display.IMAGE_ROBOT_5

# Hub images
display.IMAGE_HUB_1
display.IMAGE_HUB_2
display.IMAGE_HUB_3
display.IMAGE_HUB_4

# Scene images
display.IMAGE_AMUSEMENT_PARK  # = 13
display.IMAGE_BEACH           # = 14
display.IMAGE_HAUNTED_HOUSE   # = 15
display.IMAGE_CARNIVAL        # = 16
display.IMAGE_CAVE           # = 17
display.IMAGE_OCEAN          # = 18
display.IMAGE_POLAR_BEAR     # = 19
display.IMAGE_PARK           # = 20
display.IMAGE_RANDOM         # = 21
display.IMAGE_BOOKSHELF
display.IMAGE_PLAYGROUND
display.IMAGE_MOON
```

## Linegraph Module

Create dynamic line graphs:

```python
from app import linegraph
import color

# Plot points
linegraph.plot(color.RED, 1, 50)
linegraph.plot(color.RED, 2, 75)

# Get statistics
average = await linegraph.get_average(color.RED)
maximum = await linegraph.get_max(color.RED)
minimum = await linegraph.get_min(color.RED)
last = await linegraph.get_last(color.RED)

# Clear specific color or all
linegraph.clear(color.RED)
linegraph.clear_all()

# Show/hide the graph
linegraph.show(fullscreen=True)
linegraph.hide()
```

## Music Module

Play music and sounds:

```python
from app import music

# Play an instrument
music.play_instrument(music.INSTRUMENT_PIANO, 60, 500)  # Middle C for 500ms

# Play a drum
music.play_drum(music.DRUM_SNARE)
```

### Available Instruments and Drums

```python
# Drums
DRUM_BASS = 2
DRUM_BONGO = 13
DRUM_CABASA = 15
DRUM_CLAVES = 9
DRUM_CLOSED_HI_HAT = 6
DRUM_CONGA = 14
DRUM_COWBELL = 11
DRUM_CRASH_CYMBAL = 4
DRUM_CUICA = 18
DRUM_GUIRO = 16
DRUM_HAND_CLAP = 8
DRUM_OPEN_HI_HAT = 5
DRUM_SIDE_STICK = 3
DRUM_SNARE = 1
DRUM_TAMBOURINE = 7
DRUM_TRIANGLE = 12
DRUM_VIBRASLAP = 17
DRUM_WOOD_BLOCK = 10

# Instruments
INSTRUMENT_BASS = 6
INSTRUMENT_BASSOON = 14
INSTRUMENT_PIANO = 1
INSTRUMENT_GUITAR = 2
INSTRUMENT_SAXOPHONE = 3
# ... and more
```

## Sound Module

Play sounds with control:

```python
from app import sound

# Play a sound
await sound.play("Cat Meow", volume=100, pitch=0, pan=0)

# Set sound attributes
sound.set_attributes(volume=80, pitch=10, pan=-50)

# Control volume separately
sound.volume(50)

# Stop all sounds
sound.stop()
```

## Best Practices

1. **Display Management**
   - Clear displays when done
   - Use appropriate screen modes
   - Consider update frequency

2. **Sound Control**
   - Manage volume levels
   - Clean up sounds when done
   - Use appropriate durations

3. **Graph Usage**
   - Clear old data when starting new
   - Use appropriate scales
   - Choose suitable update rates

4. **Performance**
   - Don't update too frequently
   - Clean up resources
   - Use async functions appropriately

## Next Steps

Continue to [Sound and Display](08_sound_and_display.md) for more detailed information about sound and display capabilities. 