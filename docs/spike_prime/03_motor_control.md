# Motor Control

![SPIKE Prime Motor and Hub](../images/spike_prime_motor_hub.png)
*SPIKE Prime Motor (light blue) connected to the Hub unit (white/yellow) via cable*

## Basic Motor Operations

Connect a motor to port A and try this basic program:

```python
import motor
from hub import port

# Run a motor on port A for 360 degrees at 720 degrees per second.
motor.run_for_degrees(port.A, 360, 720)
```

The motor will run one complete rotation (360 degrees) at a speed of 720 degrees per second.

## Multiple Motors

You can control multiple motors simultaneously:

```python
import motor
import runloop
from hub import port

async def main():
    # Run two motors on ports A and B for 360 degrees at 720 degrees per second.
    await motor.run_for_degrees(port.A, 360, 720)
    await motor.run_for_degrees(port.B, 360, 720)

runloop.run(main())
```

## Motor Functions

The motor module provides several key functions:

### run()
```python
motor.run(port: int, velocity: int, acceleration: int = 1000)
```
Starts a motor at constant speed.

### run_for_degrees()
```python
motor.run_for_degrees(port: int, degrees: int, velocity: int, 
                     stop: int = BRAKE, 
                     acceleration: int = 1000, 
                     deceleration: int = 1000)
```
Turns a motor for a specific number of degrees.

### Position Control
```python
# Get absolute position
position = motor.absolute_position(port.A)

# Get relative position
rel_pos = motor.relative_position(port.A)

# Reset relative position
motor.reset_relative_position(port.A, 0)
```

## Motor Pair Control

For more complex movements, you can pair motors:

```python
import motor_pair
import runloop
from hub import port

async def main():
    # Pair motors on port A and B 
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

    # Move straight
    await motor_pair.move_tank_for_time(motor_pair.PAIR_1, 1000, 1000, 1000)

    # Turn right
    await motor_pair.move_tank_for_time(motor_pair.PAIR_1, 0, 1000, 3000)

    # Tank turn
    await motor_pair.move_tank_for_time(motor_pair.PAIR_1, 1000, -1000, 2000)

runloop.run(main())
```

## Motor Constants

Important constants for motor control:

```python
# Stop modes
motor.COAST        # Coast until stop
motor.BRAKE        # Brake and continue braking
motor.HOLD         # Hold position
motor.CONTINUE     # Continue at current velocity
motor.SMART_COAST  # Smart coast with compensation
motor.SMART_BRAKE  # Smart brake with compensation

# Status constants
motor.READY        # Motor is ready
motor.RUNNING      # Motor is running
motor.STALLED      # Motor is stalled
motor.CANCELED     # Command was canceled
motor.ERROR        # Error occurred
motor.DISCONNECTED # Motor is disconnected
```

## Best Practices

1. **Speed Control**
   - Use appropriate speeds for your robot's size
   - Consider acceleration for smooth movement
   - Use brake or hold when precision is needed

2. **Error Handling**
   - Check motor connection before running
   - Handle stall conditions
   - Use status returns to verify operation

3. **Movement Precision**
   - Use relative positioning for precise movements
   - Consider using paired motors for straight lines
   - Calibrate movements when needed

## Next Steps

Continue to [Variables and Loops](04_variables_and_loops.md) to learn how to make your motor control more dynamic and repeatable. 