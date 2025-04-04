# SPIKE Prime Motor Control: 5-Day Learning Plan

## Overview

This curriculum introduces 6th-grade students with no previous Python experience to robot movement using SPIKE Prime's motor_pair module. Each activity builds on previous concepts while introducing fundamental programming concepts.

## Activity 1: "First Steps with Motor Control"

**Learning Focus:** 
- Program entry point and structure
- Basic motor pairing and movement
- Print statements and string concatenation

```python
# My First SPIKE Prime Robot Program

import motor_pair
from hub import port
import runloop

# ===== MOTOR SETUP =====
# The pair() function connects two motors so they work together
# Parameters:
#   1. PAIR_1: This is a constant that identifies the pair
#   2. port.C: The port where your left motor is connected
#   3. port.D: The port where your right motor is connected
print("Setting up motors...")
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

async def main():
    # In Python, we use print() to show messages
    print("Robot starting in 3 seconds...")
    await runloop.sleep_ms(3000)  # Wait 3 seconds
    
    # ===== FORWARD MOVEMENT =====
    # The move() function makes both motors move together
    # Parameters:
    #   1. motor_pair.PAIR_1: Which motor pair to use
    #   2. 0: Steering (0 = straight, 100 = right, -100 = left)
    #   3. velocity=300: How fast to move (degrees per second)
    print("Moving forward...")
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=300)
    await runloop.sleep_ms(2000)  # Run for 2 seconds
    motor_pair.stop(motor_pair.PAIR_1)
    
    # ===== BACKWARD MOVEMENT =====
    # For backward motion, we use a negative velocity
    print("Moving backward...")
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=-300)
    await runloop.sleep_ms(2000)  # Run for 2 seconds
    motor_pair.stop(motor_pair.PAIR_1)
    
    # We can combine text and converted numbers in print statements
    speed = 300
    print("Finished moving at speed " + str(speed) + " degrees per second")

# This line is the entry point - it tells Python where to start
runloop.run(main())
```

**Group Activity & Challenges:**
1. Build a simple robot with two motors connected to ports C and D
2. Identify the entry point of the program and experiment with speeds
3. Make the robot move forward for 3 seconds and backward for 1 second
4. Add new print statements that combine text and numbers

## Activity 2: "Precision Movements and Control Flow"

**Learning Focus:** 
- Using move_for_degrees for precise distance control
- Understanding async/await and runloop
- If statements and variables

```python
# SPIKE Prime Precision Movement

import motor_pair
from hub import port
import runloop

# ===== VARIABLES =====
wheel_diameter = 2.0   # Diameter of wheels in inches
speed = 300            # Speed in degrees per second
movement_type = "precise"  # Can be "precise" or "timed"

# ===== MOTOR SETUP =====
print("Setting up motors...")
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

# ===== UNDERSTANDING TURN CALCULATIONS =====
'''

How Turn Angle Math Works:

When a robot turns in place, the wheels follow a circular path. Here's how we calculate
the wheel rotations needed for a specific turn angle:

1. Finding the Arc Length:
   - The WHEEL_BASE (4.5") is the distance between wheels
   - For a full 360° turn, each wheel travels a distance of π × WHEEL_BASE
   - For any angle, we use: arc_length = (angle/360) × π × WHEEL_BASE
   
   Example for 90° turn:
   - arc_length = (90/360) × π × 4.5
   - arc_length ≈ 3.53 inches

2. Converting Arc Length to Wheel Rotations:
   - Each wheel has diameter of 2.0", so circumference = π × 2.0 ≈ 6.28 inches
   - Number of rotations = arc_length / wheel_circumference
   - Degrees = rotations × 360
   
   Example for 90° turn:
   - rotations = 3.53/6.28 ≈ 0.56 rotations
   - degrees = 0.56 × 360 ≈ 202 degrees

Visual representation:
    ┌──────────4.5"──────────┐
    │                        │
    │         Robot          │
    │                        │
    └────────────────────────┘
           ↻90°

To make the robot turn:
- Right turn: Left wheel forward, Right wheel backward
- Left turn: Right wheel forward, Left wheel backward
'''

# ===== MATH HELPER =====
'''
How Distance to Degrees Math works:

When a wheel moves 1 rotation, it moves by a distance of it's circumference
wheel_circumference = pi * wheel_diameter_inches

Now, let's find out how many times we want the wheel to move depending on the distance we want to travel
wheel_rotations = distance_inches / wheel_cirumference

1 rotation is 360 degrees, now let's figure out degrees from rotations
degrees = wheel_rotations * 360
'''
def calculate_degrees(distance_inches):
    wheel_circumference = 3.14159 * wheel_diameter  # Distance per rotation
    rotations = distance_inches / wheel_circumference  # Number of rotations needed
    degrees = rotations * 360  # Convert rotations to degrees
    return int(degrees)  # Return as a whole number

async def main():
    print("SPIKE Prime Movement Example")
    await runloop.sleep_ms(1000)  # Wait 1 second before starting
    
    # Use an if statement to decide which movement type to use
    if movement_type == "precise":
        # ===== PRECISE DISTANCE MOVEMENT =====
        print("Moving forward exactly 4 inches...")
        distance = 4  # 4 inches
        degrees = calculate_degrees(distance)
        
        # The await means "wait until this exact movement is complete"
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, 0, velocity=speed)
        print("Precise forward movement complete!")
        
    else:
        # ===== TIMED MOVEMENT =====
        print("Using timed movement instead...")
        motor_pair.move(motor_pair.PAIR_1, 0, velocity=speed)
        await runloop.sleep_ms(1000)  # Run for 1 second
        motor_pair.stop(motor_pair.PAIR_1)
        print("Timed movement complete!")
    
    # ===== BACKWARD MOVEMENT =====
    print("Moving backward exactly 6 inches...")
    distance = 6  # 6 inches
    degrees = calculate_degrees(distance)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, 0, velocity=-speed)

# Start the program
runloop.run(main())
```

**Group Activity & Challenges:**
1. Measure your robot's wheel diameter and update the variable
2. Change the movement_type variable to "timed" and observe the difference
3. Create a square pattern using precise movements
4. Add an if statement to check if speed is greater than 200

## Activity 3: "Tank Turns and Loops"

**Learning Focus:** 
- Tank turning with move_tank and move_tank_for_degrees
- For loops for repeated actions
- Boolean values and operators

```python
# SPIKE Prime Tank Turns and Loops

import motor_pair
from hub import port
import runloop

# ===== VARIABLES AND CONSTANTS =====
WHEEL_DIAMETER = 2.0    # Wheel diameter in inches
WHEEL_BASE = 4.5        # Distance between wheels in inches
PI = 3.14159

MOVE_SPEED = 300        # Regular movement speed
TURN_SPEED = 100        # Lower speed for more accurate turns
draw_square = True      # Boolean value (True or False)
number_of_sides = 4     # Number of sides for our shape

# ===== MOTOR SETUP =====
print("Setting up motors...")
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

# ===== UNDERSTANDING TURN CALCULATIONS =====
'''
How Turn Angle Math Works:

When a robot turns in place, the wheels follow a circular path. Here's how we calculate
the wheel rotations needed for a specific turn angle:

1. Finding the Arc Length:
   - The WHEEL_BASE (4.5") is the distance between wheels
   - For a full 360° turn, each wheel travels a distance of π × WHEEL_BASE
   - For any angle, we use: arc_length = (angle/360) × π × WHEEL_BASE
   
   Example for 90° turn:
   - arc_length = (90/360) × π × 4.5
   - arc_length ≈ 3.53 inches

2. Converting Arc Length to Wheel Rotations:
   - Each wheel has diameter of 2.0", so circumference = π × 2.0 ≈ 6.28 inches
   - Number of rotations = arc_length / wheel_circumference
   - Degrees = rotations × 360
   
   Example for 90° turn:
   - rotations = 3.53/6.28 ≈ 0.56 rotations
   - degrees = 0.56 × 360 ≈ 202 degrees

Visual representation:
    ┌──────────4.5"──────────┐
    │                        │
    │         Robot          │
    │                        │
    └────────────────────────┘
           ↻90°

To make the robot turn:
- Right turn: Left wheel forward, Right wheel backward
- Left turn: Right wheel forward, Left wheel backward
'''

# ===== HELPER FUNCTIONS =====
def calculate_distance_degrees(distance_inches):
    """Convert a distance to motor rotation degrees"""
    wheel_circumference = PI * WHEEL_DIAMETER
    degrees = (distance_inches / wheel_circumference) * 360
    return int(degrees)

def calculate_turn_degrees(angle):
    """Calculate wheel rotation needed for a specific turn angle"""
    arc_length = (angle / 360) * PI * WHEEL_BASE
    wheel_circumference = PI * WHEEL_DIAMETER
    degrees = (arc_length / wheel_circumference) * 360
    return int(degrees)

async def main():
    print("SPIKE Prime Tank Turns and Loops Example")
    await runloop.sleep_ms(1000)
    
    # ===== TANK TURNING DEMONSTRATION =====
    # Turn right (left wheel forward, right wheel backward)
    print("Turning right using tank steering...")
    motor_pair.move_tank(motor_pair.PAIR_1, TURN_SPEED, -TURN_SPEED)
    await runloop.sleep_ms(1500)  # Turn for 1.5 seconds
    motor_pair.stop(motor_pair.PAIR_1)
    
    # ===== PRECISE TANK TURNING =====
    print("Demonstrating precise 90-degree turn...")
    turn_angle = 90
    wheel_degrees = calculate_turn_degrees(turn_angle)
    
    # This await means "wait until this precise turn is complete"
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, wheel_degrees, TURN_SPEED, -TURN_SPEED)
    
    # ===== USING LOOPS TO DRAW SHAPES =====
    if draw_square:
        print("Drawing a square with " + str(number_of_sides) + " sides...")
        total_rotation = 0
        
        for i in range(number_of_sides):
            print("Drawing side " + str(i+1) + " of " + str(number_of_sides))
            
            # Move forward for one side of the square
            forward_inches = 6  # 6 inch side length
            forward_degrees = calculate_distance_degrees(forward_inches)
            await motor_pair.move_for_degrees(motor_pair.PAIR_1, forward_degrees, 0, velocity=MOVE_SPEED)
            
            # Turn right 90 degrees
            turn_angle = 90  # For a square, each turn is 90 degrees
            turn_degrees = calculate_turn_degrees(turn_angle)
            await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, turn_degrees, TURN_SPEED, -TURN_SPEED)
            
            # Add this turn to our total rotation
            total_rotation += turn_angle
        
        # Check if we've completed a full 360-degree rotation
        if total_rotation == 360:
            print("Perfect! We made a complete 360-degree turn.")

# Start the program
runloop.run(main())
```

**Group Activity & Challenges:**
1. Run the program and observe the tank turns and precise 90-degree turns
2. Change the program to draw a triangle (3 sides with 120-degree turns)
3. Modify the draw_square variable to False and observe what happens
4. Create a program that turns in 45-degree increments using a loop

## Activity 4: "Combined Movements and Functions"

**Learning Focus:** 
- Creating reusable movement functions
- Combining different movement types
- Understanding function parameters

```python
# SPIKE Prime Movement Library

import motor_pair
from hub import port
import runloop

# ===== CONSTANTS =====
WHEEL_DIAMETER = 2.0      # Wheel diameter in inches
WHEEL_BASE = 4.5          # Distance between wheels in inches
PI = 3.14159
DEFAULT_SPEED = 300      # Default movement speed
PAIR = motor_pair.PAIR_1 # Which motor pair to use
LEFT_PORT = port.C       # Left motor port
RIGHT_PORT = port.D      # Right motor port

# Setup tracking
is_setup_done = False

# ===== SETUP FUNCTION =====
def setup():
    """Set up the motor pair if not already done"""
    global is_setup_done
    
    if is_setup_done:
        return
    
    print("Setting up motors...")
    motor_pair.pair(PAIR, LEFT_PORT, RIGHT_PORT)
    is_setup_done = True

# ===== MOVEMENT HELPER FUNCTIONS =====
def calculate_distance_degrees(distance_inches):
    """Calculate motor degrees for a given distance"""
    wheel_circumference = PI * WHEEL_DIAMETER
    degrees = (distance_inches / wheel_circumference) * 360
    return int(degrees)

def calculate_turn_degrees(angle):
    """Calculate motor degrees for a given turn angle"""
    arc_length = (angle / 360) * PI * WHEEL_BASE
    wheel_circumference = PI * WHEEL_DIAMETER
    degrees = (arc_length / wheel_circumference) * 360
    return int(degrees)

# ===== MOVEMENT FUNCTIONS =====
async def move_straight(distance_inches, speed=DEFAULT_SPEED):
    """Move the robot straight for an exact distance
    
    Parameters:
        distance_inches: Distance to move (positive=forward, negative=backward)
        speed: Motor speed in degrees per second (default=300)
    """
    # Make sure motors are set up
    setup()
    
    # Check if we're going forward or backward
    direction = 1
    if distance_inches < 0:
        direction = -1
        distance_inches = abs(distance_inches)  # Make distance positive for calculation
    
    # Calculate degrees and move
    degrees = calculate_distance_degrees(distance_inches)
    print("Moving " + ("forward" if direction > 0 else "backward") + " " + str(distance_inches) + " inches")
    await motor_pair.move_for_degrees(PAIR, degrees, 0, velocity=speed * direction)

async def turn(angle, speed=DEFAULT_SPEED // 3):
    """Turn the robot by a specific angle
    
    Parameters:
        angle: Angle to turn in degrees (positive=right, negative=left)
        speed: Motor speed in degrees per second (default=100)
    """
    # Make sure motors are set up
    setup()
    
    # Check if we're turning right or left
    direction = 1
    if angle < 0:
        direction = -1
        angle = abs(angle)  # Make angle positive for calculation
    
    # Calculate degrees and turn
    degrees = calculate_turn_degrees(angle)
    print("Turning " + ("right" if direction > 0 else "left") + " " + str(angle) + " degrees")
    
    if direction > 0:  # Right turn
        await motor_pair.move_tank_for_degrees(PAIR, degrees, speed, -speed)
    else:  # Left turn
        await motor_pair.move_tank_for_degrees(PAIR, degrees, -speed, speed)

async def drive_square(side_length_inches=6, pause_ms=300):
    """Drive in a square pattern"""
    for i in range(4):
        await move_straight(side_length_inches)
        await runloop.sleep_ms(pause_ms)
        await turn(90)
        await runloop.sleep_ms(pause_ms)

async def drive_polygon(sides=3, side_length_inches=6, pause_ms=300):
    """Drive in a polygon pattern with any number of sides"""
    # Calculate the turn angle based on number of sides
    turn_angle = 360 / sides
    
    for i in range(sides):
        await move_straight(side_length_inches)
        await runloop.sleep_ms(pause_ms)
        await turn(turn_angle)
        await runloop.sleep_ms(pause_ms)

# ===== MAIN PROGRAM =====
async def main():
    print("SPIKE Prime Movement Library Demo")
    await runloop.sleep_ms(1000)
    
    # Move forward and backward with our helper function
    await move_straight(8)    # Forward 8 inches
    await runloop.sleep_ms(1000)
    await move_straight(-8)   # Backward 8 inches
    await runloop.sleep_ms(1000)
    
    # Turn right and left with our helper function
    await turn(90)            # Right 90 degrees
    await runloop.sleep_ms(1000)
    await turn(-90)           # Left 90 degrees
    await runloop.sleep_ms(1000)
    
    # Draw a square using our square function
    print("Drawing a square...")
    await drive_square(side_length_inches=6)
    await runloop.sleep_ms(1000)
    
    # Draw a triangle using our polygon function
    print("Drawing a triangle...")
    await drive_polygon(sides=3, side_length_inches=6)

# Start the program
runloop.run(main())
```

**Group Activity & Challenges:**
1. Notice how each complex movement is built from simpler functions
2. Create a zigzag pattern using the move_straight and turn functions
3. Make the robot draw a pentagon (5 sides) using drive_polygon
4. Create a function that makes the robot move in a spiral pattern

## Activity 5: "Advanced Movements and Challenges"

**Learning Focus:** 
- Combining precise movements to create complex patterns
- Understanding program structure
- Problem-solving and debugging strategies

```python
# SPIKE Prime Advanced Movements

import motor_pair
from hub import port
import runloop

# ===== CONFIGURATION =====
WHEEL_DIAMETER = 2.0      # Wheel diameter in inches
WHEEL_BASE = 4.5          # Distance between wheels in inches
DEFAULT_SPEED = 300       # Default forward/backward speed
TURN_SPEED = 100          # Default turning speed (slower for accuracy)
LEFT_PORT = port.C        # Left motor port
RIGHT_PORT = port.D       # Right motor port
PAIR = motor_pair.PAIR_1  # Motor pair identifier

# Flag to track if setup is complete
is_setup_done = False

# ===== UTILITY FUNCTIONS =====
def setup():
    """Set up the motor pair if not already done"""
    global is_setup_done
    
    if is_setup_done:
        return
    
    print("Setting up motors...")
    motor_pair.pair(PAIR, LEFT_PORT, RIGHT_PORT)
    is_setup_done = True

def calculate_distance_degrees(distance_inches):
    """Convert distance to wheel rotation degrees"""
    PI = 3.14159
    wheel_circumference = PI * WHEEL_DIAMETER
    degrees = (distance_inches / wheel_circumference) * 360
    return int(degrees)

def calculate_turn_degrees(angle):
    """Convert angle to wheel rotation degrees for turning"""
    PI = 3.14159
    arc_length = (angle / 360) * PI * WHEEL_BASE
    wheel_circumference = PI * WHEEL_DIAMETER
    degrees = (arc_length / wheel_circumference) * 360
    return int(degrees)

# ===== BASIC MOVEMENT FUNCTIONS =====
async def move_straight(distance_inches, speed=None):
    """Move the robot straight for an exact distance"""
    setup()
    
    # If speed not specified, use the default
    if speed is None:
        speed = DEFAULT_SPEED
    
    # Determine if we're going forward or backward
    direction = 1
    if distance_inches < 0:
        direction = -1
        distance_inches = abs(distance_inches)
    
    # Calculate and execute the movement
    degrees = calculate_distance_degrees(distance_inches)
    print("Moving " + ("forward" if direction > 0 else "backward") + " " + str(distance_inches) + " inches")
    await motor_pair.move_for_degrees(PAIR, degrees, 0, velocity=speed * direction)

async def turn(angle, speed=None):
    """Turn the robot by a specific angle"""
    setup()
    
    # If speed not specified, use the turning default
    if speed is None:
        speed = TURN_SPEED
    
    # Determine if we're turning right or left
    direction = 1
    if angle < 0:
        direction = -1
        angle = abs(angle)
    
    # Calculate and execute the turn
    degrees = calculate_turn_degrees(angle)
    print("Turning " + ("right" if direction > 0 else "left") + " " + str(angle) + " degrees")
    
    if direction > 0:  # Right turn
        await motor_pair.move_tank_for_degrees(PAIR, degrees, speed, -speed)
    else:  # Left turn
        await motor_pair.move_tank_for_degrees(PAIR, degrees, -speed, speed)

# ===== PATTERN FUNCTIONS =====
async def drive_square(side_length=6, speed=None):
    """Drive in a square pattern"""
    for i in range(4):
        await move_straight(side_length, speed)
        await runloop.sleep_ms(300)
        await turn(90)
        await runloop.sleep_ms(300)

async def drive_polygon(sides=3, side_length=6, speed=None):
    """Drive in a polygon pattern with any number of sides"""
    if sides < 3:
        print("Error: A polygon must have at least 3 sides")
        return
    
    # Calculate turn angle for the polygon
    turn_angle = 360 / sides
    
    for i in range(sides):
        await move_straight(side_length, speed)
        await runloop.sleep_ms(300)
        await turn(turn_angle)
        await runloop.sleep_ms(300)

async def drive_zigzag(length=4, width=2, count=4, speed=None):
    """Drive in a zigzag pattern"""
    for i in range(count):
        # Forward movement
        await move_straight(length, speed)
        
        # Turn based on whether we're on an odd or even count
        if i % 2 == 0:
            await turn(90)
            await move_straight(width, speed)
            await turn(90)
        else:
            await turn(-90)
            await move_straight(width, speed)
            await turn(-90)

# ===== MAIN PROGRAM =====
async def main():
    print("SPIKE Prime Advanced Movement Challenges")
    
    # Choose which pattern to run by uncommenting one of these lines:
    
    # Basic patterns
    # await drive_square(side_length=6)
    # await drive_polygon(sides=5, side_length=4)  # Pentagon
    
    # Advanced patterns
    await drive_zigzag(length=4, width=2, count=4)

# Start the program
runloop.run(main())
```

**Group Activity & Final Challenges:**
1. Run the program and observe the zigzag pattern
2. Create a sequence that makes the robot:
   - Draw a square
   - Turn 45 degrees
   - Draw another square
3. Design your own robot "dance" routine combining different movements
4. Implement a "figure-eight" pattern using the functions provided

## Advanced Activity: "Accurate Turning with Sensors"

**Learning Focus:**
- Using motion sensors for precise turns
- Understanding closed-loop control
- Implementing correction mechanisms

This activity introduces a more advanced approach to turning using the motion sensor for feedback. We'll explore this in three phases, each building on the previous one.

### Phase 1: Basic Tank Turns

```python
# Basic Tank Turns with SPIKE Prime

import motor_pair
from hub import port
import runloop

# Motor setup (using ports C and D)
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

async def main():
    print("Phase 1: Basic Tank Turns")
    await runloop.sleep_ms(1000)
    
    # Turn right for 2 seconds
    print("Turning right...")
    motor_pair.move_tank(motor_pair.PAIR_1, 100, -100)  # Right wheel forward, left backward
    await runloop.sleep_ms(2000)
    motor_pair.stop(motor_pair.PAIR_1)
    
    await runloop.sleep_ms(1000)
    
    # Turn left for 2 seconds
    print("Turning left...")
    motor_pair.move_tank(motor_pair.PAIR_1, -100, 100)  # Left wheel forward, right backward
    await runloop.sleep_ms(2000)
    motor_pair.stop(motor_pair.PAIR_1)

runloop.run(main())
```

### Phase 2: Turn Angle Calculations

```python
# Turn Angle Calculations with SPIKE Prime

import motor_pair
from hub import port
import motion_sensor
import runloop
import math

# Constants (in millimeters and degrees)
WHEEL_DIAMETER_MM = 50.8    # 2 inches = 50.8mm
WHEEL_BASE_MM = 114.3       # 4.5 inches = 114.3mm
TURN_SPEED = 100           # Slower speed for more accurate turns

# Motor setup
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

def calculate_turn_degrees(angle):
    """Calculate motor degrees needed for a turn angle"""
    # Arc length for the turn
    arc_length_mm = (abs(angle) / 360) * math.pi * WHEEL_BASE_MM
    
    # Convert to wheel rotations
    wheel_circumference = math.pi * WHEEL_DIAMETER_MM
    wheel_rotations = arc_length_mm / wheel_circumference
    motor_degrees = wheel_rotations * 360
    
    return int(motor_degrees)

async def turn_robot(target_angle):
    """Turn robot by specified angle using calculations"""
    print(f"Turning to {target_angle} degrees...")
    
    # Calculate required motor movement
    motor_degrees = calculate_turn_degrees(target_angle)
    
    # Determine turn direction
    if target_angle > 0:  # Turn right
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1, 
            motor_degrees,
            TURN_SPEED, 
            -TURN_SPEED
        )
    else:  # Turn left
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1, 
            motor_degrees,
            -TURN_SPEED, 
            TURN_SPEED
        )

async def main():
    print("Phase 2: Turn Angle Calculations")
    await runloop.sleep_ms(1000)
    
    # Reset yaw angle to 0
    motion_sensor.reset_yaw(0)
    
    # Try some turns
    await turn_robot(90)   # Turn right 90 degrees
    print(f"Current yaw: {motion_sensor.tilt_angles()[0]}")
    await runloop.sleep_ms(1000)
    
    await turn_robot(-45)  # Turn left 45 degrees
    print(f"Current yaw: {motion_sensor.tilt_angles()[0]}")

runloop.run(main())
```

### Phase 3: Sensor-Based Correction

```python
# Precise Turns with Sensor Feedback and Initial Calculation

import motor_pair
from hub import port
import motion_sensor
import runloop
import math

# Constants
WHEEL_DIAMETER_MM = 50.8    # 2 inches = 50.8mm
WHEEL_BASE_MM = 114.3       # 4.5 inches = 114.3mm
TURN_SPEED = 100           # Base turning speed
MIN_SPEED = 30            # Minimum speed for small corrections
TOLERANCE = 2             # Acceptable error in degrees
MAX_ATTEMPTS = 3          # Maximum correction attempts

# Motor setup
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

def calculate_turn_degrees(angle):
    """Calculate motor degrees needed for a turn angle"""
    # Arc length for the turn
    arc_length_mm = (abs(angle) / 360) * math.pi * WHEEL_BASE_MM
    
    # Convert to wheel rotations
    wheel_circumference = math.pi * WHEEL_DIAMETER_MM
    wheel_rotations = arc_length_mm / wheel_circumference
    motor_degrees = wheel_rotations * 360
    
    return int(motor_degrees)

def get_current_angle():
    """Get current yaw angle from motion sensor"""
    return motion_sensor.tilt_angles()[0]

async def make_correction(target_angle, attempts=0):
    """Make small corrections using sensor feedback"""
    if attempts >= MAX_ATTEMPTS:
        print("Max correction attempts reached")
        return
    
    current_angle = get_current_angle()
    angle_error = target_angle - current_angle
    
    # If we're within tolerance, we're done
    if abs(angle_error) <= TOLERANCE:
        print(f"Target reached: {current_angle}°")
        return
    
    print(f"Correction attempt {attempts + 1}: From {current_angle}° to {target_angle}°")
    
    # Calculate turn speed based on error (slower for small corrections)
    turn_speed = max(MIN_SPEED, min(abs(angle_error), TURN_SPEED // 2))
    
    # Turn in the appropriate direction
    if angle_error > 0:  # Need to turn right
        motor_pair.move_tank(motor_pair.PAIR_1, turn_speed, -turn_speed)
    else:  # Need to turn left
        motor_pair.move_tank(motor_pair.PAIR_1, -turn_speed, turn_speed)
    
    # Keep turning until we reach target (or get close)
    while abs(target_angle - get_current_angle()) > TOLERANCE:
        await runloop.sleep_ms(10)
    
    # Stop motors
    motor_pair.stop(motor_pair.PAIR_1)
    
    # Check if we need another correction
    await runloop.sleep_ms(500)  # Wait for settling
    final_angle = get_current_angle()
    
    if abs(target_angle - final_angle) > TOLERANCE:
        print(f"Still off by {target_angle - final_angle}°")
        await make_correction(target_angle, attempts + 1)

async def turn_to_angle(target_angle):
    """Turn to exact angle using initial calculation and sensor correction"""
    print(f"Turning to {target_angle} degrees...")
    
    # First, calculate and perform the initial turn
    motor_degrees = calculate_turn_degrees(target_angle)
    
    # Perform the initial turn
    if target_angle > 0:  # Turn right
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1, 
            motor_degrees,
            TURN_SPEED, 
            -TURN_SPEED
        )
    else:  # Turn left
        await motor_pair.move_tank_for_degrees(
            motor_pair.PAIR_1, 
            motor_degrees,
            -TURN_SPEED, 
            TURN_SPEED
        )
    
    # Wait for the turn to settle
    await runloop.sleep_ms(500)
    
    # Get current angle and check if we need corrections
    current_angle = get_current_angle()
    if abs(target_angle - current_angle) > TOLERANCE:
        print(f"Initial turn completed. Off by {target_angle - current_angle}°")
        await make_correction(target_angle)
    else:
        print(f"Perfect initial turn! At {current_angle}°")

async def main():
    print("Phase 3: Precise Turns with Calculation and Correction")
    await runloop.sleep_ms(1000)
    
    # Reset yaw angle to 0
    motion_sensor.reset_yaw(0)
    
    # Try some precise turns
    await turn_to_angle(90)    # Turn right to 90°
    await runloop.sleep_ms(1000)
    
    await turn_to_angle(-45)   # Turn left to -45°
    await runloop.sleep_ms(1000)
    
    await turn_to_angle(0)     # Return to starting position

runloop.run(main())
```

**Group Activity & Challenges:**
1. Compare the accuracy of turns between Phase 1 and Phase 3
2. Experiment with different TOLERANCE and MIN_SPEED values
3. Create a sequence of turns that draws a star pattern
4. Add print statements to track the number of correction attempts needed
5. Modify the code to use different speeds for initial turns vs corrections

## Teaching Tips

- **Code First, Explain Later:** Let students see code working before diving into details
- **Hands-On Learning:** Every concept should be immediately tried on robots
- **Build Complexity Gradually:** Start with single movements before complex patterns
- **Visual Aids:** Use diagrams to explain wheel rotation calculations
- **Debugging Practice:** Intentionally introduce small errors for students to find and fix
- **Collaborative Problem-Solving:** Have students work in pairs to solve challenges

## Assessment Ideas

- **Movement Accuracy:** How precisely can students program specific distances?
- **Pattern Completion:** Can students create complex patterns like spirals?
- **Code Modification:** How well can students adapt example code for new purposes?
- **Peer Teaching:** Can students explain concepts to each other?
- **Final Challenge:** Navigate an obstacle course combining all learned techniques 