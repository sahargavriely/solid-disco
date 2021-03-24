import os
import sys
import traceback

import click

import soliddisco


class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group()
@click.version_option(soliddisco.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.group()
def server():
    pass


@server.command('run_server')
@click.argument('address', type=str)
@click.argument('data_dir', type=str)
def soliddisco_run_server(address, data_dir):
    host, port = address.split(':')
    address = (host, int(port))
    log(soliddisco.run_server(address, data_dir))


@main.group()
def website():
    pass


@website.command('run_webserver')
@click.argument('address', type=str)
@click.argument('data_dir', type=str)
def soliddisco_run_webserver(address, data_dir):
    host, port = address.split(':')
    address = (host, int(port))
    log(soliddisco.run_webserver(address, data_dir))


@main.group()
def client():
    pass


@client.command('upload_thought')
@click.argument('address', type=str)
@click.argument('user', type=str)
@click.argument('thought', type=str)
def soliddisco_upload_thought(address, user, thought):
    host, port = address.split(':')
    address = (host, int(port))
    log(soliddisco.upload_thought(address, user, thought))


@client.command('error')
def bar_error():
    raise RuntimeError('something went terribly wrong :[')


if __name__ == '__main__':
    try:
        main(prog_name='soliddisco')
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
