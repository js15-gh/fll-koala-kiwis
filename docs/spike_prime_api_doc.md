# SPIKE Prime API Documentation

This document provides a comprehensive reference guide to the SPIKE Prime Python API.

## Getting Started

### Introduction to Python

Python is a popular text-based coding language that is excellent for beginners because it's concise and easy-to-read. It's also useful for programmers because it's applicable to web and software development, as well as scientific applications like data analysis and machine learning.

This Getting Started section introduces the basics of using Python with LEGO® Education SPIKE™ Prime. It contains chapters where you'll:

- Learn to use the Code Editor in the LEGO® Education SPIKE™ App to write Python code.
- Write a message on the Light Matrix of the SPIKE Prime Hub.
- Learn how comments can help you describe draft and finished programs.
- Define and start asynchronous functions to control motors.
- Control two motors with local and global variables.
- Discover ways to create fun and unpredictable programs that control the light on the Hub.
- Control a motor using the Force Sensor. Then learn ways to use the Console to debug your program.
- Use logical expressions to react to different conditions. Then learn to run different parts of your code together to react to multiple conditions.

### Python Syntax

When learning a text programming language, the first step is to understand its syntax. This language syntax prescribes the rules for writing statements (lines of code), and how to indicate code blocks that consist of multiple statements.

In Python, each statement begins with a level of indentation and ends with a line break. Indentation is the number of spaces before a statement. Lines with the same number of spaces have the same indentation level and belong to the same code block. The SPIKE App uses 4 spaces for each indentation level.

You write code in the Code Editor, which has features to help you write it correctly. For example, when you start a new code block, like a function or if statement, the Editor indents the next line with four extra spaces. Also, it numbers each line to make it easier to navigate your code.

Syntax highlighting in the Code Editor shows comments, keywords, text, and numbers in different colors so the code is easier to read. In the code below, the comment on the first line is green, the keywords print, if, and True are blue, the text 'LEGO' is magenta, and the number 123 is orange.

```python
# This is a comment.
print('LEGO')
if True:
    print(123)
```

### SPIKE Prime Modules

To control the SPIKE Prime Hub, sensors, and motors, you'll need the SPIKE Prime modules. Modules are used to organize related code. There's one for each SPIKE Prime component, e.g., the motor module contains the code to control the motors. To use the functionality of a module, first import it with the import statement:

```python
import motor
```

Import the modules you need once at the beginning of your Python program.

### MicroPython

The SPIKE Prime Hub is a small computer called a microcontroller, which has limited memory and processing power. Since the full Python programming language would use too much memory, the Hub runs MicroPython, a highly optimized version of the Python language that can run on microcontrollers. The modules to control the SPIKE Prime Hub, sensors, and motors are also highly optimized by using optimized data types.

You've seen that the Code Editor shows text and numbers in different colors – because they're different data types. Python further distinguishes between whole numbers and decimals. Whole numbers are also known as integers, or type int, which is optimized in MicroPython. Decimals use the unoptimized float type, so the SPIKE Prime modules avoid this data type. This means you have to stick to whole numbers or use different units to describe decimals. For half a second, you can use 500 milliseconds instead of 0.5 seconds.

## Basic Concepts

### Hello, World!

```python
from hub import light_matrix

light_matrix.write('Hello, World!')
```

### Defining Functions

```python
from hub import light_matrix

def hello():
    light_matrix.write('Hello, World!')

hello()
```

### Function Parameters

```python
from hub import light_matrix

def hello(name):
    light_matrix.write('Hello, ' + name + '!')

hello('World')
```

### Comments in Python

```python
# This is a comment.
from hub import light_matrix
# This is another comment.
```

### Motor Control

```python
import motor
from hub import port

# Run a motor on port A for 360 degrees at 720 degrees per second.
motor.run_for_degrees(port.A, 360, 720)
```

### Run Loop, Async, and Await

```python
import motor
import runloop
from hub import port

async def main():
    # Run two motors on ports A and B for 360 degrees at 720 degrees per second.
    # The motors run after each other.
    await motor.run_for_degrees(port.A, 360, 720)
    await motor.run_for_degrees(port.B, 360, 720)

runloop.run(main())
```

### Variables

```python
import motor
import runloop
from hub import port

async def main():
    # Create a variable `velocity` with a value of 720.
    velocity = 720

    # Run two motors on ports A and B for 360 degrees.
    # Use the value of the `velocity` variable for the motor velocity.
    await motor.run_for_degrees(port.A, 360, velocity)
    await motor.run_for_degrees(port.B, 360, velocity)

runloop.run(main())
```

### Variable Scope

```python
import motor
import runloop
from hub import port

# Create a global variable `velocity` with a value of 720.
velocity = 720

async def main():
    # Create a local variable `degrees` with a value of 360.
    degrees = 360

    # Run two motors on ports A and B.
    # Use the value of the `degrees` variable for the number of degrees.
    # Use the value of the `velocity` variable for the motor velocity.
    await motor.run_for_degrees(port.A, degrees, velocity)
    await motor.run_for_degrees(port.B, degrees, velocity)

runloop.run(main())
```

### Variables in Loops

```python
import motor
import runloop
from hub import port

# Create a global variable `velocity` with a value of 450.
velocity = 450

async def main():
    # Use the `global` keyword to enable changing `velocity` here.
    global velocity

    # Create a local variable `degrees` with a value of 360.
    degrees = 360

    # The `for` loop creates a local variable `i` and repeats 4 times.
    # The values of the `i` variable are 0, 1, 2, and 3.
    for i in range(4):
        # Change the global variable `velocity` by adding `i`*90 each time.
        # The values of the `velocity` variable are 450, 540, 720, and 990.
        velocity = velocity + i*90
        await motor.run_for_degrees(port.A, degrees, velocity)

    # The value of the `velocity` variable outside the `for` loop is 990.
    await motor.run_for_degrees(port.B, degrees, velocity)

runloop.run(main())
```

## Module Reference

### Color Module

The color module contains all the color constants to use with other modules.

```python
import color
```

#### Constants

- `color.BLACK = 0`
- `color.PURPLE = 1`
- `color.BLUE = 3`
- `color.CYAN = 4`
- `color.TURQUOISE = 5`
- `color.GREEN = 5`
- `color.YELLOW = 7`
- `color.ORANGE = 8`
- `color.RED = 9`
- `color.WHITE = 10`
- `color.NONE = None`

### Color Sensor Module

The color_sensor module enables you to write code that reacts to colors and reflected light.

```python
import color_sensor
```

#### Functions

**color**

```python
color_sensor.color(port: int) -> int
```

Retrieves the detected color from the Color Sensor.

Parameters:
- `port: int` - A port from the port submodule in the hub module

Example:
```python
if color_sensor.color(port.A) is color.RED:
    print("Red detected")
```

**reflection**

```python
color_sensor.reflection(port: int) -> int
```

Retrieves the intensity of the reflected light (0-100%).

Parameters:
- `port: int` - A port from the port submodule in the hub module

**rgbi**

```python
color_sensor.rgbi(port: int) -> tuple[int, int, int, int]
```

Retrieves the overall color intensity and intensity of red, green and blue.

Returns `tuple[red: int, green: int, blue: int, intensity: int]`

Parameters:
- `port: int` - A port from the port submodule in the hub module

### Distance Sensor Module

The distance_sensor module enables you to write code that reacts to specific distances or light up the Distance Sensor in different ways.

```python
import distance_sensor
```

#### Functions

**clear**

```python
distance_sensor.clear(port: int) -> None
```

Turns off all the lights in the Distance Sensor connected to port.

Parameters:
- `port: int` - A port from the port submodule in the hub module

**distance**

```python
distance_sensor.distance(port: int) -> int
```

Retrieve the distance in millimeters captured by the Distance Sensor connected to port. If the Distance Sensor cannot read a valid distance it will return -1.

Parameters:
- `port: int` - A port from the port submodule in the hub module

**get_pixel**

```python
distance_sensor.get_pixel(port: int, x: int, y: int) -> int
```

Retrieve the intensity of a specific light on the Distance Sensor connected to port.

Parameters:
- `port: int` - A port from the port submodule in the hub module
- `x: int` - The X value (0 - 3)
- `y: int` - The Y value, range (0 - 3)

**set_pixel**

```python
distance_sensor.set_pixel(port: int, x: int, y: int, intensity: int) -> None
```

Changes the intensity of a specific light on the Distance Sensor connected to port.

Parameters:
- `port: int` - A port from the port submodule in the hub module
- `x: int` - The X value (0 - 3)
- `y: int` - The Y value, range (0 - 3)
- `intensity: int` - How bright to light up the pixel

**show**

```python
distance_sensor.show(port: int, pixels: list[int]) -> None
```

Change all the lights at the same time.

Example:
```python
from hub import port
import distance_sensor

# Update all pixels on Distance Sensor using the show function 
# Create a list with 4 identical intensity values 
pixels = [100] * 4 
# Update all pixels to show same intensity 
distance_sensor.show(port.A, pixels)
```

Parameters:
- `port: int` - A port from the port submodule in the hub module
- `pixels: bytes` - A list containing intensity values for all 4 pixels.

### Force Sensor Module

The force_sensor module contains all functions and constants to use the Force Sensor.

```python
import force_sensor
```

#### Functions

**force**

```python
force_sensor.force(port: int) -> int
```

Retrieves the measured force as decinewton. Values range from 0 to 100

Example:
```python
from hub import port
import force_sensor
print(force_sensor.force(port.A))
```

Parameters:
- `port: int` - A port from the port submodule in the hub module

**pressed**

```python
force_sensor.pressed(port: int) -> bool
```

Tests whether the button on the sensor is pressed. Returns true if the force sensor connected to port is pressed.

Example:
```python
from hub import port
import force_sensor
print(force_sensor.pressed(port.A))
```

Parameters:
- `port: int` - A port from the port submodule in the hub module

**raw**

```python
force_sensor.raw(port: int) -> int
```

Returns the raw, uncalibrated force value of the force sensor connected on port port

Example:
```python
from hub import port
import force_sensor
print(force_sensor.raw(port.A))
```

Parameters:
- `port: int` - A port from the port submodule in the hub module

### Hub Module

#### Button Submodule

```python
from hub import button
```

**pressed**

```python
button.pressed(button: int) -> int
```

This module allows you to react to buttons being pressed on the hub.

Parameters:
- `button: int` - The button to check (button.LEFT, button.RIGHT, etc.)

### Motor Module

```python
import motor
```

#### Functions

(Motor module functions documentation will be added here)

### Motor Pair Module

The motor_pair module enables you to write code that controls two motors at the same time.

```python
import motor_pair
```

#### Functions

**move**

```python
motor_pair.move(pair: int, steering: int, *, velocity: int = 360, acceleration: int = 1000) -> None
```

Move a Motor Pair at a constant speed until a new command is given.

Example:
```python
from hub import port
import runloop
import motor_pair

async def main():
    # Pair motors on port A and B 
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

    await runloop.sleep_ms(2000)

    # Move straight at default velocity 
    motor_pair.move(motor_pair.PAIR_1, 0)

    await runloop.sleep_ms(2000)

    # Move straight at a specific velocity 
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=280)

    await runloop.sleep_ms(2000)

    # Move straight at a specific velocity and acceleration 
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=280, acceleration=100)

runloop.run(main())
```

Parameters:
- `pair: int` - The pair slot of the Motor Pair.
- `steering: int` - The steering (-100 to 100)

Optional keyword arguments:
- `velocity: int` - The velocity in degrees/sec (defaults to 360)
- `acceleration: int` - The acceleration (deg/sec²) (1 - 10000)

**move_for_degrees**

```python
motor_pair.move_for_degrees(pair: int, degrees: int, steering: int, *, velocity: int = 360, stop: int = motor.BRAKE, acceleration: int = 1000, deceleration: int = 1000) -> Awaitable
```

Move a Motor Pair at a constant speed for a specific number of degrees.

Example:
```python
from hub import port
import runloop
import motor_pair

async def main():
    # Pair motors on port A and B 
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

    # Move straight at default velocity for 90 degrees 
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 90, 0)

    # Move straight at a specific velocity 
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 360, 0, velocity=280)

    # Move straight at a specific velocity with a slow deceleration 
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 360, 0, velocity=280, deceleration=10)

runloop.run(main())
```

Parameters:
- `pair: int` - The pair slot of the Motor Pair.
- `degrees: int` - The number of degrees
- `steering: int` - The steering (-100 to 100)

Optional keyword arguments:
- `velocity: int` - The velocity in degrees/sec
- `stop: int` - The behavior of the Motor after it has stopped. Use the constants in the motor module.
- `acceleration: int` - The acceleration (deg/sec²) (1 - 10000)
- `deceleration: int` - The deceleration (deg/sec²) (1 - 10000)

**move_for_time**

```python
motor_pair.move_for_time(pair: int, duration: int, steering: int, *, velocity: int = 360, stop: int = motor.BRAKE, acceleration: int = 1000, deceleration: int = 1000) -> Awaitable
```

Move a Motor Pair at a constant speed for a specific duration.

Example:
```python
from hub import port
import runloop
import motor_pair

async def main():
    # Pair motors on port A and B 
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

    # Move straight at default velocity for 1 second 
    await motor_pair.move_for_time(motor_pair.PAIR_1, 1000, 0)

    # Move straight at a specific velocity for 1 second 
    await motor_pair.move_for_time(motor_pair.PAIR_1, 1000, 0, velocity=280)

    # Move straight at a specific velocity for 10 seconds with a slow deceleration 
    await motor_pair.move_for_time(motor_pair.PAIR_1, 10000, 0, velocity=280, deceleration=10)

runloop.run(main())
```

Parameters:
- `pair: int` - The pair slot of the Motor Pair.
- `duration: int` - The duration in milliseconds
- `steering: int` - The steering (-100 to 100)

Optional keyword arguments:
- `velocity: int` - The velocity in degrees/sec
- `stop: int` - The behavior of the Motor after it has stopped. Use the constants in the motor module.
- `acceleration: int` - The acceleration (deg/sec²) (1 - 10000)
- `deceleration: int` - The deceleration (deg/sec²) (1 - 10000)

**move_tank**

```python
motor_pair.move_tank(pair: int, left_velocity: int, right_velocity: int, *, acceleration: int = 1000) -> None
```

Perform a tank move on a Motor Pair at a constant speed until a new command is given.

Example:
```python
from hub import port
import runloop
import motor_pair

async def main():
    # Pair motors on port A and B 
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

    # Move straight at default velocity 
    motor_pair.move_tank(motor_pair.PAIR_1, 1000, 1000)

    await runloop.sleep_ms(2000)

    # Turn right 
    motor_pair.move_tank(motor_pair.PAIR_1, 0, 1000)

    await runloop.sleep_ms(2000)

    # Perform tank turn 
    motor_pair.move_tank(motor_pair.PAIR_1, 1000, -1000)

runloop.run(main())
```

Parameters:
- `pair: int` - The pair slot of the Motor Pair.
- `left_velocity: int` - The velocity (deg/sec) of the left motor.
- `right_velocity: int` - The velocity (deg/sec) of the right motor.

Optional keyword arguments:
- `acceleration: int` - The acceleration (deg/sec²) (1 - 10000)

**move_tank_for_degrees**

```python
motor_pair.move_tank_for_degrees(pair: int, degrees: int, left_velocity: int, right_velocity: int, *, stop: int = motor.BRAKE, acceleration: int = 1000, deceleration: int = 1000) -> Awaitable
```

Perform a tank move on a Motor Pair at a constant speed until a new command is given.

Example:
```python
from hub import port
import runloop
import motor_pair

async def main():
    # Pair motors on port A and B 
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

    # Move straight at default velocity for 360 degrees 
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 360, 1000, 1000)

    # Turn right for 180 degrees 
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 180, 0, 1000)

    # Perform tank turn for 720 degrees 
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 720, 1000, -1000)

runloop.run(main())
```

Parameters:
- `pair: int` - The pair slot of the Motor Pair.
- `degrees: int` - The number of degrees
- `left_velocity: int` - The velocity (deg/sec) of the left motor.
- `right_velocity: int` - The velocity (deg/sec) of the right motor.

Optional keyword arguments:
- `stop: int` - The behavior of the Motor after it has stopped. Use the constants in the motor module.
- `acceleration: int` - The acceleration (deg/sec²) (1 - 10000)
- `deceleration: int` - The deceleration (deg/sec²) (1 - 10000)

**move_tank_for_time**

```python
motor_pair.move_tank_for_time(pair: int, left_velocity: int, right_velocity: int, duration: int, *, stop: int = motor.BRAKE, acceleration: int = 1000, deceleration: int = 1000) -> Awaitable
```

Perform a tank move on a Motor Pair at a constant speed for a specific amount of time.

Example:
```python
from hub import port
import runloop
import motor_pair

async def main():
    # Pair motors on port A and B 
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)

    # Move straight at default velocity for 1 second 
    await motor_pair.move_tank_for_time(motor_pair.PAIR_1, 1000, 1000, 1000)

    # Turn right for 3 seconds 
    await motor_pair.move_tank_for_time(motor_pair.PAIR_1, 0, 1000, 3000)

    # Perform tank turn for 2 seconds 
    await motor_pair.move_tank_for_time(motor_pair.PAIR_1, 1000, -1000, 2000)

runloop.run(main())
```

Parameters:
- `pair: int` - The pair slot of the Motor Pair.
- `duration: int` - The duration in milliseconds
- `left_velocity: int` - The velocity (deg/sec) of the left motor.
- `right_velocity: int` - The velocity (deg/sec) of the right motor.

Optional keyword arguments:
- `stop: int` - The behavior of the Motor after it has stopped. Use the constants in the motor module.
- `acceleration: int` - The acceleration (deg/sec²) (1 - 10000)
- `deceleration: int` - The deceleration (deg/sec²) (1 - 10000)

**pair**

```python
motor_pair.pair(pair: int, left_motor: int, right_motor: int) -> None
```

Pair two motors (left_motor & right_motor) and store the paired motors in pair.
Use pair in all subsequent motor_pair related function calls.

Example:
```python
import motor_pair
from hub import port

motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
```

Parameters:
- `pair: int` - The pair slot of the Motor Pair.
- `left_motor: int` - The port of the left motor. Use the port submodule in the hub module.
- `right_motor: int` - The port of the right motor. Use the port submodule in the hub module.

**stop**

```python
motor_pair.stop(pair: int, *, stop: int = motor.BRAKE) -> None
```

Stops a Motor Pair.

Example:
```python
import motor_pair

motor_pair.stop(motor_pair.PAIR_1)
```

Parameters:
- `pair: int` - The pair slot of the Motor Pair.

Optional keyword arguments:
- `stop: int` - The behavior of the Motor after it has stopped. Use the constants in the motor module.

**unpair**

```python
motor_pair.unpair(pair: int) -> None
```

Unpair a Motor Pair.

Example:
```python
import motor_pair

motor_pair.unpair(motor_pair.PAIR_1)
```

Parameters:
- `pair: int` - The pair slot of the Motor Pair.

### Constants

```python
PAIR_1 = 0  # First Motor Pair
PAIR_2 = 1  # Second Motor Pair
PAIR_3 = 2  # Third Motor Pair
```

### Runloop Module

The runloop module contains all functions and constants to use the Runloop.

```python
import runloop
```

#### Functions

**run**

```python
runloop.run(*functions: Awaitable) -> None
```

Start any number of parallel async functions. This is the function you should use to create programs with a similar structure to Word Blocks.

Parameters:
- `*functions: awaitable` - The functions to run

**sleep_ms**

```python
runloop.sleep_ms(duration: int) -> Awaitable
```

Pause the execution of the application for any amount of milliseconds.

Example:
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

**until**

```python
runloop.until(function: Callable[[], bool], timeout: int = 0) -> Awaitable
```

Returns an awaitable that will return when the condition in the function or lambda passed is True or when it times out

Example:
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
- `function: Callable[[], bool]` - A callable with no parameters that returns either True or False.
- `timeout: int` - A timeout for the function in milliseconds. 0 means no timeout.

## Additional Resources

For more detailed information and examples, refer to the official LEGO Education SPIKE Prime documentation. 