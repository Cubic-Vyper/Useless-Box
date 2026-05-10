from machine import Pin, PWM
import time

# =====================================
# defin pins
# =====================================

toggle = Pin(1, Pin.IN, Pin.PULL_DOWN)

limit_sw = Pin(2, Pin.IN, Pin.PULL_UP)

touch = Pin(3, Pin.IN)

servo_pwm = PWM(Pin(0))
servo_pwm.freq(50)

# =====================================
# servo stuff
# =====================================

def angle_to_duty(degrees):
    pulse_us = 500 + (degrees / 180) * 1900  
    return int((pulse_us / 20000) * 65535)    

def move_servo(degrees):
    servo_pwm.duty_u16(angle_to_duty(degrees))

def servo_off():
    servo_pwm.duty_u16(0)

# servo positions

HOME = 90
FLIP = 45

move_servo(HOME)    
time.sleep(0.5)    
servo_off()     

#track where the arm is

arm_out = False


# =====================================
# main loop
# =====================================

while True:

    toggle_on   = toggle.value()   == 1   # true when flipped
    limit_hit   = limit_sw.value() == 0   # true when arm hits the limit switch
    secret_held = touch.value()    == 1   # true when finger is on TTP223

    #secret switch
    if toggle_on and secret_held:
        if arm_out:
            # pull arm in if out
            move_servo(HOME)
            time.sleep(0.4)
            servo_off()
            arm_out = False
        # end loop
        time.sleep(0.05)
        continue
    
    #cheack if toggle flipped
    if toggle_on and not arm_out:
        arm_out = True
        move_servo(FLIP) 

    #check if servo has flipped the switch

    if arm_out and limit_hit:
        servo_off()         # Stop dead — don't push against the wall
        time.sleep(0.1)     # Tiny pause before reversing
        move_servo(HOME)    # Pull arm back in
        time.sleep(0.5)     # Wait for it to reach HOME
        servo_off()         # Cut PWM again
        arm_out = False

    #check if the sevo stayed off 
    if arm_out and not toggle_on:
        move_servo(HOME)
        time.sleep(0.4)
        servo_off()
        arm_out = False

    # small pause between loops
    time.sleep(0.02)