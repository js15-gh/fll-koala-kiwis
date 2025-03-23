"""
SPIKE Prime Motor Pair Straight Movement Module

This module provides functions for moving a Spike Prime robot in a straight line
using motor_pair API with gyro corrections.

Multiple API variants are supported:
1. SPIKE Hub API: 
   - Using predefined PAIR constants: motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
   - Using numeric IDs as fallback: motor_pair.pair(1, port.A, port.B)

2. SPIKE Education API: 
   - MotorPair class: motor_pair.MotorPair('A', 'B')
   - String port identifiers: motor_pair.pair('A', 'B')

The code automatically detects and uses the appropriate API for your SPIKE Prime firmware.

SPIKE Prime Motor Pair API Reference:
- motor_pair.pair(motor_pair.PAIR_1, port.A, port.B): Creates a motor pair
- motor_pair.move_for_degrees(PAIR, steering, speed, degrees): Moves for specified degrees
- motor_pair.move_tank(PAIR, left_speed, right_speed): Moves with tank steering
- motor_pair.move(PAIR, steering, speed): Moves with differential steering
- motor_pair.stop(PAIR): Stops the motor pair

Usage:
1. Upload this file to your SPIKE Prime
2. Run the program to test motor pair movement
3. The program will first test API compatibility, then run movement tests

You can modify the config variables at the top of the file to match your robot's setup.

Reference API docs:
- https://spike.legoeducation.com/essential/help/lls-help-python#lls-help-python-spm

Author: AI Assistant
Created for: LEGO SPIKE Prime robots
"""

import motor_pair
import motor
import runloop
from hub import port
from hub import motion_sensor
import sys
import time

# Print version information for debugging
print("\n=== SPIKE Prime System Information ===")
print("MicroPython version: " + sys.version)
try:
    print("Implementation: " + sys.implementation._machine)
except:
    print("Implementation info not available")

# ===== CONFIGURATION =====
# These can be adjusted based on your robot and preferences
DEFAULT_SPEED = 30         # Default motor speed (percentage 0-100)
DEFAULT_STEERING = 0       # 0 is straight, -100 is full left, +100 is full right
WHEEL_DIAMETER = 2.0       # Wheel diameter in inches
LEFT_MOTOR_PORT = port.C   # Port for left motor
RIGHT_MOTOR_PORT = port.D  # Port for right motor
# Use the predefined pair constants instead of numeric IDs
try:
    # Check if PAIR constants are available
    if hasattr(motor_pair, 'PAIR_1'):
        PAIR = motor_pair.PAIR_1  # Use the predefined pair constant
        print("Using predefined motor_pair.PAIR_1 constant")
    else:
        PAIR = 1  # Fallback to numeric ID if constants not available
        print("Predefined PAIR constants not found, using numeric ID: 1")
except Exception as e:
    PAIR = 1  # Fallback to numeric ID if constants not available
    print("Error checking for PAIR constants: " + str(e) + ", using numeric ID: 1")

# ===== UTILITY FUNCTIONS =====

def inches_to_degrees(inches, wheel_diameter=WHEEL_DIAMETER):
    """Convert a distance in inches to motor degrees based on wheel diameter"""
    circumference = 3.14159 * wheel_diameter  # Calculate wheel circumference
    degrees = (inches / circumference) * 360  # Convert to degrees
    return int(degrees)  # Return as integer

def get_yaw_angle():
    """Get current yaw angle from the motion sensor"""
    try:
        angles = motion_sensor.tilt_angles()
        return angles[2]  # Yaw is the third value in the tuple
    except Exception as e:
        print("Error reading yaw angle: " + str(e))
        return 0  # Return 0 if can't read yaw

# ===== MOTOR PAIR SETUP =====

def setup_motor_pair_spike_education():
    """Configure the motor pair using the SPIKE Education API format
    
    This uses the format documented at:
    https://spike.legoeducation.com/essential/help/lls-help-python#lls-help-python-spm
    """
    print("Attempting to setup motor pair using SPIKE Education API format...")
    try:
        # In SPIKE Education, motor_pair may be imported directly or through a different import
        # Some versions use from spike import MotorPair
        
        # Check if the module has a MotorPair class attribute
        if hasattr(motor_pair, "MotorPair"):
            # Get port letters
            left_port_letter = get_port_letter(LEFT_MOTOR_PORT)
            right_port_letter = get_port_letter(RIGHT_MOTOR_PORT)
            
            if not left_port_letter or not right_port_letter:
                print("Could not determine port letters")
                return False
            
            print("Using ports: " + left_port_letter + " (left) and " + right_port_letter + " (right)")
            
            # Create a MotorPair object using the correct ports
            global motor_pair_obj
            motor_pair_obj = motor_pair.MotorPair(left_port_letter, right_port_letter)
            print("Created motor_pair using MotorPair class format")
            return True
        else:
            # Try using string port letters with the older motor_pair.pair method
            left_port_letter = get_port_letter(LEFT_MOTOR_PORT)
            right_port_letter = get_port_letter(RIGHT_MOTOR_PORT)
            
            if not left_port_letter or not right_port_letter:
                print("Could not determine port letters")
                return False
            
            print("Using ports: " + left_port_letter + " (left) and " + right_port_letter + " (right)")
            
            # Try with string port letters
            motor_pair.pair(left_port_letter, right_port_letter)
            print("Paired motors using port letters: " + left_port_letter + ", " + right_port_letter)
            return True
    except Exception as e:
        print("Error setting up motor pair with SPIKE Education format: " + str(e))
        return False

def get_port_letter(port_obj):
    """Convert a port object to its letter representation"""
    if port_obj == port.A: return "A"
    elif port_obj == port.B: return "B"
    elif port_obj == port.C: return "C"
    elif port_obj == port.D: return "D"
    elif port_obj == port.E: return "E"
    elif port_obj == port.F: return "F"
    else: return ""

def setup_motor_pair():
    """Configure the motor pair for movement - tries multiple methods"""
    try:
        # First try to unpair any existing pairs to avoid "already assigned" errors
        try:
            # Try to unpair all pairs
            if hasattr(motor_pair, 'unpair'):
                print("Unpairing any existing motor pairs...")
                motor_pair.unpair(PAIR)  # Unpair the specific pair we want to use
                time.sleep_ms(50)  # Use time.sleep_ms here instead of await
        except Exception as e:
            print("Note: Unpair attempt: " + str(e))
            # Continue even if unpair fails
        
        # First try the standard hub module format with predefined PAIR constant
        print("Attempting to setup motor pair using standard SPIKE method...")
        try:
            # Try with the official SPIKE syntax
            motor_pair.pair(PAIR, LEFT_MOTOR_PORT, RIGHT_MOTOR_PORT)
            print("Motor pair successfully configured with PAIR: " + str(PAIR))
            return True
        except TypeError as e:
            # If that fails with a TypeError, try alternative approaches
            print("First pairing method failed: " + str(e))
            
            # Try with other predefined pair constants if available
            if hasattr(motor_pair, 'PAIR_2'):
                try:
                    print("Trying with PAIR_2...")
                    motor_pair.pair(motor_pair.PAIR_2, LEFT_MOTOR_PORT, RIGHT_MOTOR_PORT)
                    print("Pairing with PAIR_2 successful")
                    return True
                except Exception as e2:
                    print("PAIR_2 attempt failed: " + str(e2))
            
            try:
                # Try an alternative pairing method that might be available
                print("Trying alternative pairing method...")
                # Some versions use different parameter order or don't use a pair ID
                motor_pair.pair(LEFT_MOTOR_PORT, RIGHT_MOTOR_PORT)
                print("Alternative pairing successful")
                return True
            except Exception as e2:
                print("Alternative pairing also failed: " + str(e2))
                
                # Try the SPIKE Education format
                if setup_motor_pair_spike_education():
                    return True
                    
                # As a last resort, try with just a single parameter - the pair ID
                try:
                    print("Attempting fallback pairing method...")
                    # Some versions might auto-detect ports or use default ports
                    motor_pair.pair(PAIR)
                    print("Fallback pairing successful")
                    return True
                except Exception as e3:
                    print("All pairing methods failed. Try manual motor control instead.")
                    return False
    except Exception as e:
        print("Error setting up motor pair: " + str(e))
        
        # Try SPIKE Education format as a last resort
        if setup_motor_pair_spike_education():
            return True
        
        return False

# Initialize global variable for SPIKE Education MotorPair object (if created)
motor_pair_obj = None

def is_using_education_api():
    """Check if we're using the SPIKE Education API (MotorPair class)"""
    return motor_pair_obj is not None

def stop_pair():
    """Stop the motor pair using the appropriate method"""
    if is_using_education_api():
        try:
            # Try to use the Education API object
            motor_pair_obj.stop()
            print("Motor pair stopped (Education API)")
            return
        except Exception as e:
            print("Error with Education API stop: " + str(e))
    
    # Fall back to standard API
    try:
        # Try the standard stop method first with the PAIR constant
        motor_pair.stop(PAIR)
        print("Motor pair stopped")
    except Exception as e:
        print("Error with stop(PAIR): " + str(e))
        try:
            # Try without the pair ID parameter
            motor_pair.stop()
            print("Motor pair stopped (without ID)")
        except Exception as e2:
            print("All stop methods failed: " + str(e2))
            # Last resort - try direct motor control
            try:
                motor.stop(LEFT_MOTOR_PORT)
                motor.stop(RIGHT_MOTOR_PORT)
                print("Motors stopped with direct control")
            except Exception as e3:
                print("All stop methods failed. Motors may still be running.")

# ===== MOVEMENT FUNCTIONS =====

async def move_straight_simple(distance_inches=6, speed=DEFAULT_SPEED):
    """
    Move straight for a specific distance using motor_pair without gyro correction
    This uses direct motor control since move_for_degrees doesn't work correctly
    """
    print("Starting simple straight movement...")
    
    # Convert distance to degrees
    target_degrees = inches_to_degrees(distance_inches)
    
    try:
        print("Moving " + str(distance_inches) + " inches (" + str(target_degrees) + " degrees)")
        
        # Use direct motor control since it worked in the logs
        print("Using direct motor control...")
        motor.run_for_degrees(LEFT_MOTOR_PORT, target_degrees, speed)
        motor.run_for_degrees(RIGHT_MOTOR_PORT, target_degrees, speed)
        print("Direct motor control complete")
        
        print("Movement complete")
        return True
    except Exception as e:
        print("Error during movement: " + str(e))
        # Try stopping individual motors as a fallback
        try:
            motor.stop(LEFT_MOTOR_PORT)
            motor.stop(RIGHT_MOTOR_PORT)
            print("Individual motors stopped as fallback")
        except:
            pass
        return False

async def move_straight_with_gyro(distance_inches=6, speed=DEFAULT_SPEED, max_iterations=500):
    """
    Move straight for a specific distance using iteration-based movement with gyro correction
    
    This uses a counter-based approach rather than time tracking, since time()
    is not available on this SPIKE Prime firmware.
    
    Args:
        distance_inches: Distance to travel in inches
        speed: Motor speed (0-100)
        max_iterations: Maximum number of iterations before stopping (safety timeout)
    """
    print("Starting gyro-guided straight movement...")
    
    # Calculate estimated iterations based on distance and speed
    # This is an approximation that may need adjustment for your specific robot
    # At speed 30, about 15 iterations per inch seems reasonable (with 20ms delay per iteration)
    iterations_per_inch = 15 * (30.0 / speed)  # Adjust for different speeds
    estimated_iterations = int(distance_inches * iterations_per_inch)
    print("Distance: " + str(distance_inches) + " inches")
    print("Estimated iterations: " + str(estimated_iterations))
    
    # Reset orientation reference
    motion_sensor.reset_yaw()
    await runloop.sleep_ms(100)  # Short delay for sensor to stabilize
    initial_yaw = get_yaw_angle()
    print("Initial yaw: " + str(initial_yaw))
    
    # Flag to track if we're using tank mode or not
    using_tank_mode = True
    
    try:
        # PID controller parameters
        kp = 1.5    # Proportional gain - how strongly to react to current error
        
        # Start the motors - try tank mode first
        print("Starting motors...")
        try:
            # Try with pair ID - this method worked in the logs
            motor_pair.move_tank(PAIR, speed, speed)
            print("move_tank with pair ID successful")
        except Exception as e:
            print("move_tank with pair ID failed: " + str(e))
            try:
                # Try without pair ID
                motor_pair.move_tank(speed, speed)
                print("move_tank without pair ID successful")
            except Exception as e2:
                print("move_tank methods failed: " + str(e2))
                # Fall back to direct motor control
                motor.run(LEFT_MOTOR_PORT, speed)
                motor.run(RIGHT_MOTOR_PORT, speed)
                print("Direct motor control used as last resort")
                using_tank_mode = False
        
        # Variables for iteration tracking
        iterations = 0
        print_interval = 10  # Print status every 10 iterations
        
        # Run until we reach estimated iterations or max safety limit
        while iterations < estimated_iterations and iterations < max_iterations:
            iterations += 1
            
            # Print progress periodically
            if iterations % print_interval == 0:
                progress_percent = int((iterations / estimated_iterations) * 100)
                print("Progress: iteration " + str(iterations) + " / " + str(estimated_iterations) + 
                      " (" + str(min(100, progress_percent)) + "%)")
            
            # Get current yaw for correction
            current_yaw = get_yaw_angle()
            error = current_yaw - initial_yaw
            
            # Only apply corrections if error is significant
            if abs(error) > 1:
                # Calculate steering correction based on proportional control
                steering = -int(error * kp)
                
                # Keep steering within valid range (-100 to 100)
                steering = max(-100, min(100, steering))
                
                # Calculate modified speeds based on error
                left_speed = max(10, min(100, speed - steering))
                right_speed = max(10, min(100, speed + steering))
                
                if iterations % 10 == 0:  # Only print every 10 iterations to reduce spam
                    print("Yaw: " + str(error) + ", Correction: L=" + str(left_speed) + ", R=" + str(right_speed))
                
                # Apply correction using the appropriate method
                if using_tank_mode:
                    try:
                        # Try with pair ID - this works according to logs
                        motor_pair.move_tank(PAIR, left_speed, right_speed)
                    except Exception:
                        # Fall back to individual motor control
                        motor.run(LEFT_MOTOR_PORT, left_speed)
                        motor.run(RIGHT_MOTOR_PORT, right_speed)
                else:
                    # Direct motor control mode
                    motor.run(LEFT_MOTOR_PORT, left_speed)
                    motor.run(RIGHT_MOTOR_PORT, right_speed)
            
            # Small delay to prevent overwhelming the CPU
            await runloop.sleep_ms(20)
        
        # Stop the motors
        try:
            # Try to stop using motor_pair
            if using_tank_mode:
                motor_pair.stop(PAIR)
            else:
                motor.stop(LEFT_MOTOR_PORT)
                motor.stop(RIGHT_MOTOR_PORT)
        except Exception:
            # Fallback to direct motor control
            try:
                motor.stop(LEFT_MOTOR_PORT)
                motor.stop(RIGHT_MOTOR_PORT)
            except:
                print("Failed to stop motors cleanly")
        
        final_yaw = get_yaw_angle()
        print("Final yaw: " + str(final_yaw) + " (drift: " + str(final_yaw - initial_yaw) + ")")
        
        timeout = iterations >= max_iterations
        print("Gyro-guided movement complete" + (" (timed out)" if timeout else ""))
        return not timeout
    except Exception as e:
        print("Error during gyro-guided movement: " + str(e))
        # Try stopping individual motors as a fallback
        try:
            motor.stop(LEFT_MOTOR_PORT)
            motor.stop(RIGHT_MOTOR_PORT)
            print("Individual motors stopped as fallback")
        except:
            pass
        return False

async def test_movement():
    """
    Test straight movement using both simple and gyro-guided methods
    """
    print("\n=== Motor Pair Movement Tests ===")
    
    # First test basic motor_pair functionality
    print("\n--- Testing Motor Pair Setup ---")
    # Print information about the motor ports and motion sensor
    print("Motor configuration:")
    print("- Left motor port: " + str(LEFT_MOTOR_PORT))
    print("- Right motor port: " + str(RIGHT_MOTOR_PORT))
    
    # Test motion sensor
    print("\nTesting motion sensor...")
    try:
        angles = motion_sensor.tilt_angles()
        print("Motion sensor tilt angles: " + str(angles))
        print("- Current yaw angle: " + str(angles[2]))
        
        # Reset yaw and check again
        motion_sensor.reset_yaw()
        await runloop.sleep_ms(100)  # Allow time for reset
        angles_after_reset = motion_sensor.tilt_angles()
        print("Tilt angles after yaw reset: " + str(angles_after_reset))
    except Exception as e:
        print("Error testing motion sensor: " + str(e))
    
    # Test motor_pair setup
    print("\nSetting up motor pair...")
    pair_success = setup_motor_pair()
    if not pair_success:
        print("CAUTION: Motor pair setup failed. Testing will continue with fallbacks.")
    
    # Test simple movement first (short distance)
    print("\n--- Testing Simple Straight Movement ---")
    print("Moving forward 3 inches without gyro correction...")
    success = await move_straight_simple(3, DEFAULT_SPEED)
    if success:
        print("Simple movement test succeeded")
        await runloop.sleep_ms(1000)  # Pause between tests
    else:
        print("Simple movement test failed")
        print("Skipping remaining tests due to basic movement failure")
        return
    
    # Test gyro-guided movement with different distances
    print("\n--- Testing Gyro-Guided Movement ---")
    
    # Small distance test
    print("\nTest 1: Short distance (3 inches)")
    small_success = await move_straight_with_gyro(3, DEFAULT_SPEED, max_iterations=250)
    if small_success:
        print("Short distance test succeeded")
        await runloop.sleep_ms(1000)  # Pause between tests
    else:
        print("Short distance test failed")
        print("Skipping remaining tests due to short distance failure")
        return
    
    # Medium distance test
    print("\nTest 2: Medium distance (6 inches)")
    medium_success = await move_straight_with_gyro(6, DEFAULT_SPEED, max_iterations=400)
    if medium_success:
        print("Medium distance test succeeded")
        await runloop.sleep_ms(1000)  # Pause between tests
    else:
        print("Medium distance test failed")
        print("Skipping remaining tests due to medium distance failure")
        return
    
    # Only proceed to longer distance if previous tests were successful
    print("\nTest 3: Longer distance (10 inches)")
    long_success = await move_straight_with_gyro(10, DEFAULT_SPEED, max_iterations=600)
    if long_success:
        print("Long distance test succeeded")
    else:
        print("Long distance test failed")
    
    # Final cleanup
    print("\n--- Test Complete ---")
    try:
        motor.stop(LEFT_MOTOR_PORT)
        motor.stop(RIGHT_MOTOR_PORT)
    except:
        pass
    
    # Summary of test results
    print("\n=== Test Summary ===")
    print("Motor pair setup: " + ("SUCCESS" if pair_success else "FAILED (used fallbacks)"))
    print("Simple movement: " + ("SUCCESS" if success else "FAILED"))
    print("Short gyro movement: " + ("SUCCESS" if small_success else "FAILED"))
    print("Medium gyro movement: " + ("SUCCESS" if medium_success else "FAILED"))
    print("Long gyro movement: " + ("SUCCESS" if long_success else "FAILED"))
    print("===============================")

async def test_motor_pair_api():
    """
    Test motor_pair API methods in isolation to identify compatibility issues
    """
    print("\n=== Testing Motor Pair API Compatibility ===")
    
    # Set up the motor pair
    print("Setting up motor pair...")
    pair_setup = setup_motor_pair()
    if not pair_setup:
        print("Failed to set up motor pair. API testing incomplete.")
        return False
    
    # Test for SPIKE Education API first
    print("\nChecking for SPIKE Education API...")
    if is_using_education_api():
        print("SPIKE Education API detected! Testing Education API methods...")
        
        # Test stop method
        print("\nTesting Education API stop method")
        try:
            motor_pair_obj.stop()
            print("Education API stop() - SUCCESS")
        except Exception as e:
            print("Education API stop() - FAILED: " + str(e))
        
        # Test move method
        print("\nTesting Education API move method")
        try:
            # Just attempt a very small movement (0.5 cm)
            motor_pair_obj.move(0.5, 'cm', 0, DEFAULT_SPEED)
            print("Education API move() - SUCCESS")
        except Exception as e:
            print("Education API move() - FAILED: " + str(e))
        
        # Test start_tank method
        print("\nTesting Education API start_tank method")
        try:
            motor_pair_obj.start_tank(DEFAULT_SPEED, DEFAULT_SPEED)
            print("Education API start_tank() - SUCCESS")
            await runloop.sleep_ms(500)  # Run for half a second
            motor_pair_obj.stop()
        except Exception as e:
            print("Education API start_tank() - FAILED: " + str(e))
        
        # Check if get_degrees_counted is available
        print("\nTesting if get_degrees_counted is available")
        try:
            position = motor_pair_obj.get_degrees_counted()
            print("Education API get_degrees_counted() - SUCCESS: " + str(position))
        except Exception as e:
            print("Education API get_degrees_counted() - FAILED: " + str(e))
    else:
        print("SPIKE Education API not detected, using standard API methods")
    
    # Test basic methods
    print("\nTesting basic motor_pair methods...")
    
    # Test 1: stop method
    print("\nTest 1: Testing stop method")
    try:
        motor_pair.stop(PAIR)
        print("stop(PAIR) - SUCCESS")
    except Exception as e:
        print("stop(PAIR) - FAILED: " + str(e))
        try:
            motor_pair.stop()
            print("stop() - SUCCESS")
        except Exception as e2:
            print("stop() - FAILED: " + str(e2))
    
    # Test 2: move_tank method with no arguments
    print("\nTest 2: Testing move_tank method")
    try:
        # Try to run for a brief moment (0.5 seconds)
        motor_pair.move_tank(PAIR, 30, 30)
        print("move_tank(PAIR, speed, speed) - SUCCESS")
        await runloop.sleep_ms(500)  # Run for half a second
        stop_pair()
    except Exception as e:
        print("move_tank(PAIR, speed, speed) - FAILED: " + str(e))
        try:
            motor_pair.move_tank(30, 30)
            print("move_tank(speed, speed) - SUCCESS")
            await runloop.sleep_ms(500)  # Run for half a second
            stop_pair()
        except Exception as e2:
            print("move_tank(speed, speed) - FAILED: " + str(e2))
    
    # Test 3: move method
    print("\nTest 3: Testing move method")
    try:
        motor_pair.move(PAIR, DEFAULT_STEERING, DEFAULT_SPEED)
        print("move(PAIR, steering, speed) - SUCCESS")
        await runloop.sleep_ms(500)  # Run for half a second
        stop_pair()
    except Exception as e:
        print("move(PAIR, steering, speed) - FAILED: " + str(e))
        try:
            motor_pair.move(DEFAULT_STEERING, DEFAULT_SPEED)
            print("move(steering, speed) - SUCCESS")
            await runloop.sleep_ms(500)  # Run for half a second
            stop_pair()
        except Exception as e2:
            print("move(steering, speed) - FAILED: " + str(e2))
    
    # Test 4: move_for_degrees method
    print("\nTest 4: Testing move_for_degrees method")
    try:
        motor_pair.move_for_degrees(PAIR, DEFAULT_STEERING, DEFAULT_SPEED, 360)
        print("move_for_degrees(PAIR, steering, speed, degrees) - SUCCESS")
    except Exception as e:
        print("move_for_degrees(PAIR, steering, speed, degrees) - FAILED: " + str(e))
        try:
            motor_pair.move_for_degrees(DEFAULT_STEERING, DEFAULT_SPEED, 360)
            print("move_for_degrees(steering, speed, degrees) - SUCCESS")
        except Exception as e2:
            print("move_for_degrees(steering, speed, degrees) - FAILED: " + str(e2))
    
    # Test 5: Testing reset_relative_position
    print("\nTest 5: Testing reset_relative_position method")
    try:
        motor_pair.reset_relative_position(PAIR, 0)
        print("reset_relative_position(PAIR, 0) - SUCCESS")
    except Exception as e:
        print("reset_relative_position(PAIR, 0) - FAILED: " + str(e))
        try:
            motor_pair.reset_relative_position(0)
            print("reset_relative_position(0) - SUCCESS")
        except Exception as e2:
            print("reset_relative_position(0) - FAILED: " + str(e2))
    
    # Test 6: Testing relative_position
    print("\nTest 6: Testing relative_position method")
    try:
        position = motor_pair.relative_position(PAIR)
        print("relative_position(PAIR) - SUCCESS: " + str(position))
    except Exception as e:
        print("relative_position(PAIR) - FAILED: " + str(e))
        try:
            position = motor_pair.relative_position()
            print("relative_position() - SUCCESS: " + str(position))
        except Exception as e2:
            print("relative_position() - FAILED: " + str(e2))
    
    # Test 7: Test direct motor control as fallback
    print("\nTest 7: Testing direct motor control (fallback)")
    try:
        motor.run(LEFT_MOTOR_PORT, DEFAULT_SPEED)
        motor.run(RIGHT_MOTOR_PORT, DEFAULT_SPEED)
        print("Direct motor control - SUCCESS")
        await runloop.sleep_ms(500)  # Run for half a second
        motor.stop(LEFT_MOTOR_PORT)
        motor.stop(RIGHT_MOTOR_PORT)
    except Exception as e:
        print("Direct motor control - FAILED: " + str(e))
    
    print("\nMotor pair API testing complete.")
    stop_pair()  # Make sure motors are stopped
    return True

async def move_education_api(distance_inches, speed=DEFAULT_SPEED):
    """Move using the SPIKE Education API MotorPair.move method"""
    if not is_using_education_api():
        print("Education API not available")
        return False
    
    try:
        print("Moving " + str(distance_inches) + " inches using Education API")
        # The Education API uses cm by default, so we need to convert
        distance_cm = distance_inches * 2.54
        
        # Call the move method from the Education API
        # move(amount, unit='cm', steering=0, speed=None)
        motor_pair_obj.move(distance_cm, 'cm', DEFAULT_STEERING, speed)
        print("Education API movement complete")
        return True
    except Exception as e:
        print("Error with Education API move: " + str(e))
        stop_pair()
        return False

async def move_tank_education_api(distance_inches, left_speed=DEFAULT_SPEED, right_speed=DEFAULT_SPEED):
    """Move using the SPIKE Education API MotorPair.move_tank method"""
    if not is_using_education_api():
        print("Education API not available")
        return False
    
    try:
        print("Moving " + str(distance_inches) + " inches using Education API tank mode")
        # The Education API uses cm by default, so we need to convert
        distance_cm = distance_inches * 2.54
        
        # Call the move_tank method from the Education API
        # move_tank(amount, unit='cm', left_speed=None, right_speed=None)
        motor_pair_obj.move_tank(distance_cm, 'cm', left_speed, right_speed)
        print("Education API tank movement complete")
        return True
    except Exception as e:
        print("Error with Education API move_tank: " + str(e))
        stop_pair()
        return False

async def main():
    """
    Main program entry point
    """
    print("\n===== SPIKE Prime Motor Pair Movement Program =====")
    print("Motor ports: Left=" + str(LEFT_MOTOR_PORT) + ", Right=" + str(RIGHT_MOTOR_PORT))
    print("Wheel diameter: " + str(WHEEL_DIAMETER) + " inches")
    print("Default speed: " + str(DEFAULT_SPEED) + "%")
    
    # Check for PAIR constants
    print("\nChecking for PAIR constants...")
    if hasattr(motor_pair, 'PAIR_1'):
        print("PAIR_1 constant found: " + str(motor_pair.PAIR_1))
    if hasattr(motor_pair, 'PAIR_2'):
        print("PAIR_2 constant found: " + str(motor_pair.PAIR_2))
    
    # Check if we can get motor_pair module information
    print("\nMotor Pair Module Information:")
    try:
        methods = [method for method in dir(motor_pair) if not method.startswith("_")]
        print("Available methods: " + str(methods))
        
        # Specifically check for the MotorPair class
        if hasattr(motor_pair, 'MotorPair'):
            print("\nMotorPair class detected (SPIKE Education API)")
            
            # Check available methods in MotorPair class
            motor_pair_methods = [method for method in dir(motor_pair.MotorPair) if not method.startswith("_")]
            print("MotorPair class methods: " + str(motor_pair_methods))
        else:
            print("\nMotorPair class not found (using standard Hub API)")
    except Exception as e:
        print("Error getting module info: " + str(e))
    
    # Offer user a choice via menu
    print("\nTest Menu:")
    print("1. Test motor_pair API compatibility")
    print("2. Run all movement tests")
    print("3. Test only simple movement (3 inches)")
    print("4. Test only gyro movement (3 inches)")
    print("5. Test only gyro movement (6 inches)")
    
    # For automatic execution, run the API test first, then the full test sequence
    print("\nRunning API compatibility test in 2 seconds...")
    await runloop.sleep_ms(2000)
    api_test_result = await test_motor_pair_api()
    
    if api_test_result:
        print("\nAPI test completed successfully. Running movement tests in 2 seconds...")
        await runloop.sleep_ms(2000)
        
        # Now run the appropriate test based on which API was successful
        if is_using_education_api():
            print("\n=== Testing with SPIKE Education API ===")
            print("Moving 3 inches using Education API...")
            
            success = await move_education_api(3, DEFAULT_SPEED)
            if success:
                print("SPIKE Education API movement successful!")
                
                # Now try a gyro movement
                print("\nTesting gyro-guided movement with Education API...")
                await runloop.sleep_ms(1000)
                gyro_success = await move_straight_with_gyro(3, DEFAULT_SPEED)
                if gyro_success:
                    print("Gyro-guided movement with Education API successful!")
                else:
                    print("Gyro-guided movement with Education API failed")
            else:
                print("SPIKE Education API movement failed")
                # Fall back to standard movement tests
                await test_movement()
        else:
            print("\n=== Testing with Standard Hub API ===")
            await test_movement()
    else:
        print("\nAPI test encountered issues. Movement tests may not work correctly.")
        print("Will attempt movement tests anyway in 3 seconds...")
        await runloop.sleep_ms(3000)
        await test_movement()
    
    print("\nProgram complete")

# Start the program
if __name__ == "__main__":
    runloop.run(main()) 