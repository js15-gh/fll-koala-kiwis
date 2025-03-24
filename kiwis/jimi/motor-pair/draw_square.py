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