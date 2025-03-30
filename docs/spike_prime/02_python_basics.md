# Python Basics for SPIKE Prime

## Python Syntax

When learning Python, understanding syntax is crucial. Python has specific rules for:

- Indentation: Used to define code blocks
- Line breaks: Each statement ends with a line break
- Code blocks: Groups of related statements at the same indentation level

The Code Editor helps you write correct code by:
- Auto-indenting new lines
- Numbering lines for easy navigation
- Highlighting syntax in different colors

Example of proper syntax:
```python
# This is a comment.
print('LEGO')
if True:
    print(123)
```

## Comments in Python

Comments help explain your code. They start with the # character:

```python
# This is a comment.
from hub import light_matrix
# This is another comment.
```

You can also use comments to temporarily disable code:
```python
# The next line is commented out:
# light_matrix.write('Hello, World!')
```

### Using Comments for Planning

Comments can help plan your code (pseudocode):
```python
# Show a happy face with eyes on the Light Matrix.
# Wait for some time.
# Show a smile without eyes on the Light Matrix.
# Wait for a short time.
# Show the first image again on the Light Matrix.
```

## Data Types

MicroPython supports several data types:

- **int**: Whole numbers (optimized)
- **bool**: True/False values
- **str**: Text strings
- **float**: Decimal numbers (not optimized)
- **list**: Collections of values
- **tuple**: Immutable collections

Example of different data types:
```python
number = 42          # int
is_active = True     # bool
text = "LEGO"        # str
speed = 0.5          # float (avoid when possible)
colors = [1, 2, 3]   # list
coords = (0, 1)      # tuple
```

## Best Practices

1. **Code Organization**
   - Import modules at the start
   - Define functions before using them
   - Use meaningful variable names

2. **Memory Usage**
   - Use integers instead of floats
   - Clean up resources when done
   - Avoid creating unnecessary variables

3. **Code Style**
   - Use consistent indentation (4 spaces)
   - Add comments for complex logic
   - Keep functions small and focused

4. **Error Handling**
   - Check for connected devices
   - Handle sensor errors gracefully
   - Use print() for debugging

## Next Steps

After understanding these basics, you can:
- Start working with motors
- Use sensors
- Create more complex programs
- Explore advanced features

Continue to the [Motor Control](03_motor_control.md) section to learn how to make your robot move. 