soliddisco CLI Reference
========================


The ``soliddisco`` package provides a command-line interface:

.. code:: bash

    $ python -m soliddisco [OPTIONS] [COMMAND] [ARGS]
    ...


The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).


To see its version, run:

.. code:: bash

    $ python -m soliddisco --version
    soliddisco, version 0.1.0


The ``server`` Command
----------------------

To run the ``~`` command:

.. code:: bash

    $ python -m soliddisco server [SUBCOMMAND] [ARGS]

The ``run_server`` subcommand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``run_server`` subcommand receives two arguments, ``address`` and ``data_dir``,
and runs the server.

.. code:: bash

    $ python -m soliddisco server run_server <ADDRESS> <DATA_DIR>
    

The ``website`` Command
-----------------------

To run the ``website`` command:

.. code:: bash

    $ python -m soliddisco website [SUBCOMMAND] [ARGS]

The ``run_webserver`` subcommand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``run_webserver`` subcommand receives two arguments, ``address`` and ``data_dir``,
and runs the website.

.. code:: bash

    $ python -m soliddisco website run_webserver <ADDRESS> <DATA_DIR>
    

The ``client`` Command
----------------------

To run the ``client`` command:

.. code:: bash

    $ python -m soliddisco client [SUBCOMMAND] [ARGS]

The ``upload_thought`` subcommand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``upload_thought`` subcommand receives three arguments, ``address``, ``user_id``, ``thought``,
and uploads a thought.

.. code:: bash

    $ python -m soliddisco client upload_thought <ADDRESS> <USER_ID> <THOUGHT>

The ``error`` subcommand
~~~~~~~~~~~~~~~~~~~~~~~~

The ``error`` subcommand raises an exception.

.. code:: bash

    $ python -m soliddisco client error
    ERROR: something went terribly wrong :[

This can be used to showcase the ``--quiet`` and ``--traceback`` options of the
``soliddisco`` command.


.. code:: bash

    $ python -m soliddisco -q client error

.. code:: bash

    $ python -m soliddisco -t client error
    ERROR: something went terribly wrong :[
    Traceback (most recent call last):
        ...
    RuntimeError: something went terribly wrong :[
