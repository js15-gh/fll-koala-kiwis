# Conditions and Logic

## If Statements

The if statement is fundamental for controlling program flow:

```python
from hub import port, sound
import color
import color_sensor

# Basic if statement
if color_sensor.color(port.A) == color.RED:
    sound.beep(440, 1000)
```

## Multiple Conditions

Use elif and else for multiple conditions:

```python
from hub import button, port, sound
import color
import color_sensor
import runloop

# Function to check for red color
def red_detected():
    return color_sensor.color(port.A) == color.RED

# Function to check button press
def left_pressed():
    return button.pressed(button.LEFT) > 0

async def main():
    while True:
        if red_detected():
            # Red color detected
            sound.beep(440, 1000000, 100)
            while red_detected():
                await runloop.sleep_ms(1)
        elif left_pressed():
            # Left button pressed
            sound.beep(880, 200, 100)
            while left_pressed():
                await runloop.sleep_ms(1)
        else:
            # Neither condition is true
            sound.stop()

runloop.run(main())
```

## Logical Operators

Combine conditions using logical operators:

```python
# AND operator
if force_sensor.force(port.A) > 50 and button.pressed(button.LEFT):
    print("Force high AND button pressed")

# OR operator
if color_sensor.color(port.A) == color.RED or color_sensor.color(port.A) == color.BLUE:
    print("Red OR blue detected")

# NOT operator
if not button.pressed(button.LEFT):
    print("Button is NOT pressed")
```

## Multiple Concurrent Conditions

Run multiple checks simultaneously using coroutines:

```python
import runloop
from hub import port, sound

async def check_color():
    while True:
        if color_sensor.color(port.A) == color.RED:
            sound.beep(440, 1000000, 100)
        await runloop.sleep_ms(1)

async def check_button():
    while True:
        if button.pressed(button.LEFT):
            sound.beep(880, 200, 100)
        await runloop.sleep_ms(1)

# Run both checks simultaneously
runloop.run(check_color(), check_button())
```

## Comparison Operators

Python provides several comparison operators:

```python
# Equal to
if value == 100:
    print("Equal to 100")

# Not equal to
if value != 0:
    print("Not zero")

# Greater than
if value > 50:
    print("Above 50")

# Less than
if value < 50:
    print("Below 50")

# Greater than or equal to
if value >= 100:
    print("100 or more")

# Less than or equal to
if value <= 0:
    print("Zero or negative")
```

## Best Practices

1. **Condition Structure**
   - Order conditions by priority
   - Use elif for mutually exclusive conditions
   - Provide else clause for error handling

2. **Logic Design**
   - Keep conditions simple and clear
   - Break complex conditions into functions
   - Use meaningful function names

3. **Performance**
   - Avoid unnecessary condition checks
   - Use appropriate sleep times in loops
   - Consider using concurrent coroutines

4. **Error Handling**
   - Handle all possible conditions
   - Provide default behaviors
   - Log unexpected conditions

## Next Steps

Continue to [App Modules](07_app_modules.md) to learn about additional functionality available through the SPIKE App. 