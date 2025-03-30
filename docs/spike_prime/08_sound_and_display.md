# Sound and Display

## Hub Light Matrix

Control the Hub's built-in light matrix:

```python
from hub import light_matrix

# Write scrolling text
light_matrix.write('Hello, World!')

# Show predefined images
light_matrix.show_image(light_matrix.IMAGE_HAPPY)
light_matrix.show_image(light_matrix.IMAGE_SMILE)

# Create custom images
CUSTOM_IMAGE = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0]
]
light_matrix.show(CUSTOM_IMAGE)
```

## Hub Light

Control the Hub's power button light:

```python
from hub import light
import color

# Set light color
light.color(light.POWER, color.RED)

# Turn light off
light.color(light.POWER, color.BLACK)

# Cycle through colors
colors = [color.RED, color.GREEN, color.BLUE]
for c in colors:
    light.color(light.POWER, c)
    time.sleep_ms(1000)
```

## Hub Sound

Play sounds directly from the Hub:

```python
from hub import sound

# Play a beep
sound.beep(440, 1000, 100)  # frequency, duration, volume

# Play different frequencies
notes = [440, 494, 523, 587, 659]  # A4 to E5
for note in notes:
    sound.beep(note, 500, 100)
    time.sleep_ms(600)

# Stop sound
sound.stop()
```

## Advanced Display Features

### Animations

Create simple animations:

```python
import time
from hub import light_matrix

# Define animation frames
FRAMES = [
    light_matrix.IMAGE_HAPPY,
    light_matrix.IMAGE_SMILE,
    light_matrix.IMAGE_NEUTRAL,
    light_matrix.IMAGE_SAD
]

# Play animation
while True:
    for frame in FRAMES:
        light_matrix.show_image(frame)
        time.sleep_ms(500)
```

### Interactive Displays

Combine display with sensor input:

```python
from hub import light_matrix, port
import color_sensor
import time

while True:
    # Show different images based on color detected
    detected_color = color_sensor.color(port.A)
    
    if detected_color == color.RED:
        light_matrix.show_image(light_matrix.IMAGE_HEART)
    elif detected_color == color.GREEN:
        light_matrix.show_image(light_matrix.IMAGE_HAPPY)
    elif detected_color == color.BLUE:
        light_matrix.show_image(light_matrix.IMAGE_DIAMOND)
    
    time.sleep_ms(100)
```

## Sound Effects

Create complex sound patterns:

```python
from hub import sound
import time

def play_siren():
    # Alternating high and low frequencies
    for _ in range(3):
        sound.beep(880, 500, 100)  # High pitch
        time.sleep_ms(500)
        sound.beep(440, 500, 100)  # Low pitch
        time.sleep_ms(500)

def play_scale():
    # Play a musical scale
    frequencies = [262, 294, 330, 349, 392, 440, 494, 523]  # C4 to C5
    for freq in frequencies:
        sound.beep(freq, 300, 100)
        time.sleep_ms(350)
```

## Best Practices

1. **Display Management**
   - Clear display when done
   - Use appropriate brightness
   - Consider animation speed
   - Handle display updates efficiently

2. **Sound Management**
   - Use appropriate volumes
   - Clean up sounds when done
   - Consider sound duration
   - Don't overlap sounds unless intended

3. **Resource Usage**
   - Free resources when not needed
   - Don't block main thread
   - Use sleep appropriately
   - Consider battery impact

4. **User Experience**
   - Provide clear visual feedback
   - Use consistent patterns
   - Consider accessibility
   - Test in different conditions

## Next Steps

Continue to [Advanced Concepts](09_advanced_concepts.md) to learn about more sophisticated programming techniques. 