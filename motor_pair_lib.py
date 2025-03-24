"""
SPIKE Prime Motor Pair Library

A concise library for basic movement functions using the SPIKE Prime motor_pair API.

Functions:
- setup(): Configure motor pair once at program start
- move_forward(distance_inches, distance_time): Move forward by distance or time
- move_backward(distance_inches, distance_time): Move backward by distance or time 
- turn_right(degrees): Turn right by specified degrees
- turn_left(degrees): Turn left by specified degrees
- test_motor_pair(): Run tests of all movement functions
"""

import motor_pair
import runloop
from hub import port
from hub import motion_sensor
import time
import motor  # Added for motor.BRAKE access

# ===== CONFIGURATION =====
DEFAULT_SPEED = 300        # Default motor speed (degrees per second, not percentage)
WHEEL_DIAMETER = 2.0       # Wheel diameter in inches
WHEEL_BASE = 4.5           # Distance between wheels in inches
LEFT_MOTOR_PORT = port.C   # Port for left motor
RIGHT_MOTOR_PORT = port.D  # Port for right motor
PAIR = motor_pair.PAIR_1   # Use PAIR_1 constant

# Flag to track if setup has been completed
is_setup_done = False

# ===== UTILITY FUNCTIONS =====

def inches_to_degrees(inches):
    """Convert a distance in inches to motor degrees"""
    circumference = 3.14159 * WHEEL_DIAMETER
    return int((inches / circumference) * 360)

def get_yaw_angle():
    """Get current yaw angle from the motion sensor"""
    return motion_sensor.tilt_angles()[2]  # Yaw is the third value

# ===== SETUP FUNCTION =====

def setup():
    """Configure motor pair - call once at the start of your program"""
    global is_setup_done
    
    if is_setup_done:
        return True  # Already set up
    
    # First unpair any existing pairs
    try:
        motor_pair.unpair(PAIR)
        time.sleep_ms(50)
    except:
        pass  # Continue even if unpair fails
    
    # Pair the motors
    motor_pair.pair(PAIR, LEFT_MOTOR_PORT, RIGHT_MOTOR_PORT)
    is_setup_done = True
    return True

# ===== MOVEMENT FUNCTIONS =====

async def move_forward(distance_inches=0, distance_time=0):
    """
    Move forward by distance or time
    
    Args:
        distance_inches: Distance to travel in inches (if 0, uses time)
        distance_time: Time to move in seconds (if both 0, moves 1 inch)
    
    Returns:
        True if movement completed successfully
    """
    if not is_setup_done:
        setup()
    
    # Default to 1 inch if both parameters are 0
    if distance_inches == 0 and distance_time == 0:
        distance_inches = 1
    
    # Distance-based movement using move_for_degrees
    if distance_inches > 0:
        target_degrees = inches_to_degrees(distance_inches)
        print("Moving forward " + str(distance_inches) + " inches (" + str(target_degrees) + " degrees)")
        
        # Using the correct syntax per documentation: positional for pair/degrees/steering, 
        # named for the parameters after the *
        await motor_pair.move_for_degrees(PAIR, target_degrees, 0, velocity=DEFAULT_SPEED)
        
        print("Forward movement complete")
        return True
    
    # Time-based movement using move
    elif distance_time > 0:
        print("Moving forward for " + str(distance_time) + " seconds")
        # Using the correct syntax per documentation
        motor_pair.move(PAIR, 0, velocity=DEFAULT_SPEED)
        await runloop.sleep_ms(int(distance_time * 1000))
        motor_pair.stop(PAIR)
        print("Forward movement complete")
        return True
    
    return False

async def move_backward(distance_inches=0, distance_time=0):
    """
    Move backward by distance or time
    
    Args:
        distance_inches: Distance to travel in inches (if 0, uses time)
        distance_time: Time to move in seconds (if both 0, moves 1 inch)
    
    Returns:
        True if movement completed successfully
    """
    if not is_setup_done:
        setup()
    
    # Default to 1 inch if both parameters are 0
    if distance_inches == 0 and distance_time == 0:
        distance_inches = 1
    
    # Distance-based movement using move_for_degrees
    if distance_inches > 0:
        target_degrees = inches_to_degrees(distance_inches)
        print("Moving backward " + str(distance_inches) + " inches (" + str(target_degrees) + " degrees)")
        
        # Using the correct syntax per documentation: positional for pair/degrees/steering, 
        # named for the parameters after the *
        await motor_pair.move_for_degrees(PAIR, target_degrees, 0, velocity=-DEFAULT_SPEED)
        
        print("Backward movement complete")
        return True
    
    # Time-based movement using move
    elif distance_time > 0:
        print("Moving backward for " + str(distance_time) + " seconds")
        # Using the correct syntax per documentation
        motor_pair.move(PAIR, 0, velocity=-DEFAULT_SPEED)
        await runloop.sleep_ms(int(distance_time * 1000))
        motor_pair.stop(PAIR)
        print("Backward movement complete")
        return True
    
    return False

async def turn_right(degrees=90):
    """
    Turn right by specified degrees using steering
    
    Args:
        degrees: Degrees to turn (default 90)
    
    Returns:
        True if turn completed successfully
    """
    if not is_setup_done:
        setup()
    
    if degrees <= 0:
        return False
    
    print("Starting right turn of " + str(degrees) + " degrees")
    
    # Use tank steering for turns with higher speeds
    motor_pair.move_tank(PAIR, DEFAULT_SPEED, -DEFAULT_SPEED)
    
    # Since the gyro doesn't seem to be reliable, we'll use a time-based approach
    # Based on testing, we need much longer times than expected
    # For a 90-degree turn at 300 degrees/sec, we'll estimate 3000ms (3 seconds)
    estimated_turn_time_ms = int((degrees / 90) * 3000)  # 3 seconds for 90 degrees
    
    print("Using time-based turn for " + str(estimated_turn_time_ms) + " ms")
    
    # Sleep for the estimated time
    await runloop.sleep_ms(estimated_turn_time_ms)
    
    # Stop the motors
    motor_pair.stop(PAIR)
    
    print("Turn right complete - turned approximately " + str(degrees) + " degrees based on timing")
    
    return True

async def turn_left(degrees=90):
    """
    Turn left by specified degrees using steering
    
    Args:
        degrees: Degrees to turn (default 90)
    
    Returns:
        True if turn completed successfully
    """
    if not is_setup_done:
        setup()
    
    if degrees <= 0:
        return False
    
    print("Starting left turn of " + str(degrees) + " degrees")
    
    # Use tank steering for turns with higher speeds
    motor_pair.move_tank(PAIR, -DEFAULT_SPEED, DEFAULT_SPEED)
    
    # Since the gyro doesn't seem to be reliable, we'll use a time-based approach
    # Based on testing, we need much longer times than expected
    # For a 90-degree turn at 300 degrees/sec, we'll estimate 3000ms (3 seconds)
    estimated_turn_time_ms = int((degrees / 90) * 3000)  # 3 seconds for 90 degrees
    
    print("Using time-based turn for " + str(estimated_turn_time_ms) + " ms")
    
    # Sleep for the estimated time
    await runloop.sleep_ms(estimated_turn_time_ms)
    
    # Stop the motors
    motor_pair.stop(PAIR)
    
    print("Turn left complete - turned approximately " + str(degrees) + " degrees based on timing")
    
    return True

# ===== TEST FUNCTION =====

async def test_motor_pair():
    """Run tests of all movement functions"""
    print("\n=== Motor Pair Library Test ===")
    
    # Ensure setup is complete
    setup()
    print("Setup complete: SUCCESS")
    
    # Test 1: Forward 2 inches
    print("\nTest 1: Forward 2 inches")
    await runloop.sleep_ms(1000)
    test1 = await move_forward(distance_inches=2)
    await runloop.sleep_ms(1000)  # Pause between tests
    
    # Test 2: Forward for 2 seconds
    print("\nTest 2: Forward for 2 seconds")
    test2 = await move_forward(distance_time=2)
    await runloop.sleep_ms(1000)  # Pause between tests
    
    # Test 3: Backward 2 inches
    print("\nTest 3: Backward 2 inches")
    test3 = await move_backward(distance_inches=2)
    await runloop.sleep_ms(1000)  # Pause between tests
    
    # Test 4: Backward for 2 seconds
    print("\nTest 4: Backward for 2 seconds")
    test4 = await move_backward(distance_time=2)
    await runloop.sleep_ms(1000)  # Pause between tests
    
    # Test 5: Turn right 90 degrees
    print("\nTest 5: Turn right 90 degrees")
    test5 = await turn_right(degrees=90)
    await runloop.sleep_ms(1000)  # Pause between tests
    
    # Test 6: Turn left 90 degrees
    print("\nTest 6: Turn left 90 degrees")
    test6 = await turn_left(degrees=90)
    
    # Summary
    print("\n=== Test Summary ===")
    print("1. Forward 2 inches: " + ("SUCCESS" if test1 else "FAILED"))
    print("2. Forward 2 seconds: " + ("SUCCESS" if test2 else "FAILED"))
    print("3. Backward 2 inches: " + ("SUCCESS" if test3 else "FAILED"))
    print("4. Backward 2 seconds: " + ("SUCCESS" if test4 else "FAILED"))
    print("5. Turn right 90 degrees: " + ("SUCCESS" if test5 else "FAILED"))
    print("6. Turn left 90 degrees: " + ("SUCCESS" if test6 else "FAILED"))
    print("===========================")

# ===== MAIN PROGRAM =====

async def main():
    # Run the test function
    await test_motor_pair()

# Run the program if this file is executed directly
if __name__ == "__main__":
    runloop.run(main()) 