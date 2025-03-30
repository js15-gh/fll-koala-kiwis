# Advanced Concepts

## Asynchronous Programming

Understanding async/await and coroutines:

```python
import runloop
import motor
from hub import port

async def main():
    # Awaitable function call
    await motor.run_for_degrees(port.A, 360, 720)
    
    # Multiple awaitable calls
    await motor.run_for_degrees(port.B, 360, 720)

# Run the coroutine
runloop.run(main())
```

## Run Loops

The run loop is essential for async operations. The `runloop` module provides several key functions:

### sleep_ms()

Pause execution for a specified duration:

```python
from hub import light_matrix
import runloop

async def main():
    light_matrix.write("Hi!")
    # Wait for ten seconds 
    await runloop.sleep_ms(10000)
    light_matrix.write("Are you still here?")

runloop.run(main())
```

Parameters:
- `duration: int` - The duration in milliseconds

### until()

Wait for a condition to become true:

```python
import color_sensor
import color
from hub import port
import runloop

def is_color_red():
    return color_sensor.color(port.A) is color.RED

async def main():
    # Wait until Color Sensor sees red 
    await runloop.until(is_color_red)
    print("Red!")

runloop.run(main())
```

Parameters:
- `function: Callable[[], bool]` - A callable (function or lambda) that returns True or False
- `timeout: int = 0` - Optional timeout in milliseconds (0 means no timeout)

## Multiple Coroutines

Running multiple tasks concurrently:

```python
import runloop
from hub import port, sound
import color_sensor
import motor

async def check_color():
    while True:
        if color_sensor.color(port.A) == color.RED:
            await motor.run_for_degrees(port.B, 360, 720)
        await runloop.sleep_ms(100)

async def monitor_force():
    while True:
        if force_sensor.force(port.C) > 50:
            sound.beep(880, 200, 100)
        await runloop.sleep_ms(100)

# Run both monitoring tasks
runloop.run(check_color(), monitor_force())
```

## Error Handling

Proper error handling in async code:

```python
import runloop
from hub import port, sound
import motor

async def safe_motor_run():
    try:
        await motor.run_for_degrees(port.A, 360, 720)
    except Exception as e:
        print(f"Motor error: {e}")
        sound.beep(220, 1000, 100)  # Error sound
    finally:
        # Clean up
        motor.stop(port.A)

async def main():
    while True:
        try:
            await safe_motor_run()
        except Exception as e:
            print(f"Main error: {e}")
        await runloop.sleep_ms(1000)

runloop.run(main())
```

## State Management

Managing program state effectively:

```python
import runloop
from hub import port, sound
import motor

class RobotState:
    def __init__(self):
        self.is_running = False
        self.error_count = 0
        self.last_sensor_value = 0

    async def run(self):
        while True:
            if self.is_running:
                try:
                    await motor.run_for_degrees(port.A, 360, 720)
                except Exception as e:
                    self.error_count += 1
                    if self.error_count > 3:
                        self.is_running = False
            await runloop.sleep_ms(100)

# Create and run state manager
state = RobotState()
runloop.run(state.run())
```

## Advanced Motor Control

Complex movement patterns:

```python
import runloop
import motor
from hub import port

async def smooth_acceleration():
    # Start slow and gradually increase speed
    for speed in range(100, 1000, 100):
        await motor.run(port.A, speed, acceleration=100)
        await runloop.sleep_ms(500)

async def synchronized_movement():
    # Move motors in synchronized patterns
    while True:
        # Forward
        await motor.run_for_degrees(port.A, 360, 720)
        await motor.run_for_degrees(port.B, 360, 720)
        
        # Turn
        await motor.run_for_degrees(port.A, 180, 720)
        await motor.run_for_degrees(port.B, -180, 720)

runloop.run(smooth_acceleration(), synchronized_movement())
```

## Best Practices

1. **Async Programming**
   - Always use await with coroutines
   - Handle errors in each coroutine
   - Use sleep_ms to prevent blocking
   - Clean up resources properly
   - Use until() for condition-based waiting
   - Set appropriate timeouts

2. **State Management**
   - Use classes for complex state
   - Keep state changes atomic
   - Monitor state transitions
   - Handle edge cases

3. **Error Recovery**
   - Implement retry mechanisms
   - Log errors appropriately
   - Have fallback behaviors
   - Clean up after errors

4. **Performance**
   - Optimize coroutine scheduling
   - Minimize resource usage
   - Monitor memory usage
   - Profile critical sections
   - Use appropriate sleep intervals

## Next Steps

This concludes the SPIKE Prime Python documentation. You can now:
- Build complex robots
- Create sophisticated programs
- Handle errors gracefully
- Manage multiple tasks
- Use advanced async features

Remember to check the [Examples](examples/) directory for more sample programs and inspiration. 