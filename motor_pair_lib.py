    """
    SPIKE Prime Motor Pair Library

    A concise library for basic movement functions using the SPIKE Prime motor_pair API.
    Based on learnings from testing different firmware versions.

    Functions:
    - setup(): Configure motor pair once at program start
    - move_forward(distance_inches, distance_time): Move forward by distance or time
    - move_backward(distance_inches, distance_time): Move backward by distance or time 
    - turn_right(degrees): Turn right by specified degrees
    - turn_left(degrees): Turn left by specified degrees
    - test_motor_pair(): Run tests of all movement functions

    Author: AI Assistant
    """

    import motor_pair
    import motor
    import runloop
    from hub import port
    from hub import motion_sensor
    import time

    # ===== CONFIGURATION =====
    DEFAULT_SPEED = 30         # Default motor speed (percentage 0-100)
    WHEEL_DIAMETER = 2.0       # Wheel diameter in inches
    WHEEL_BASE = 4.5           # Distance between wheels in inches (adjust for your robot)
    LEFT_MOTOR_PORT = port.C   # Port for left motor
    RIGHT_MOTOR_PORT = port.D  # Port for right motor

    # Determine appropriate PAIR constant
    try:
        if hasattr(motor_pair, 'PAIR_1'):
            PAIR = motor_pair.PAIR_1
        else:
            PAIR = 1  # Fallback to numeric ID
    except:
        PAIR = 1

    # Flag to track if setup has been completed
    is_setup_done = False
    using_tank_mode = True  # Track if tank mode is being used or direct motor control

    # ===== UTILITY FUNCTIONS =====

    def inches_to_degrees(inches):
        """Convert a distance in inches to motor degrees"""
        circumference = 3.14159 * WHEEL_DIAMETER
        return int((inches / circumference) * 360)

    def degrees_to_wheel_degrees(turn_degrees):
        """Convert turning degrees to wheel rotation degrees"""
        # Calculate wheel travel distance needed for turn
        # Each wheel needs to travel distance = (wheel_base * pi * turn_degrees / 360)
        wheel_travel = WHEEL_BASE * 3.14159 * turn_degrees / 360
        return inches_to_degrees(wheel_travel)

    def get_yaw_angle():
        """Get current yaw angle from the motion sensor"""
        try:
            return motion_sensor.tilt_angles()[2]  # Yaw is the third value
        except:
            return 0

    # ===== SETUP FUNCTION =====

    def setup():
        """Configure motor pair - call once at the start of your program"""
        global is_setup_done, using_tank_mode
        
        if is_setup_done:
            return True  # Already set up
        
        # First try to unpair any existing pairs
        try:
            if hasattr(motor_pair, 'unpair'):
                motor_pair.unpair(PAIR)  # Unpair the specific pair
                time.sleep_ms(50)
        except:
            pass  # Continue even if unpair fails
        
        # Try to pair the motors using the standard method
        try:
            motor_pair.pair(PAIR, LEFT_MOTOR_PORT, RIGHT_MOTOR_PORT)
            is_setup_done = True
            using_tank_mode = True
            return True
        except:
            # Try alternative pairing without PAIR ID
            try:
                motor_pair.pair(LEFT_MOTOR_PORT, RIGHT_MOTOR_PORT)
                is_setup_done = True
                using_tank_mode = True
                return True
            except:
                # Fallback to direct motor control
                is_setup_done = True
                using_tank_mode = False
                print("Using direct motor control as fallback")
                return False

    def stop_motors():
        """Stop all motors using the appropriate method"""
        if using_tank_mode:
            try:
                motor_pair.stop(PAIR)
            except:
                try:
                    motor_pair.stop()  # Try without PAIR parameter
                except:
                    # Fallback to direct control
                    motor.stop(LEFT_MOTOR_PORT)
                    motor.stop(RIGHT_MOTOR_PORT)
        else:
            # Direct motor control
            motor.stop(LEFT_MOTOR_PORT)
            motor.stop(RIGHT_MOTOR_PORT)

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
        
        # If using distance
        if distance_inches > 0:
            target_degrees = inches_to_degrees(distance_inches)
            print("Moving forward " + str(distance_inches) + " inches (" + str(target_degrees) + " degrees)")
            
            # Strategy 1: Try move_for_degrees (most precise if available)
            if using_tank_mode:
                try:
                    print("Attempting motor_pair.move_for_degrees...")
                    motor_pair.move_for_degrees(PAIR, 0, DEFAULT_SPEED, target_degrees)
                    print("move_for_degrees completed successfully")
                    return True
                except Exception as e:
                    print("move_for_degrees failed: " + str(e))
                    
                    # Strategy 2: Try direct motor control
                    try:
                        print("Trying direct motor.run_for_degrees...")
                        motor.run_for_degrees(LEFT_MOTOR_PORT, target_degrees, DEFAULT_SPEED)
                        motor.run_for_degrees(RIGHT_MOTOR_PORT, target_degrees, DEFAULT_SPEED)
                        print("Direct run_for_degrees completed")
                        return True
                    except Exception as e2:
                        print("Direct run_for_degrees failed: " + str(e2))
                        
                        # Strategy 3: Time-based fallback (convert distance to estimated time)
                        try:
                            print("Falling back to time-based movement...")
                            # Estimate time needed: inches / (speed_pct * max_speed_inch_per_sec)
                            # At 100% speed, robot moves roughly 8 inches per second - adjust for your robot
                            max_speed = 8.0  # inches per second at 100% speed
                            speed_factor = DEFAULT_SPEED / 100.0
                            estimated_time = distance_inches / (max_speed * speed_factor)
                            
                            print("Estimated time for " + str(distance_inches) + " inches: " + 
                                str(estimated_time) + " seconds")
                            
                            # Start motors for estimated time
                            if using_tank_mode:
                                try:
                                    motor_pair.move_tank(PAIR, DEFAULT_SPEED, DEFAULT_SPEED)
                                except:
                                    try:
                                        motor_pair.move_tank(DEFAULT_SPEED, DEFAULT_SPEED)
                                    except:
                                        motor.run(LEFT_MOTOR_PORT, DEFAULT_SPEED)
                                        motor.run(RIGHT_MOTOR_PORT, DEFAULT_SPEED)
                            else:
                                motor.run(LEFT_MOTOR_PORT, DEFAULT_SPEED)
                                motor.run(RIGHT_MOTOR_PORT, DEFAULT_SPEED)
                            
                            # Wait for the estimated time
                            ms_to_wait = int(estimated_time * 1000)
                            await runloop.sleep_ms(ms_to_wait)
                            
                            # Stop motors
                            stop_motors()
                            print("Time-based fallback movement completed")
                            return True
                        except Exception as e3:
                            print("All movement strategies failed: " + str(e3))
                            stop_motors()
                            return False
            else:
                # Using direct motor control
                try:
                    print("Using direct run_for_degrees...")
                    motor.run_for_degrees(LEFT_MOTOR_PORT, target_degrees, DEFAULT_SPEED)
                    motor.run_for_degrees(RIGHT_MOTOR_PORT, target_degrees, DEFAULT_SPEED)
                    print("Direct run_for_degrees completed")
                    return True
                except Exception as e:
                    print("Direct run_for_degrees failed: " + str(e))
                    
                    # Time-based fallback (same as above)
                    try:
                        print("Falling back to time-based movement...")
                        max_speed = 8.0  # inches per second at 100% speed
                        speed_factor = DEFAULT_SPEED / 100.0
                        estimated_time = distance_inches / (max_speed * speed_factor)
                        
                        print("Estimated time for " + str(distance_inches) + " inches: " + 
                            str(estimated_time) + " seconds")
                        
                        # Start motors for estimated time
                        motor.run(LEFT_MOTOR_PORT, DEFAULT_SPEED)
                        motor.run(RIGHT_MOTOR_PORT, DEFAULT_SPEED)
                        
                        # Wait for the estimated time
                        ms_to_wait = int(estimated_time * 1000)
                        await runloop.sleep_ms(ms_to_wait)
                        
                        # Stop motors
                        stop_motors()
                        print("Time-based fallback movement completed")
                        return True
                    except Exception as e2:
                        print("All movement strategies failed: " + str(e2))
                        stop_motors()
                        return False
        
        # If using time
        elif distance_time > 0:
            print("Moving forward for " + str(distance_time) + " seconds")
            # Start motors
            if using_tank_mode:
                try:
                    motor_pair.move_tank(PAIR, DEFAULT_SPEED, DEFAULT_SPEED)
                except:
                    try:
                        motor_pair.move_tank(DEFAULT_SPEED, DEFAULT_SPEED)
                    except:
                        motor.run(LEFT_MOTOR_PORT, DEFAULT_SPEED)
                        motor.run(RIGHT_MOTOR_PORT, DEFAULT_SPEED)
            else:
                motor.run(LEFT_MOTOR_PORT, DEFAULT_SPEED)
                motor.run(RIGHT_MOTOR_PORT, DEFAULT_SPEED)
            
            # Wait for the specified time
            ms_to_wait = int(distance_time * 1000)
            await runloop.sleep_ms(ms_to_wait)
            
            # Stop motors
            stop_motors()
            return True
        
        return False  # Should never reach here

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
        
        # If using distance
        if distance_inches > 0:
            target_degrees = inches_to_degrees(distance_inches)
            print("Moving backward " + str(distance_inches) + " inches (" + str(target_degrees) + " degrees)")
            
            # Strategy 1: Try move_for_degrees (most precise if available)
            if using_tank_mode:
                try:
                    print("Attempting motor_pair.move_for_degrees...")
                    motor_pair.move_for_degrees(PAIR, 0, -DEFAULT_SPEED, target_degrees)
                    print("move_for_degrees completed successfully")
                    return True
                except Exception as e:
                    print("move_for_degrees failed: " + str(e))
                    
                    # Strategy 2: Try direct motor control
                    try:
                        print("Trying direct motor.run_for_degrees...")
                        motor.run_for_degrees(LEFT_MOTOR_PORT, target_degrees, -DEFAULT_SPEED)
                        motor.run_for_degrees(RIGHT_MOTOR_PORT, target_degrees, -DEFAULT_SPEED)
                        print("Direct run_for_degrees completed")
                        return True
                    except Exception as e2:
                        print("Direct run_for_degrees failed: " + str(e2))
                        
                        # Strategy 3: Time-based fallback (convert distance to estimated time)
                        try:
                            print("Falling back to time-based movement...")
                            # Estimate time needed: inches / (speed_pct * max_speed_inch_per_sec)
                            # At 100% speed, robot moves roughly 8 inches per second - adjust for your robot
                            max_speed = 8.0  # inches per second at 100% speed
                            speed_factor = DEFAULT_SPEED / 100.0
                            estimated_time = distance_inches / (max_speed * speed_factor)
                            
                            print("Estimated time for " + str(distance_inches) + " inches: " + 
                                str(estimated_time) + " seconds")
                            
                            # Start motors for estimated time
                            if using_tank_mode:
                                try:
                                    motor_pair.move_tank(PAIR, -DEFAULT_SPEED, -DEFAULT_SPEED)
                                except:
                                    try:
                                        motor_pair.move_tank(-DEFAULT_SPEED, -DEFAULT_SPEED)
                                    except:
                                        motor.run(LEFT_MOTOR_PORT, -DEFAULT_SPEED)
                                        motor.run(RIGHT_MOTOR_PORT, -DEFAULT_SPEED)
                            else:
                                motor.run(LEFT_MOTOR_PORT, -DEFAULT_SPEED)
                                motor.run(RIGHT_MOTOR_PORT, -DEFAULT_SPEED)
                            
                            # Wait for the estimated time
                            ms_to_wait = int(estimated_time * 1000)
                            await runloop.sleep_ms(ms_to_wait)
                            
                            # Stop motors
                            stop_motors()
                            print("Time-based fallback movement completed")
                            return True
                        except Exception as e3:
                            print("All movement strategies failed: " + str(e3))
                            stop_motors()
                            return False
            else:
                # Using direct motor control
                try:
                    print("Using direct run_for_degrees...")
                    motor.run_for_degrees(LEFT_MOTOR_PORT, target_degrees, -DEFAULT_SPEED)
                    motor.run_for_degrees(RIGHT_MOTOR_PORT, target_degrees, -DEFAULT_SPEED)
                    print("Direct run_for_degrees completed")
                    return True
                except Exception as e:
                    print("Direct run_for_degrees failed: " + str(e))
                    
                    # Time-based fallback (same as above)
                    try:
                        print("Falling back to time-based movement...")
                        max_speed = 8.0  # inches per second at 100% speed
                        speed_factor = DEFAULT_SPEED / 100.0
                        estimated_time = distance_inches / (max_speed * speed_factor)
                        
                        print("Estimated time for " + str(distance_inches) + " inches: " + 
                            str(estimated_time) + " seconds")
                        
                        # Start motors for estimated time
                        motor.run(LEFT_MOTOR_PORT, -DEFAULT_SPEED)
                        motor.run(RIGHT_MOTOR_PORT, -DEFAULT_SPEED)
                        
                        # Wait for the estimated time
                        ms_to_wait = int(estimated_time * 1000)
                        await runloop.sleep_ms(ms_to_wait)
                        
                        # Stop motors
                        stop_motors()
                        print("Time-based fallback movement completed")
                        return True
                    except Exception as e2:
                        print("All movement strategies failed: " + str(e2))
                        stop_motors()
                        return False
        
        # If using time
        elif distance_time > 0:
            print("Moving backward for " + str(distance_time) + " seconds")
            # Start motors
            if using_tank_mode:
                try:
                    motor_pair.move_tank(PAIR, -DEFAULT_SPEED, -DEFAULT_SPEED)
                except:
                    try:
                        motor_pair.move_tank(-DEFAULT_SPEED, -DEFAULT_SPEED)
                    except:
                        motor.run(LEFT_MOTOR_PORT, -DEFAULT_SPEED)
                        motor.run(RIGHT_MOTOR_PORT, -DEFAULT_SPEED)
            else:
                motor.run(LEFT_MOTOR_PORT, -DEFAULT_SPEED)
                motor.run(RIGHT_MOTOR_PORT, -DEFAULT_SPEED)
            
            # Wait for the specified time
            ms_to_wait = int(distance_time * 1000)
            await runloop.sleep_ms(ms_to_wait)
            
            # Stop motors
            stop_motors()
            return True
        
        return False  # Should never reach here

    async def turn_right(degrees=90):
        """
        Turn right by specified degrees
        
        Args:
            degrees: Degrees to turn (default 90)
        
        Returns:
            True if turn completed successfully
        """
        if not is_setup_done:
            setup()
        
        if degrees <= 0:
            return False
        
        # Reset gyro for accurate measurements
        motion_sensor.reset_yaw()
        await runloop.sleep_ms(100)  # Stabilize
        initial_yaw = get_yaw_angle()
        target_yaw = initial_yaw - degrees  # Negative for right turn in our system
        
        # Calculate wheel rotation based on turn angle
        wheel_degrees = degrees_to_wheel_degrees(degrees)
        
        # Start turn based on available methods
        if using_tank_mode:
            try:
                # Tank steering with opposite wheel directions
                motor_pair.move_tank(PAIR, DEFAULT_SPEED, -DEFAULT_SPEED)
            except:
                try:
                    motor_pair.move_tank(DEFAULT_SPEED, -DEFAULT_SPEED)
                except:
                    # Fallback to direct control
                    motor.run(LEFT_MOTOR_PORT, DEFAULT_SPEED)
                    motor.run(RIGHT_MOTOR_PORT, -DEFAULT_SPEED)
        else:
            # Direct motor control
            motor.run(LEFT_MOTOR_PORT, DEFAULT_SPEED)
            motor.run(RIGHT_MOTOR_PORT, -DEFAULT_SPEED)
        
        # Monitor the turn and stop when target reached
        max_iterations = 300  # Safety limit
        iterations = 0
        
        while iterations < max_iterations:
            current_yaw = get_yaw_angle()
            
            # Print progress every 10 iterations
            if iterations % 10 == 0:
                print("Turning right: Current=" + str(current_yaw) + ", Target=" + str(target_yaw))
            
            # Check if we've reached the target angle (allowing for small error)
            if current_yaw <= target_yaw + 3:
                break
            
            iterations += 1
            await runloop.sleep_ms(20)
        
        # Stop the motors
        stop_motors()
        
        # Report success or timeout
        final_yaw = get_yaw_angle()
        print("Turn complete: Final=" + str(final_yaw) + ", Target=" + str(target_yaw) + ", Error=" + str(final_yaw-target_yaw))
        
        return iterations < max_iterations  # True if didn't time out

    async def turn_left(degrees=90):
        """
        Turn left by specified degrees
        
        Args:
            degrees: Degrees to turn (default 90)
        
        Returns:
            True if turn completed successfully
        """
        if not is_setup_done:
            setup()
        
        if degrees <= 0:
            return False
        
        # Reset gyro for accurate measurements
        motion_sensor.reset_yaw()
        await runloop.sleep_ms(100)  # Stabilize
        initial_yaw = get_yaw_angle()
        target_yaw = initial_yaw + degrees  # Positive for left turn in our system
        
        # Calculate wheel rotation based on turn angle
        wheel_degrees = degrees_to_wheel_degrees(degrees)
        
        # Start turn based on available methods
        if using_tank_mode:
            try:
                # Tank steering with opposite wheel directions
                motor_pair.move_tank(PAIR, -DEFAULT_SPEED, DEFAULT_SPEED)
            except:
                try:
                    motor_pair.move_tank(-DEFAULT_SPEED, DEFAULT_SPEED)
                except:
                    # Fallback to direct control
                    motor.run(LEFT_MOTOR_PORT, -DEFAULT_SPEED)
                    motor.run(RIGHT_MOTOR_PORT, DEFAULT_SPEED)
        else:
            # Direct motor control
            motor.run(LEFT_MOTOR_PORT, -DEFAULT_SPEED)
            motor.run(RIGHT_MOTOR_PORT, DEFAULT_SPEED)
        
        # Monitor the turn and stop when target reached
        max_iterations = 300  # Safety limit
        iterations = 0
        
        while iterations < max_iterations:
            current_yaw = get_yaw_angle()
            
            # Print progress every 10 iterations
            if iterations % 10 == 0:
                print("Turning left: Current=" + str(current_yaw) + ", Target=" + str(target_yaw))
            
            # Check if we've reached the target angle (allowing for small error)
            if current_yaw >= target_yaw - 3:
                break
            
            iterations += 1
            await runloop.sleep_ms(20)
        
        # Stop the motors
        stop_motors()
        
        # Report success or timeout
        final_yaw = get_yaw_angle()
        print("Turn complete: Final=" + str(final_yaw) + ", Target=" + str(target_yaw) + ", Error=" + str(final_yaw-target_yaw))
        
        return iterations < max_iterations  # True if didn't time out

    # ===== TEST FUNCTION =====

    async def test_motor_pair():
        """
        Run tests of all movement functions:
        1) Forward 2 inches
        2) Forward for 2 seconds
        3) Backward 2 inches
        4) Backward for 2 seconds
        5) Turn right 90 degrees
        6) Turn left 90 degrees
        """
        print("\n=== Motor Pair Library Test ===")
        
        # Ensure setup is complete
        success = setup()
        print("Setup complete: " + ("SUCCESS" if success else "USING FALLBACKS"))
        
        # Test 1: Forward 2 inches
        print("\nTest 1: Forward 2 inches")
        await runloop.sleep_ms(1000)
        test1 = await move_forward(distance_inches=2)
        print("Test 1 result: " + ("SUCCESS" if test1 else "FAILED"))
        await runloop.sleep_ms(1000)  # Pause between tests
        
        # Test 2: Forward for 2 seconds
        print("\nTest 2: Forward for 2 seconds")
        test2 = await move_forward(distance_time=2)
        print("Test 2 result: " + ("SUCCESS" if test2 else "FAILED"))
        await runloop.sleep_ms(1000)  # Pause between tests
        
        # Test 3: Backward 2 inches
        print("\nTest 3: Backward 2 inches")
        test3 = await move_backward(distance_inches=2)
        print("Test 3 result: " + ("SUCCESS" if test3 else "FAILED"))
        await runloop.sleep_ms(1000)  # Pause between tests
        
        # Test 4: Backward for 2 seconds
        print("\nTest 4: Backward for 2 seconds")
        test4 = await move_backward(distance_time=2)
        print("Test 4 result: " + ("SUCCESS" if test4 else "FAILED"))
        await runloop.sleep_ms(1000)  # Pause between tests
        
        # Test 5: Turn right 90 degrees
        print("\nTest 5: Turn right 90 degrees")
        test5 = await turn_right(degrees=90)
        print("Test 5 result: " + ("SUCCESS" if test5 else "FAILED"))
        await runloop.sleep_ms(1000)  # Pause between tests
        
        # Test 6: Turn left 90 degrees
        print("\nTest 6: Turn left 90 degrees")
        test6 = await turn_left(degrees=90)
        print("Test 6 result: " + ("SUCCESS" if test6 else "FAILED"))
        
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