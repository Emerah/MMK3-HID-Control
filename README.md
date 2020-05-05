# MMK3-HID-Control


the problem we are trying to solve is the problem of gaining access to the gorgeous screens found on newer generation ni products, namely **Maschine MK3** and **Komplete Kontrol S-MK2** series.

this can be very useful if we for example want to use one of those ni products with ableton live and be able to see meaningful feedback on the screens instead of using the old and ugly mackie control protocol for text display. to make things worse, mackie is only available on the maschine mk3 hardware and not the komplete series.

for this prototype engine we will try to accomplish 2 things:

- send valid data messages to Maschine MK3 to fill the screens with colors.
- send images to Maschine MK3 screens

![Display Images on Maschine MK3 screens](https://repository-images.githubusercontent.com/260289282/8e735200-8f1c-11ea-94f3-68c94e5293a1)

 since we know the product ids of all NI products with similar screens, we could  assume that what works here will also work with komplete keyboards from the S mk2 family *with minor touches*. in order to be able to access Maschine MK3 screens and therefore be able to accomplish the goals of this prototype we must suspend ni drivers.

**Suspending ni backend support services**

ni products are back-powered by ni drivers that handle all communications between the hardware device and ni applications running on your computer like komplete kontrol and maschine 2 software or other midi-capable software. as soon as your computer starts, these drivers claims control of the hardware and therefore before we are able to send date to the screens, we must suspend these background processes/drivers to be able to claim control of the hardware to ourselves.

this operation is complletely safe. as soon you start maschine 2 software or at worst restart your computer, the drivers start up and immidiately claim control of the Maschine MK3 hardware device again.

**Platform**

the code in this prototype was developed on **macOS 10.14.6 and 10.15.x**. since we must accesses the system to suspend ni drivers the code will only work on **mac**. developed with **python 3.7.7**

**Required**

this prototype uses **pyusb**, which uses **libusb** as its backend. and uses **PIL** for image creation. these libraries must be installed before this prototype will work on your computer

    brew install libusb 
    pip3 install Pillow
    pip3 install pyusb

***note on libusb***: libusb has been recently updated to ver 1.0.23 (used in this project). currently brew installs an older version of libusb .. otherwise you will have to build the libusb library from source. in case you decide to build the library on your mac, you must have **autoconf**, **automake**, and **libtools** installed before you attempt at building the library .. 

automake installs autoconf as a requirement.

    brew install automake, libtool


**How to run**

download this packege. in terminal, cd to the package folder and type:

    python3 main.py

script will ask you to agree to suspending ni drivers. if you choose yes, the script will run and you should see you Maschine MK3 screens blink in random colors. and display the 2 images at the end of the color sequence.

you should set **"running"** flag in main.py to **False** after suspending the drivers the first time so it doesnt ask you everytime you run it. the process of suspending the drivers allows *6 seconds* if wait so the system has enough time to actually suspend the drivers.
