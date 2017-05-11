.. highlight:: rest

.. _build:
.. _zlog: https://github.com/HardySimpson/zlog
.. _check: https://libcheck.github.io/check/
.. _zlog_install: https://github.com/HardySimpson/zlog
.. _check_install: https://libcheck.github.io/check/web/install.html

Build
=====

Dependencies
------------
This project has two external dependencies:

- The zlog_ library is used as the logging mechanism. This enables the module to log important parameters and options
  every time the tool is run which allows for easier debugging.
- In order to unit test our code the check_ library is used; this is optional so it doesn't need to be installed.


Installing Dependencies
-----------------------

Zlog Installation
~~~~~~~~~~~~~~~~~
To install zlog please follow the instructions at zlog_install_.

Check Installation [Optional]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Installation of this library is optional, however, if you want to run the unit tests then
you must install it. Please follow the instructions at check_install_.

Installation
------------
First, make sure the dependencies are installed as outlined above and then follow these steps:

1. Clone the repository
2. Navigate to the root directory (./forecast) and create a build directory

.. code-block:: bash

    mkdir build

3. Navigate to the build directory

.. code-block:: bash

    cd build/

4. Run cmake from the build directory

.. code-block:: bash

    cmake ../

NOTE: If check is installed then you may run the following line to build the unit tests along with the main executable:

.. code-block:: bash

      cmake ../ -DFORECAST_ENABLE_TESTING=ON

5. Compile and install the files

.. code-block:: bash

    make
    make install
