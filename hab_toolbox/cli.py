#!/usr/bin/env python3

import logging
import click

import utils


@click.group()
@click.option('-v', '--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
def cli(verbose, debug):
    FORMAT = '%(asctime)-15s %(levelname)+8s: %(message)s'
    logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z")
    log = logging.getLogger()

    if debug:
        log.setLevel(logging.DEBUG)
    elif verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARNING)


@cli.command()
def test():
    # test the current logging level
    utils.test_logger()


cli.add_command(test)
if __name__ == '__main__':
    cli()
