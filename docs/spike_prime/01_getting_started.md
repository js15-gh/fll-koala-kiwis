# Getting Started with SPIKE Prime Python

## Introduction to Python

Python is a popular text-based coding language that is excellent for beginners because it's concise and easy-to-read. It's also useful for programmers because it's applicable to web and software development, as well as scientific applications like data analysis and machine learning.

This Getting Started section introduces the basics of using Python with LEGO® Education SPIKE™ Prime.

## Python Syntax

When learning a text programming language, the first step is to understand its syntax. Python has specific rules for:

- Each statement begins with indentation and ends with a line break
- Indentation (4 spaces) defines code blocks
- Lines with the same indentation belong to the same block

The Code Editor helps you write correct code by:
- Auto-indenting new lines
- Numbering lines for navigation
- Highlighting syntax in different colors

Example of proper syntax:
```python
# This is a comment (green)
print('LEGO')  # Text is magenta
if True:       # Keywords are blue
    print(123) # Numbers are orange
```

## Hello, World!

It's a tradition when learning a new programming language to create a "Hello, World!" program. First, make sure your SPIKE Prime Hub is turned on and connected to the SPIKE App.

```python
from hub import light_matrix

light_matrix.write('Hello, World!')
```

You'll see the text "Hello, World!" scrolling across the Light Matrix.

## Define Functions

Functions organize code into reusable blocks:

```python
from hub import light_matrix

def hello():
    light_matrix.write('Hello, World!')

hello()
```

### Add Parameters

Make functions more flexible with parameters:

```python
from hub import light_matrix

def hello(name):
    light_matrix.write('Hello, ' + name + '!')

hello('World')
```

## Comments in Python

Comments help explain your code and start with #:

```python
# This is a comment
from hub import light_matrix  # Import statement
# This is another comment
```

### Using Comments for Planning (Pseudocode)

```python
# Show a happy face with eyes
# Wait for some time
# Show a smile without eyes
# Wait briefly
# Show the first image again
```

### Code Example: Blinking Eyes

```python
import time
from hub import light_matrix

def blink():
    # Show happy face
    light_matrix.show_image(light_matrix.IMAGE_HAPPY)
    time.sleep_ms(1000)  # Wait 1 second
    
    # Blink
    light_matrix.show_image(light_matrix.IMAGE_SMILE)
    time.sleep_ms(200)   # Brief blink
    
    # Return to happy face
    light_matrix.show_image(light_matrix.IMAGE_HAPPY)

# Blink three times
for _ in range(3):
    blink()
    time.sleep_ms(1000)
```

## SPIKE Prime Modules

To control the SPIKE Prime Hub, sensors, and motors, you'll need the SPIKE Prime modules:

```python
# Import required modules
import motor            # For motor control
import color_sensor     # For color sensing
from hub import port    # For port access
```

Import the modules you need once at the beginning of your Python program.

## MicroPython

The SPIKE Prime Hub runs MicroPython, a highly optimized version of Python designed for microcontrollers. This is important because:

- The Hub has limited memory and processing power
- Modules are optimized for performance
- Some data types (like integers) are optimized while others (like floats) are not
- Use whole numbers instead of decimals (e.g., 500ms instead of 0.5s)

## Best Practices

1. **Code Organization**
   - Import modules at the start
   - Define functions before using them
   - Use meaningful names
   - Keep code blocks focused

2. **Comments**
   - Don't repeat obvious code (avoid "WET" - Write Everything Twice)
   - Follow "DRY" principle (Don't Repeat Yourself)
   - Use comments to explain complex logic
   - Use pseudocode for planning

3. **Error Prevention**
   - Check device connections
   - Use appropriate data types
   - Test code in small chunks
   - Handle errors gracefully

## Challenge

Try these exercises:
1. Modify the "Hello, World!" program to greet you by name
2. Create a custom blinking pattern
3. Combine text and images in a program
4. Use different timing in the blink function

## Next Steps

After mastering these basics, continue to:
- [Python Basics](02_python_basics.md) for more detailed Python concepts
- [Motor Control](03_motor_control.md) to learn about movement
- [Variables and Loops](04_variables_and_loops.md) for program flow
- [Sensor Control](05_sensor_control.md) for working with sensors 