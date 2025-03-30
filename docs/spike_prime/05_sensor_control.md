# Sensor Control

## Overview

![SPIKE Prime Hub with components](../images/spike_prime_sensor_components.png)
*SPIKE Prime components showing: (left) hand placing a red LEGO brick, (middle) a sensor unit with cable, and (right) the Hub unit*

Sensors allow your robot to interact with its environment. The SPIKE Prime has several types of sensors that can be used to control your robot's behavior.

## Force Sensor

Connect a Force Sensor to port B and try this basic program:

```python
import force_sensor
import motor
from hub import port

# Store the force of the Force Sensor in a variable
force = force_sensor.force(port.B)

# Print the force value
print(force)

# Use force to control motor speed
motor.run(port.A, force)
```

### Continuous Force Reading

For continuous monitoring:

```python
import force_sensor
import motor
from hub import port

while True:
    # Get current force
    force = force_sensor.force(port.B)
    
    # Print value for debugging
    print(force)
    
    # Control motor with force
    motor.run(port.A, force)
```

## Color Sensor

The Color Sensor can detect different colors and light levels:

```python
from hub import port, sound
import color
import color_sensor
import runloop

async def main():
    while True:
        # Check if red color is detected
        if color_sensor.color(port.A) == color.RED:
            # Make a sound when red is detected
            sound.beep(440, 1000000, 100)
            
            # Wait while red is still detected
            while color_sensor.color(port.A) == color.RED:
                await runloop.sleep_ms(1)
                
            # Stop sound when red is gone
            sound.stop()

runloop.run(main())
```

## Debugging with Console

Use print() statements to debug sensor readings:

```python
while True:
    force = force_sensor.force(port.B)
    color = color_sensor.color(port.A)
    
    print(f"Force: {force}, Color: {color}")
    await runloop.sleep_ms(100)
```

## Function Return Values

Create functions to process sensor data:

```python
def motor_velocity():
    # Multiply force by 5 for better control range
    return force_sensor.force(port.B) * 5

while True:
    # Use function return value for velocity
    motor.run(port.A, motor_velocity())
```

## Best Practices

1. **Sensor Reading**
   - Check sensor connection before reading
   - Handle missing sensor errors
   - Use appropriate sampling rates

2. **Data Processing**
   - Filter noisy sensor data
   - Scale values to useful ranges
   - Consider sensor limitations

3. **Error Handling**
   - Check for sensor errors
   - Provide feedback when sensors fail
   - Have fallback behaviors

4. **Performance**
   - Don't read sensors too frequently
   - Use appropriate sleep times
   - Consider sensor response times

## Next Steps

Continue to [Conditions and Logic](06_conditions_and_logic.md) to learn how to make decisions based on sensor inputs. 