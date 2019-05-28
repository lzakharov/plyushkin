Plyushkin
=========

A command line application for dumping photos from your VK account.

Installation
------------

Plyushkin can be installed from source:

.. code:: bash

   # run from project directory
   pip install .

Requirements
~~~~~~~~~~~~

-  Python 3.7 or later. See https://www.python.org/getit/

Dependencies
~~~~~~~~~~~~

-  `aiofiles`_
-  `aiohttp`_

.. _aiofiles: https://github.com/Tinche/aiofiles
.. _aiohttp: https://aiohttp.readthedocs.io

Help
----

To view help run ``plyushkin -h``:

::

   usage: plyushkin [-h] [--output OUTPUT]

   Dump photos from your VK account.

   optional arguments:
     -h, --help       show this help message and exit
     --output OUTPUT  output path. Default is "dump"

Issue tracker
-------------

Please report any bugs and enhancement ideas using the Plyushkin issue
tracker:

https://github.com/lzakharov/plyushkin/issues

Feel free to also ask questions on the tracker.

License
-------

Copyright (c) 2019 Lev Zakharov. Licensed under `the MIT License`_.

.. _the MIT License: https://raw.githubusercontent.com/lzakharov/plyushkin/master/LICENSE
