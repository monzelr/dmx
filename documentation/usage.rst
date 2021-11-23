=====
Usage
=====

Example Code Snippets
---------------------
If you want to dim 4 channels up and down:

.. code-block:: python

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

.. code-block:: python

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