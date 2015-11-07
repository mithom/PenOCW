# From Car.py

# Oude ongebruikte functies

def go_straight_distance2(power, distance):
    global offset_A, offset_B, O, d
    print 'start go straight distance'
    calibrate()
    left_power = power
    right_power = power
    set_left(left_power)
    set_right(right_power)
    BrickPiUpdateValues()
    update_interval = 0.1
    pid_controller = PID.PID(5, 5, 5, 1, offset_A, offset_B, update_interval)
    last_update = 0
    average = 0
    print O, "omtrek"
    degree = (distance / O) * 360
    print degree, "degree"
    # counter = 0  # uitgecomment omdat niet nodig (eerst inwhile geset voor gebruikt
    # difference = 0
    while average < degree:
        print "while"
        average = ((BrickPi.Encoder[PORT_A] - offset_A) + (BrickPi.Encoder[PORT_B] - offset_B)) / 2
        difference = (BrickPi.Encoder[PORT_A] - offset_A) - (BrickPi.Encoder[PORT_B] - offset_B)
        pid_value = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
        if (time.time() - last_update) > update_interval:
            last_update = time.time()
            print "time to update our values"
            if pid_value < difference:
                # left_power -= int(abs(difference-pid_value))
                right_power += int(abs(difference - pid_value))
                set_left(power)
                set_right(right_power)
            elif pid_value > difference:
                left_power += int(abs(difference - pid_value))
                # right_power -= int(abs(difference-pid_value))
                set_left(left_power)
                set_right(power)
            else:
                set_left(power)
                set_right(power)
        print 'left: ' + str(left_power) + ", right: " + str(right_power)
        BrickPiUpdateValues()

def circle_test(power, duration):
    global offset_A, offset_B
    calibrate()
    main_power = 80
    left_power = main_power
    right_power = main_power
    set_motors(left_power,right_power)
    BrickPiUpdateValues()

    power_increase = (power-main_power)/(duration/2)
    step = 1

    start_time = time.time()
    update_interval = 0.01
    proportional_factor = 0
    derivative_factor = 0
    integral_factor = 5
    pid_controller = PID.PID(proportional_factor,derivative_factor, integral_factor, 1.2987, offset_A, offset_B, update_interval)
    last_update = time.time()
    with open('values.txt', 'w') as f:
        f.write('New PID --------')
        while (time.time() - start_time) < duration:
            if (time.time()-start_time) > step and main_power < power:
                left_power += power_increase
                right_power += power_increase
                main_power += power_increase
                step += 1
            if time.time() - start_time > 1:
                pid_controller.set_proportional(main_power/10)
            if time.time() - start_time > 3:
                pid_controller.set_derivative(15)
                pid_controller.set_integral(18)
            encoder_A = BrickPi.Encoder[PORT_A] - offset_A
            encoder_B = BrickPi.Encoder[PORT_B] - offset_B
            if encoder_B != 0:
                ratio = encoder_A / float(encoder_B)
            else:
                ratio = 1
            f.write(str(ratio) + ',')
            print 'Ratio: ', ratio
            pid_ratio = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
            print 'PID ratio: ', pid_ratio
            if (time.time() - last_update) > update_interval and (time.time()-start_time) > 1:
                last_update = time.time()
                right_power = int((2*main_power)/(pid_ratio+1))
                left_power = int(pid_ratio*right_power)
                set_motors(left_power, right_power)
            BrickPiUpdateValues()
        print BrickPi.Encoder[PORT_A]


def go_straight_duration(power, duration):
    global offset_A, offset_B
    calibrate()
    print 'start'
    left_power = power
    right_power = power
    set_left(left_power)
    set_right(right_power)
    BrickPiUpdateValues()
    start_time = time.time()
    update_interval = 0.01
    pid_controller = PID.PID(5, 5, 0, offset_A, offset_B, update_interval)
    last_update = 0
    # difference = 0  # uitgecomment omdat eerst geset in while, dus nog niet nodig
    # counter = 0
    with open('values.txt', 'w') as f:
        # f = open('values.txt','w')
        while (time.time() - start_time) < duration:
            difference = (BrickPi.Encoder[PORT_A] - offset_A) - (BrickPi.Encoder[PORT_B] - offset_B)
            f.write(str(difference) + ',')
            print "difference", difference
            pid_value = pid_controller.update(BrickPi.Encoder[PORT_A], BrickPi.Encoder[PORT_B])
            if (time.time() - last_update) > update_interval:
                last_update = time.time()
                if pid_value < difference:
                    # rechts sneller
                    # left_power -= abs(difference-pid_value)
                    right_power += int(abs(difference - pid_value))
                    set_left(power)
                    set_right(right_power)
                elif pid_value > difference:
                    # rechts sneller
                    left_power += int(abs(difference - pid_value))
                    # right_power += abs(difference-pid_value)power
                    set_left(left_power)
                    set_right(power)
                else:
                    set_left(power)
                    set_right(power)
            print 'left: ' + str(left_power) + ", right: " + str(right_power)
            BrickPiUpdateValues()
            # f.close()

"""
def brake():
    while(power>5):
        set_left(power-10)
        set_right(power-10)
        BrickPiUpdateValues()
        power -= 10
    set_left(0)
    set_right(0)
    BrickPiUpdateValues()
    power = 0"""

deviations_per_power = {50: 1.2, 100: 1.0}