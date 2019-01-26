# rpi3_machinekit
Trials and tribulations experienced while learning RaspberryPi + machinekit

This is currently a running log of steps taken to get the machinekit application running
on a RaspberryPi3B+...

REFERENCES (Thank you!)

1) http://www.machinekit.io/
2) https://www.raspberrypi.org/downloads/raspbian/
3) https://groups.google.com/forum/m/#!topic/machinekit/wiM-oc7HAms
4) https://www.youtube.com/watch?v=H2XkYI79irQ&t=1s
5) https://www.youtube.com/watch?v=uFbr7xBjItE
6) https://www.youtube.com/watch?v=8lAKXLrmSZo
7) https://lemariva.com/blog/2018/04/rapberry-pi-preempt-rt-kernel-performance-on-rasbperry-pi-3-model-b


Here are the steps performed:

1) Ordered Raspi 3b+ ( skipped the 'expert' installation... :) )
https://www.amazon.com/ELEMENT-Element14-Raspberry-Pi-Motherboard/dp/B07BDR5PDW/ref=sr_1_3?s=pc&ie=UTF8&qid=1544580059&sr=1-3&keywords=raspberry+pi+3+b%2B

2) Ordered / used a 16 GB micro SD card
https://www.amazon.com/Kingston-16GB-microSDHC-microSD-SDCS/dp/B079H6PDCK/ref=sr_1_2?s=pc&ie=UTF8&qid=1544580269&sr=1-2&keywords=micro+sd+card&refinements=p_n_feature_two_browse-bin%3A6518303011

3) Ordered / used a USB SD Card adapter
https://www.amazon.com/Xit-MicroSD-Reader-Writer-XTSDCR/dp/B00APAKX52/ref=sr_1_1?s=electronics&ie=UTF8&qid=1544580397&sr=1-1&keywords=micro+sd+card+usb+adapter

4) Downloaded a fresh image of Raspbian Stretch w/ Desktop
https://www.raspberrypi.org/downloads/raspbian/

5) Unzipped to img file

6) Wrote image file to micro SD card using Etcher
https://www.balena.io/etcher/

7) After image file was written, I 'touched' a file 'ssh' in the micro SD 'boot' folder to enable ssh

8) Removed card from USB adapter, inserted into rpi3b+ and booted..

9) Connected the rpi3b+ to my network via a std Ethernet cable

10) Was able to find out the rpi MAC address by looking at my router logs and then I reserved a local IP addresess

11) Used ssh to log into my pi
	$ ssh pi@192.168.0.200

12) Following (mostly) reference (2) above, I entered these shell commands:

	$ sudo apt-get -y update

    $ mkdir git
    
    $ cd git/
    
    $ git clone --depth=1 https://github.com/raspberrypi/linux -b rpi-4.14.y-rt
    
    $ cd linux/
    
    $ KERNEL=kernel7
    
    $ make bcm2709_defconfig
    
    $ sudo apt-get install ncurses-base
    
    $ sudo apt-get install libncurses5-dev libncursesw5-dev
    
    $ make menuconfig
    
    $ sudo apt-get install bc
    
    $ make -j4 zImage modules dtbs
    
    $ sudo make modules_install
    
    $ sudo cp arch/arm/boot/dts/*.dtb /boot/
    
    $ sudo cp arch/arm/boot/dts/overlays/*.dtb* /boot/overlays/
    
    $ sudo cp arch/arm/boot/dts/overlays/README /boot/overlays/
    
    $ sudo cp arch/arm/boot/zImage /boot/$KERNEL.img
    
    $ sudo reboot -n
    
    $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 43DDF224
    
    $ sudo apt-get dirmngr
    
    $ sudo apt-get install dirmngr
    
    $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 43DDF224
    
    $ sudo sh -c   "echo 'deb http://deb.machinekit.io/debian stretch main' > \
       /etc/apt/sources.list.d/machinekit.list"
    
    $ sudo apt-get update
    
    $ sudo apt-get install machinekit-rt-preempt

13) On my host, I opened a new terminal and enabled x server access
	$ xhost +

14) Then I reconnected to the rpi with
	$ ssh -X pi@192.168.0.200
    $ export DISPLAY=192.168.0.113:0.0

15) And at the prompt I was able to start machinekit with the graphic window shown on my host!
	$ machinekit


SO....  After this initial success, I followed the instructions at http://www.machinekit.io/docs/install/Latency_Test/

and the latency I am seeing seems to be VERY large:

A) For the first test 

	$ latency-test

   the Max jitter while I am not loading the CPU is ~ 60 us (yes, micro-sec)

   and when I load the rpi with another application (glxgears) the latency balloons to about 310 us!!!

B) For the second test as shown on the machinekit website
	
	$ latency-test 25us 1ms

    This test, under load has

    Servo thread:  3.8 us jitter
    Base Thread:   190 us jitter


I think these numbers are quite large, so I will investigate...


12/12/2018

From reference (7) I added the additional lines to the /boot/cmdline.txt, and again ran

    $ latency-test 125us 2ms

This time, the results were: 
Unloaded
Servo Thread (2ms): 101.5 us
Base Thread (125us) 89 us

Loaded
Servo Thread (2ms): 3377472 ns
Base Thread (125us) 214113 ns


Next, I tried recompiling the 4.14.y-rt kernel w/ 1000Hz timer resolution:




12/14

when using the HAL shell + tutorial I ran into an issue w/ 

halcmd: loadusr halmeter
halcmd: Gtk-Message: Failed to load module "canberra-gtk-module"


sudo apt install libcanberra-gtk-module libcanberra-gtk3-module


12/22

CHANGED TO BEAGLE BONE BLACK

1) https://elinux.org/Beagleboard:BeagleBoneBlack_Debian#Flashing_eMMC
2) https://machinekoder.com/machinekit-debian-stretch-beaglebone-black/


Downladed image:
wget https://rcn-ee.com/rootfs/bb.org/testing/2018-12-10/stretch-machinekit/bone-debian-9.6-machinekit-armhf-2018-12-10-4gb.img.xz

Unzipped and wrote to micro SD using 
https://www.balena.io/etcher/

Logged in w/ usr:pass of machinekit:machinekit

$ ssh -X machinekit@192.168.0.123

Made a git folder:

$ mkdir /home/machinekit/git

Cloned

https://github.com/machinekit/machinekit.git

into git

Also found this reference

https://github.com/cdsteinkuehler/beaglebone-black-pinmux/blob/hal_pru_generic/pinmux.ods

on BBB:

$ sudo apt-get update

$ sudo apt-get upgrade

$ sudo apt-get install xauth

$ touch ~/.Xauthority

Now you can run ssh on client 

$ ssh -v -X machinekit@192.168.0.210

$ machinekit

halscope

$ sudo apt-get install libcanberra-gtk-module

https://groups.google.com/forum/#!topic/machinekit/7ZC80xVkfXo

Jun 19 post

Solution to insmod error...
https://jetforme.org/2018/04/machinekit-on-bbb/

1) Install from elinux
2) sudo apt-get update
3) sudo apt-get upgrade
4) machinekit 

select pru-examples in GUI, (check YES to copy config file)
it will fail w/ error


5) Edit newly copied config file in /home/machinekit/configs/pru-examples

$ vim pru-stepper.ini 

For the CONFIG line, change to

CONFIG=prucode=/usr/lib/linuxcnc/rt-preempt/pru_generic.bin pru=1 num_stepgens=3 num_pwmgens=1

Save file

6) Restart machinekit

machinekit@beaglebone:~$ mkdir git
machinekit@beaglebone:~$ cd git/
machinekit@beaglebone:~/git$ git clone https://github.com/machinekit/machinekit.git --depth 1

Info re device tree overlays

http://www.weigu.lu/sb-computer/bbb_device_tree/index.html
http://derekmolloy.ie/gpios-on-the-beaglebone-black-using-device-tree-overlays/

https://github.com/machinekoder/BBIOConfig

issue w/ pin 9.28

Waiting for /sys/class/uio/uio0 OK
P9_28 pinmux file not found!
WARNING: GPIO pin not exported, cannot set direction or value!
bash: /sys/devices/platform/ocp/ocp*P9_28_pinmux/state: No such file or directory
Cannot write pinmux file: /sys/devices/platform/ocp/ocp*P9_28_pinmux/state
CRAMPS.hal:11: program './setup.sh' failed, returned 1
Shutting down and cleaning up Machinekit...

https://groups.google.com/forum/#!topic/beagleboard/EYSwmyxYjdM

added this line to uEnv.txt

cape_enable=bone_capemgr.enable_partno=/lib/firmware/BB-SPIDEV0-00A0.dtbo,/lib/firmware/BB-SPIDEV1-00A0.dtbo

root@beaglebone:/sys/devices/platform/ocp# ls
40300000.ocmcram  48046000.timer     48300000.epwmss    driver_override       ocp:P8_18_pinmux  ocp:P9_23_pinmux
44e07000.gpio     48048000.timer     48302000.epwmss    modalias          ocp:P8_19_pinmux  ocp:P9_24_pinmux
44e09000.serial   4804a000.timer     48304000.epwmss    ocp:cape-universal    ocp:P8_26_pinmux  ocp:P9_26_pinmux
44e0b000.i2c      4804c000.gpio      4830e000.lcdc  ocp:l4_wkup@44c00000  ocp:P9_11_pinmux  ocp:P9_27_pinmux
44e0d000.tscadc   48060000.mmc       48310000.rng   ocp:P8_07_pinmux      ocp:P9_12_pinmux  ocp:P9_30_pinmux
44e35000.wdt      480c8000.mailbox   49000000.edma  ocp:P8_08_pinmux      ocp:P9_13_pinmux  ocp:P9_41_pinmux
44e3e000.rtc      480ca000.spinlock  49800000.tptc  ocp:P8_09_pinmux      ocp:P9_14_pinmux  ocp:P9_42_pinmux
47400000.usb      4819c000.i2c       49900000.tptc  ocp:P8_10_pinmux      ocp:P9_15_pinmux  ocp:P9_91_pinmux
48022000.serial   481a0000.spi       49a00000.tptc  ocp:P8_11_pinmux      ocp:P9_16_pinmux  ocp:P9_92_pinmux
48024000.serial   481a8000.serial    4a100000.ethernet  ocp:P8_12_pinmux      ocp:P9_17_pinmux  of_node
4802a000.i2c      481ac000.gpio      4a300000.pruss ocp:P8_13_pinmux      ocp:P9_18_pinmux  power
48030000.spi      481ae000.gpio      4c000000.emif  ocp:P8_14_pinmux      ocp:P9_19_pinmux  subsystem
48038000.mcasp    481cc000.can       53100000.sham  ocp:P8_15_pinmux      ocp:P9_20_pinmux  uevent
48042000.timer    481d0000.can       53500000.aes   ocp:P8_16_pinmux      ocp:P9_21_pinmux
48044000.timer    481d8000.mmc       56000000.sgx   ocp:P8_17_pinmux      ocp:P9_22_pinmux

###############################################################
######  BBB + CRAMPS from scratch 20190101
###############################################################

Downladed image:
wget https://rcn-ee.com/rootfs/bb.org/testing/2018-12-10/stretch-machinekit/bone-debian-9.6-machinekit-armhf-2018-12-10-4gb.img.xz

Unzipped and wrote to micro SD using 
https://www.balena.io/etcher/

Logged in via ssh on host
    $ ssh machinekit@192.168.0.210
Logged in w/ 
usr: machinekit
passwd: machinekit

Update / upgrade

    $ sudo apt-get update

    $ sudo apt-get upgrade

    $ sudo apt-get install xauth

    $ touch ~/.Xauthority


Edit /boot/uEnv.txt

Uncomment line 

    disable_uboot_overlay_audio=1 

to disable audio function from IO pins (allows for use as GPIO and SPI)

Reboot

    $sudo reboot -n

And login per ssh w/ X windows support

    $ ssh -X machinekit@192.168.200

Make a folder

    $ mkdir ~/git

    $ cd ~/git

Clone machinekit

    $ git clone https://github.com/machinekit/machinekit.git --depth 1

Goto CRAMPS directory

    $ cd ~/git/machinekit/configs/ARM/BeagleBone/CRAMPS

Ensure setup.sh is executable with

    $ chmod 777 setup.sh

Start machinekit w/ CRAMPS.ini

    $ machinekit CRAMPS.ini

Machinekit should start...

FYI, info re. IO pins 

https://github.com/beagleboard/bb.org-overlays/blob/master/src/arm/cape-universal-00A0.dts

20190102

After some more research, I commented out additional lines of /boot/uEnv.txt

    disable_uboot_overlay_emmc=1
    disable_uboot_overlay_video=1

since I am using X windows and a microSD card


remote UI
https://github.com/scottnortman/machinekit.git



20190125

Due to issues w/ remote UI and high CPU usage, going back to tkemc for now...

Also found a problem with PWM generation; both the PWM component and the PRU PWM (as provided in machinekit)
do not work properly; both implements have been tested with the Nomad spindle motor driver controller with
poor results...

Therefore, since machinekit allows for calling of python code in their 'real time' implementation, a work around
using Adafruit BBIO library is under development...

https://github.com/adafruit/adafruit-beaglebone-io-python































































