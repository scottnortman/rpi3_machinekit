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









