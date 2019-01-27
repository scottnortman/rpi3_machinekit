#!/usr/bin/python2
# encoding: utf-8

###################################################################################################
#	File:	AdaHalPWM.py
#	Desc:	Lightweight machinekit HAL wrapper around the Adafruit BBIO PWM library
#	Date:	Jan 26 2019
#	Auth:	Scott Nortman, scott.nortman@gmail.com
#	Note:	Released under MIT open source license: https://opensource.org/licenses/MIT
#
#	For use with machinekit : http://www.machinekit.io/
#	
#	This class uses the Adafruit BBIO PWM library:
#		https://github.com/adafruit/adafruit-beaglebone-io-python
#
#	This implements a loadable machinekit HAL user module (non-realtime); example:
#
#	$ halrun
#	msgd:0 stopped
#	rtapi:0 stopped
#	rtapi_msgd command:  /usr/libexec/linuxcnc/rtapi_msgd --instance=0 --rtmsglevel=1 --usrmsglevel=1 --halsize=524288
#	rtapi_app command:  /usr/libexec/linuxcnc/rtapi_app_rt-preempt --instance=0
#	
#	halcmd: loadusr -Wn pwm ./AdaHalPWM.py -n pwm -u 10 -c P9_29 -f 1000 -p 0
#	Waiting for component 'pwm' to become ready.
#
#	halcmd: show pin
# 	Component Pins:
#   	Comp   Inst Type  Dir         Value  Name                                            Epsilon Flags  linked to:
#     		80        float IN              0  pwm.duty                                	0.000010	--l-
#     		80        bit   IN          FALSE  pwm.enable                              		--l-
#	
#	halcmd: setp pwm.enable 1
#	halcmd: setp pwm.duty 0.5 
#	

import sys
import argparse
import time

import hal
import Adafruit_BBIO.PWM as PWM


class AdaHalPWM( object ) :

	def __init__( self, name='', updateHz=1.0, channel='', freq=0.0, polarity=0 ) :

		assert( name != ''), ('[%s] is not a valid component name'%(name) )
		assert( channel != ''), ('[%s] is not a valid channel name'%(channel))
		assert( 0.0 <= freq ), ('[%f] out of range' % (freq) ) 
		assert( polarity==0 or polarity==1), ('[%d] polarity out of range'%(polarity) )
		assert( 0.1 <= updateHz <= 100.0 ), ('[%f] updateHz out of range' %(updateHz) )

		self._name = name
		self._channel = channel
		self._freq = freq
		self._polarity = polarity
		self._updateHz = updateHz

		# Create HAL component and pins
		self._component = hal.component( self._name )
		self._component.newpin('duty', hal.HAL_FLOAT, hal.HAL_IN ) #duty cycle input, 0 <= duty <= 1
		self._component.newpin('enable', hal.HAL_BIT, hal.HAL_IN ) #enable = 0 => PWM = polarity
		self._component.ready()

	def start( self ):

		try :

			if self._component['enable'] :
				PWM.start( self._channel, self._component['duty'] * 100.0 , self._freq, self._polarity )
			else :
				PWM.start( self._channel, self._polarity, self._freq, self._polarity )


			while True :
				if self._component['enable'] :
					PWM.set_duty_cycle( self._channel, self._component['duty'] * 100.0 )
				else :
					PWM.set_duty_cycle( self._channel, self._polarity )
				time.sleep( 1.0 / self._updateHz )

		except Exception, err :
			print( 'Component:[%s]:Except:[%s], exiting... '%(self._name, err))
			PWM.stop( self._channel )
			PWM.cleanup()
			self._component.exit()

		except KeyboardInterrupt, err :
			print( 'Component:[%s]:KeyboardInterrupt:[%s], exiting... '%(self._name, err))
			PWM.stop( self._channel )
			PWM.cleanup()
			self._component.exit()


# Main entry point
if __name__ == "__main__" :

	parser = argparse.ArgumentParser( description="HAL component wrapper around Adafuit_BBIO.PWM" )
	parser.add_argument( '-n', '--name', help='HAL component name', required=True, type=str )
	parser.add_argument( '-u', '--update', help='Update rate, Hz', default=1.0, type=float )
	parser.add_argument( '-c', '--channel', help='PWM channel (pin)', required=True, type=str )
	parser.add_argument( '-f', '--frequency', help='PWM frequency, Hz', required=True, type=float )
	parser.add_argument( '-p', '--polarity', help='PWM polarity', default=0, type=int )

	args = parser.parse_args()

	pwm = AdaHalPWM( name=args.name, updateHz=args.update, channel=args.channel, freq=args.frequency, polarity=args.polarity )
	pwm.start()






