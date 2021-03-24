![build status](https://travis-ci.com/sahargavriely/solid-disco.svg?branch=main)
[![codecov](https://codecov.io/gh/sahargavriely/solid-disco/branch/main/graph/badge.svg?token=1IEZYW6IJO)](https://codecov.io/gh/sahargavriely/solid-disco)
![coverage](https://codecov.io/gh/sahargavriely/solid-disco/branch/main/graph/badge.svg)

# solid-disco

An example package. See [full documentation](https://advanced-system-design-foobar.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:sahargavriely/solid-disco.git
    ...
    $ cd solid-disco/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [solid-disco] $  # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `soliddisco` packages provides the following functions:

- `run_server`

    This function starts the server at a givven address and accepts thoughts from users.
    You must provid a directory which the server save the thoughts to. 

    ```pycon
    >>> from soliddisco import run_server
    >>> run_server('localhost:5000', data_dir)

    ```

- `upload_thought`

    This function sends a thought to the server at a givven address.
    Apart from the address you will have to provide the user's id and thought.

    ```pycon
    >>> from soliddisco import upload_thought
    >>> upload_thought('localhost:5000', 1, "I think therefore I am")
    done!
    >>>
    ```

- `run_webserver`

    This function starts the webserver at a givven address.
    In the website you will find the thoughts from a givven directory.

    ```pycon
    >>> from soliddisco import run_webserver
    >>> run_webserver('localhost:8000', "data_dir")
    * Serving Flask app "soliddisco.websiteserver.web" (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: on
    * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)

    ```

The `soliddisco` package also provides a command-line interface:

```sh
$ python -m soliddisco
soliddisco, version 0.1.0
```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `server` command, with the `run_server` subcommand:

```sh
$ python -m soliddisco server run_server <ADDRESS> <DATA_DIR>
```

The CLI provides the `client` command, with the `upload_thought` subcommand:

```sh
$ python -m soliddisco client upload_thought <ADDRESS> <USER_ID> <THOUGHT>
```

The CLI provides the `website` command, with the `run_webserver` subcommand:

```sh
$ python -m soliddisco website run_webserver <ADDRESS> <DATA_DIR>
```

Do note that each command's options should be passed to *that* command, so for
example the `-q` and `-t` options should be passed to `soliddisco`, not `server` or
`run_server`.

```sh
$ python -m soliddisco server run_server -q  # this doesn't work
ERROR: no such option: -q
$ python -m soliddisco -q server run_server  # this does work
```

To showcase these options, consider `client`'s `error` subcommand, which raises an
exception:

```sh
$ python -m soliddisco client error
ERROR: something went terribly wrong :[
$ python -m soliddisco -q client error  # suppress output
$ python -m soliddisco -t client error  # show full traceback
ERROR: something went terribly wrong :[
Traceback (most recent call last):
    ...
RuntimeError: something went terrible wrong :[
```
