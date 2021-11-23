============
Installation
============


From sources
------------

The sources for dmx can be found in the github `github repo`_.

You should clone the private repository (ask for access):

.. code-block:: console

    $ git clone git://gitlab.com/monzelr/dmx

Best practice is just to link the source doe to your python environment via the develop command:

.. code-block:: console

    $ cd dmx
    $ pip install dmx

To uninstall the python package, type in this command:

.. code-block:: console

    $ pip uninstall dmx

Of course, you can also install the package with python:

.. code-block:: console

    $ python setup.py install

For deployment
--------------
If you want to distribute the package, please build a python wheel which can be distributed:

.. code-block:: console

    $ python setup.py build_ext
    $ python setup.py bdist_wheel

The wheel contains compiled machine code which is not readable for humans. Thus it can be deployed savely.
The wheel can be installed with the pip command.

.. _github repo: https://github.com/monzelr/dmx
