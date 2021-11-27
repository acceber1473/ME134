### Daniel Ryaboshapka
### Rebecca Shen
### Robotics HW2: Analog Clock
### Contains test, thoughts, extra functions, and workflows used for the project


###############################################
####										###
####                IMPORTS                 ###
####										###
###############################################

import datetime
import argparse 
import datetime
from math import radians
# USED TO TEST FROM A NON-RPI MACHINE
try:
	import RPi.GPIO as GPIO
	import pca9685 as p
except Exception:
	pass

from time import sleep

###############################################
####										###
####      RESEARCHING SERVO LIBRARIES       ###
####										###
###############################################

# pi_servo_hat from sparkfun 
# import pi_servo_hat

# SPARKFUN TEST 
# https://github.com/sparkfun/PiServoHat_Py

# def test_run_hat():
# 	servo = pi_servo_hat.PiServoHat()

# 	if !servo.isConnected():
# 		print("The Qwiic PCA9685 device isn't connected to the system. Please check your connection")
# 		return

# 	mySensor.restart()
  
# 	# Test Run
# 	#########################################
# 	# Moves servo position to 0 degrees (1ms), Channel 0
# 	mySensor.move_servo_position(0, 0)

# 	# Pause 1 sec
# 	time.sleep(1)

# 	# Moves servo position to 90 degrees (2ms), Channel 0
# 	mySensor.move_servo_position(0, 90)

# from waveshare docs

###############################################
####										###
####            ARGUMENT PARSING            ###
####										###
###############################################

parser = argparse.ArgumentParser(description='Test servo')
parser.add_argument('-a', '--angle', type=int, help='"angle" for the servo to run')
parser.add_argument('-s', '--serv2', type=int, help='"angle" for servo 2')
parser.add_argument('-f', '--serv3', type=int, help='"angle" for servo 3')
parser.add_argument('-t', '--faster', type=int, help="go faster by the specified amount")
parser.add_argument('-d', '--demo', action="store_true", help="run predefined motor commands")
args = parser.parse_args()


###############################################
####										###
####            INITIALIZATION              ###
####										###
###############################################

pwm = p.PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

# left = 500
# right = 2500 

hour_spread   = 2000 / 12 
minute_spread = 2000 / 60

hour_servo   = 10 
minute_servo = 12 
second_servo = 15

###############################################
####										###
####                TESTING                 ###
####										###
###############################################
# prev = datetime.datetime.now()

# def get_next_second(prev):
# 	time = datetime.datetime.now()
# 	while time < prev + datetime.timedelta(seconds=1):
# 		time = datetime.datetime.now()
# 		sleep(.1)
# 		pass
# 	return time


# TESTING SERVOS WITH ARGUMENTS
# max clockwise 
# if not args.demo or not args.faster:
# 	if args.angle:
# 		pwm.setServoPulse(15, args.angle)
# 	if args.serv2:
# 		pwm.setServoPulse(12, args.serv2)
# 	if args.serv3:
# 		pwm.setServoPulse(10, args.serv3)
# else:

###############################################
####										###
####                  DEMO                  ###
####										###
###############################################



if args.faster:
	prev = datetime.datetime.now()
	while True:
		now = prev + datetime.timedelta(seconds=1)
		hour = now.hour % 12
		minute = now.minute
		seconds = now.second

		pwm.setServoPulse(hour_servo, 2500 - (hour * hour_spread))
		pwm.setServoPulse(minute_servo, 2500 - (minute * minute_spread))
		pwm.setServoPulse(second_servo, 2500 - (seconds * minute_spread))
		prev = now
		sleep(1/args.faster)
else:
	while True:
		# now = get_next_second(prev)
		now = datetime.datetime.now()
		hour = now.hour % 12
		minute = now.minute
		seconds = now.second

		# print(hour, minute, seconds)

		pwm.setServoPulse(hour_servo, 2500 - (hour * hour_spread))
		pwm.setServoPulse(minute_servo, 2500 - (minute * minute_spread))
		pwm.setServoPulse(second_servo, 2500 - (seconds * minute_spread))
		sleep(1)



###############################################
####										###
####            EXTRANEOUS CODE             ###
####										###
###############################################

	# run the servo to one end, send a small push with smaller servo,
	# rinse and repeat 

	# pwm.setServoPulse(3, 500)
	# time.sleep(1)
	# pwm.setServoPulse(3, 1390)
	# time.sleep(1)
	# pwm.setServoPulse(3, 2500)

#### END TEST ####

def time_to_angle_of_clock(time, rad=False):
	"""
	Converts digital time to degrees rotated from 12 (clockwise) for hours, minutes, and seconds

	Args
	----
	time : datetime object
	rad : boolean, if True, returns the list in radian form 

	Returns
	-------
	[hour_d, minute_d, second_d] : a 3 item list containing degrees of rotation for hours, minutes, and seconds 

	"""

	hours   = abs(time.hour - 12)
	minutes = time.minute
	seconds = time.second

	# print(f"{hours} {minutes} {seconds}")
	ret = [(hours / 12) * 360, (minutes / 60) * 360, (seconds / 60) * 360]
	if rad: 
		return [radians(i) for i in ret]

	return ret


### TESTS
# print(time_to_angle_of_clock(datetime.datetime.now()))


def time_to_servo_pulse(time, choice="hour", keep_alive=False, debug=False):
	"""
	Sends motor commands to the servo hat based on 
	viewing the hour, the minutes, or the seconds of the time specified

	Args
	----
	time       : datetime object, representing the time 
	choice     : a string that must be either ["hour", "minute", "second"], which changes the speed of visualization 
	keep_alive : boolean, if True, continues to send motor commands based on the time incrementing each second
	debug      : boolean, if True, sends debug statements to stdout

	Returns
	-------
	Nothing, side effects include motor commands sent to the servo hat

	"""
	raise NotImplementedError


# in between
# pwm.setServoPulse(0, 1500)

# max counterclockwise
# pwm.setServoPulse(0,2500)


# time.sleep(.02)
# pwm.setServoPulse(0, 1000)

# STANDARD TEST

# servo_pin = 17

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servo_pin, GPIO.OUT)
# servo = GPIO.PWM(servo_pin, 50)

# ## TEST SERVOS 
# servo.start(2.5)
# servo.ChangeDutyCycle(5)
# time.sleep(.5)
# servo.ChangeDutyCycle(10)


# ## CLEANUP SERVO AND GPIO PINS 

# serve.stop()
# GPIO.cleanup()



