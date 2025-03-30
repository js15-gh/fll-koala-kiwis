# Variables and Loops

## Variable Basics

Variables store values that you can use throughout your program:

```python
import motor
import runloop
from hub import port

async def main():
    # Create a variable for velocity
    velocity = 720
    degrees = 360

    # Use variables in motor commands
    await motor.run_for_degrees(port.A, degrees, velocity)
    await motor.run_for_degrees(port.B, degrees, velocity)

runloop.run(main())
```

## Variable Scope

Variables can be local or global:

```python
# Global variable - available everywhere
velocity = 720

async def main():
    # Local variable - only available in this function
    degrees = 360
    
    # Use both variables
    await motor.run_for_degrees(port.A, degrees, velocity)
```

### Using Global Variables

To modify global variables inside functions:

```python
velocity = 450

async def main():
    # Declare we're using the global variable
    global velocity
    
    # Now we can modify it
    velocity = velocity + 90
```

## Loops

### For Loops

Repeat code a specific number of times:

```python
import random
import time
from hub import light

# Loop 10 times
for color in range(11):
    # Set light to current color
    light.color(light.POWER, color)
    # Wait random time
    time.sleep_ms(random.randint(500, 1500))
```

### While Loops

Repeat code while a condition is true:

```python
import random
import time
from hub import light

while True:
    # Generate random color (1-9)
    random_color = random.randint(1, 9)
    
    # Set light color
    light.color(light.POWER, random_color)
    
    # Random delay
    time.sleep_ms(random.randint(500, 1500))
```

## Lists and Constants

Store multiple values in lists:

```python
import random
import time
import color
from hub import light

# Create a list of colors
colors = [color.RED, color.GREEN, color.BLUE, color.YELLOW]

# Choose random number of iterations
times = random.randint(5, 10)

for i in range(times):
    # Pick random color from list
    random_color = random.choice(colors)
    light.color(light.POWER, random_color)
```

## Random Operations

The random module provides several useful functions:

```python
import random

# Random integer in range
value = random.randint(1, 10)

# Random choice from list
color = random.choice(colors)

# Random float between 0 and 1
fraction = random.random()
```

## Best Practices

1. **Variable Naming**
   - Use descriptive names
   - Follow Python naming conventions
   - Be consistent with naming style

2. **Scope Management**
   - Keep variables in smallest needed scope
   - Use global variables sparingly
   - Document global variable usage

3. **Loop Design**
   - Choose appropriate loop type
   - Include exit conditions for while loops
   - Consider performance in tight loops

4. **Random Values**
   - Seed random if reproducibility needed
   - Use appropriate random functions
   - Consider ranges carefully

## Next Steps

Continue to [Sensor Control](05_sensor_control.md) to learn how to use sensor inputs to control your robot's behavior. 