"""
file to control dmx devices

Copyright 2021 Rune Monzel
"""

# internal python modules
import logging
import time
from typing import Union

# external python modules
import serial
import serial.tools.list_ports
import numpy as np


# Use 'dmx' Logger
logger = logging.getLogger('dmx')
logger.setLevel(logging.DEBUG)


class Device(object):
    """
    class to describe further RS-485 devices
    """
    def __init__(self, vid=0, pid=0, serial_number=None):
        """
        :param vid: vendor ID
        :param pid: product ID
        :param serial_number: serial number of the device / chip
        :return None:
        """
        self.vid = vid
        self.pid = pid
        self.serial_number = serial_number


DUMMY = Device(vid=0, pid=0, serial_number=None)

"""
Some notes to EUROLITE USB-DMX512 PRO Cable Interface / EUROLITE USB-DMX512 PRO Interface MK2 :
    - uses chip FTDI232R (like EUROLITE USB-DMX512 PRO Interface MK2)
    - the FTDI232R updates the DMX automatically! You do no need to refresh the DMX universe by yourself
    - if you have only want to update channel 1 to 4 you can just set the number of channels to 4, thus sending to the 
      FTDI232R chip is faster
    - 250000 baudrate is a must
    - needs start bytes: [0x7E, 0x06, 0x01, 0x02, 0x00]
      0x7E: signal start byte
      0x06: label TX
      0x01 and 0x02: LSB of DMX length (do not forget address 0)
      0x00: address 0 of DMX signal, which is always 0
    - supports only label 6: TX DMX Packet
    - needs end byte [0xE7]
    - Example Code:
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
"""
EUROLITE_USB_DMX512_PRO_CABLE_INTERFACE = Device(vid=1027, pid=24577, serial_number=None)


DEVICE_LIST = [DUMMY,
               EUROLITE_USB_DMX512_PRO_CABLE_INTERFACE]


class DMX(object):
    """
    DMX class which talks to RS-485 chip with the pyserial python package
    """

    def __init__(self, num_of_channels: int = 512, serial_number: str = "") -> None:
        """

        :param num_of_channels: integer between 1 and 512
        :param serial_number: serial number of the RS-485 chip as string. If you want to know the current serial number
                              of your device, call my_dmx.device.serial_number
        :return None:
        """

        # numpy array with num_of_channels length
        self.data = np.zeros([1], dtype=np.uint8)

        self.break_us = 88                          # 88us < break condition < 1s -> not used in DMX implementation
        self.MAB_us = 8                             # 8us < Mark-After-Break < 1s -> not used in DMX implementation

        # Search for RS-485 devices, for this look into DEVICE_LIST
        self.ser = None
        self.device = None
        for device in serial.tools.list_ports.comports():
            for known_device in DEVICE_LIST:
                if device.vid == known_device.vid and device.pid == known_device.pid and serial_number == "":
                    try:
                        s = serial.Serial(device.device)
                        s.close()
                    except (OSError, serial.SerialException):
                        pass
                    else:
                        self.device = device
                        break

                elif device.vid == known_device.vid and device.pid == known_device.pid and \
                        serial_number == device.serial_number:
                    try:
                        s = serial.Serial(device.device)
                        s.close()
                        del s
                    except (OSError, serial.SerialException) as error:
                        raise error
                    else:
                        self.device = device
                        logger.info("Found device with serial number: " + serial_number)
                        break
            if self.device:
                logger.info("Found RS-485 interface: " + self.device.description)
                break

        if self.device is None:
            raise ConnectionError("Could not find the RS-485 interface.")

        if self.device.vid == EUROLITE_USB_DMX512_PRO_CABLE_INTERFACE.vid and \
           self.device.pid == EUROLITE_USB_DMX512_PRO_CABLE_INTERFACE.pid:
            self.start_byte = np.array([0x7E, 0x06, 0x01, 0x02, 0x00], np.uint8)
            self.end_byte = np.array([0xE7], np.uint8)
            self.num_of_channels = num_of_channels
            self.ser = serial.Serial(self.device.device,
                                     baudrate=250000,
                                     parity=serial.PARITY_NONE,
                                     bytesize=serial.EIGHTBITS,
                                     stopbits=serial.STOPBITS_TWO
                                     )
        else:
            self.start_byte = np.array([0x00], np.uint8)
            self.end_byte = np.array([], np.uint8)
            self.num_of_channels = num_of_channels
            self.ser = serial.Serial(self.device.device,
                                     baudrate=250000,
                                     parity=serial.PARITY_NONE,
                                     bytesize=serial.EIGHTBITS,
                                     stopbits=serial.STOPBITS_TWO
                                     )

    @property
    def num_of_channels(self) -> int:
        """

        :return num_of_channels: number of DMX channels which shall be used in the universe, the less channels the faster!
        """
        return self.__num_of_channels

    @num_of_channels.setter
    def num_of_channels(self, num_of_channels: int) -> None:
        """
        sets the number of DMX channels

        :param num_of_channels: number of DMX channels
        :return None:
        """
        if num_of_channels > 512:
            raise ValueError("Number of channels are maximal 512! Only channels 1 to 512 can be accessed. " +
                             "Channel 0 is reserved as start channel.")
        if self.device.vid == EUROLITE_USB_DMX512_PRO_CABLE_INTERFACE.vid and \
                self.device.pid == EUROLITE_USB_DMX512_PRO_CABLE_INTERFACE.pid:
            self.start_byte[2] = (num_of_channels+1) & 0xFF
            self.start_byte[3] = ((num_of_channels+1) >> 8) & 0xFF
        self.__num_of_channels = num_of_channels
        old_data = self.data  # save old data
        self.data = np.zeros([self.__num_of_channels], dtype=np.uint8)  # create new data
        # copy old data into new data
        for channel_id in range(min([len(old_data), len(self.data)])):
            self.data[channel_id] = old_data[channel_id]

    def is_connected(self) -> bool:
        """
        checks if the DMX class has a connection to the device

        :return:
        """
        connected = False
        devices = serial.tools.list_ports.comports()
        if self.device is not None:
            if self.device in devices:
                connected = True
        return connected

    def set_data(self, channel_id: int, data: int, auto_send: bool = True) -> None:
        """

        :param channel_id: the channel ID as integer value between 1 and 511
        :param data: the data for the cannel ID as integer value between 0 and 255
        :param auto_send: if True, all DMX Data will be send out
        :return None:
        """
        if channel_id < 1 or channel_id > 512:
            raise ValueError("Channel ID must between 1 and 512.")
        if data < 0 or data > 255:
            raise ValueError("Data ID must between 0 and 255.")
        if channel_id > self.__num_of_channels:
            raise ValueError("Channel ID was not reserved. Please set the num_of_channels first.")

        self.data[channel_id-1] = data

        if auto_send:
            self.send()

    def send(self) -> None:
        """
        Sends data to RS-485 converter

        :return None:
        """
        data = np.concatenate((self.start_byte, self.data, self.end_byte)).tobytes()
        self.ser.write(data)
        self.ser.flush()

    def __del__(self) -> None:
        """
        make sure that all DMX channels are set to 0 due to security reasons
        if you do not want this behaviour, derive this class and override the __del__ function.

        :return None:
        """
        if isinstance(self.ser, serial.Serial):
            if self.ser.is_open:
                if self.is_connected():
                    self.num_of_channels = 512
                    self.data = np.zeros([self.num_of_channels], np.uint8)
                    self.send()
                    # self.send()  # make sure it has been send
                print("close serial port")
                self.ser.close()


def sleep_us(sleep_in_us: int) -> None:
    """
    an accurate sleep in microseconds

    Note: a function call in python needs up to 1 microseconds! This depends on your platform and your computer speed.
    Thus measure this function on your platform if you want to be accurate!

    Example code for measuring:
    '''
    t = time.perf_counter_ns()
    sleep_us(1)
    b = time.perf_counter_ns() - t
    print("elapsed time: %3.3f us" % (b/1000))
    '''

    :param sleep_in_us: sleep time in microseconds
    :return None:
    """
    start_time = time.perf_counter_ns()
    sleep_in_ns = sleep_in_us * 1000
    while (time.perf_counter_ns()-start_time) < sleep_in_ns:
        continue
    return


if __name__ == "__main__":

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s',
                                  "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    dmx = DMX(num_of_channels=4)
    dmx.set_data(1, 0)
    dmx.set_data(2, 0)
    dmx.set_data(3, 0)
    dmx.set_data(4, 0)

    for t in range(5):
        for i in range(0, 255, 5):
            dmx.set_data(1, i, auto_send=False)
            dmx.set_data(2, i, auto_send=False)
            dmx.set_data(3, i, auto_send=False)
            dmx.set_data(4, i)
            time.sleep(0.01)

        for i in range(255, 1, -5):
            dmx.set_data(1, i, auto_send=False)
            dmx.set_data(2, i, auto_send=False)
            dmx.set_data(3, i, auto_send=False)
            dmx.set_data(4, i)
            time.sleep(0.01)

    my_device_sn = dmx.device.serial_number
    del dmx

    dmx2 = DMX(serial_number=my_device_sn)
    dmx2.set_data(1, 100)
    dmx2.send()
    time.sleep(1)
    del dmx2




