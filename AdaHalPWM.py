#!/usr/bin/python2
# encoding: utf-8

#########################################################################
# Description: AdaHalPWM.py                                       	

#	https://github.com/adafruit/adafruit-beaglebone-io-python
# 	                                                    
#                                                                      #
# Author(s): Scott Nortman, scott.nortman@gmail.com                    #
# License: GNU GPL Version 2.0 or (at your option) any later version.  #

import sys
import argparse

import hal
import Adafruit_BBIO.PWM as PWM


class AdaHalPWM( object ) :

	def __init__( self, name='', channel='', duty=0.0, freq=0.0, polarity=0, updateHz=1.0 ) :

		assert( name != ''), ('[%s] is not a valid component name'%(name) )
		assert( channel != ''), ('[%s] is not a valid channel name'%(channel))
		assert( 0.0 <= duty <= 1.0 ), ('[%f] out of range'% (duty))
		assert( 0.0 <= freq ), ('[%f] out of range' % (freq) ) 
		assert( polarity==0 or polarity==1), ('[%d] polarity out of range'%(polarity) )
		assert( 0.1 <= updateHz <= 100.0 ), ('[%f] updateHz out of range' %(updateHz) )

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
				PWM.start( self._channel, self._component['duty'], self._freq, self._polarity )
			else :
				PWM.start( self._channel, self._polarity, self._freq, self._polarity )


			while True :
				if self._component['enable'] :
					PWM.set_duty_cycle( self._channel, self._component['duty'] )
				else :
					PWM.set_duty_cycle( self._channel, self._polarity )
				time.sleep( 1.0 / self._updateHz )

		except Exception, err :
			print( 'Component:[%s]:Except:[%s], exiting... ')
			self._component.exit()

# Main entry point
if __name__ == "__main__" :
	print('AdaHalPWM')


#parser = argparse


