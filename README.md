USB-DMX512 Python Module
========================

This python module supports actual the following USB-DMX interfaces (FT232R chip based):
- EUROLITE USB-DMX512 PRO Cable Interface [(Link)](https://www.steinigke.de/en/mpn51860122-eurolite-usb-dmx512-pro-cable-interface.html)
- EUROLITE USB-DMX512 PRO Interface MK2 [(Link)](https://www.steinigke.de/en/mpn51860121-eurolite-usb-dmx512-pro-interface-mk2.html)


Requirements
------------ 
- Python ≥ 3.6
- numpy
- pyserial

Note: Tested on Windows 10, amd64, Python 3.8 \
Should also work on Linux, MacOS and on AARCH64 devices (ARM devices like Raspberry PI).


Installation
------------
Make sure to have git, python and pip in your environment path or activate your python environment before this code snippet:

    git clone https://github.com/monzelr/dmx.git

    cd dmx

    pip install dmx

Example Code Snippets
---------------------
If you want to dim 4 channels up and down:

    from dmx import DMX
    import time

    dmx = DMX(num_of_channels=4)
    dmx.set_data(1, 0)
    dmx.set_data(2, 0)
    dmx.set_data(3, 0)
    dmx.set_data(4, 0)
    
    while True:
        for i in range(0, 255, 5):
            dmx.set_data(1, i, auto_send=False)
            dmx.set_data(2, i, auto_send=False)
            dmx.set_data(3, i, auto_send=False)
            dmx.set_data(4, i)
            time.sleep(0.01)
    
        for i in range(255, 0, -5):
            dmx.set_data(1, i, auto_send=False)
            dmx.set_data(2, i, auto_send=False)
            dmx.set_data(3, i, auto_send=False)
            dmx.set_data(4, i)
            time.sleep(0.01)

If you want to add your own adapter or multiple adapter by serial number:


    from dmx import DMX

    dmx = DMX()
    my_device_serial_number = dmx.use_device.serial_number
    del dmx

    my_device_sn = dmx.use_device.serial_number
    del dmx

    dmx2 = DMX(serial_number=my_device_sn)
    dmx2.set_data(1, 100)
    dmx2.send()
    time.sleep(1)
    del dmx2

Technical notes
---------------
to EUROLITE USB-DMX512 PRO Cable Interface / EUROLITE USB-DMX512 PRO Interface MK2 :

- uses chip FTDI232R (like EUROLITE USB-DMX512 PRO Interface MK2)
- the FTDI FT232R updates the DMX automatically - you do no need to refresh the DMX universe by yourself
- if you only have 4 channels, set them at the DMX address start (1 to 4), thus sending updates to the FT232R chip is faster
- 250000 baudrate for the FT232R is a must
- needs 5 start bytes: [0x7E, 0x06, 0x01, 0x02, 0x00]
  
  - byte 1: signal start byte 0x7E
  - byte 2: TX DMX packet: 0x06
  - byte 3 & 4: LSB of DMX length (in this case 513 -> do not forget address 0): 0x01 and 0x02
  - byte 5: address 0 of DMX signal: 0x00
- supports only label 6: TX DMX Packet
- needs one end byte [0xE7]


Building the documentation
--------------------------
Go into the dmx root folder (where setup.py is) and type in the following command in the cmd/shell:

    python setup.py build_sphinx

The documentation can than be found in dmx/build/sphinx/html.
