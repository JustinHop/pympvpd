# -*- coding: utf-8 -*-
"""pympvpd.py"""

import click
import click_config_file
import os
import logging
import re
from pathlib import Path


try:
    basestring
except NameError:  # python3
    basestring = str

logging.basicConfig()

log = logging.getLogger(__name__)

def pathinit(base):
    """Creates base directories

    :rtype: bool
    :return: True

    :param str base: Path for the dir base

    """
    log.debug("pathinit({})".format(base))
    for dir in [base, os.path.join(base, "playlists"),os.path.join(base, "cache")]:
        if not os.path.isdir(dir):
            os.makedirs(dir)
    # os.makedirs(os.path.join(base, "playlists"))
    # os.makedirs(os.path.join(base, "cache"))
    return(True)


@click.command()
@click.option('--loglevel', '-l', default="info", show_default=True,
              type=click.Choice(['debug', 'warn', 'info', 'error'],
                                case_sensitive=False), help="Logging level")
@click.option('--port', '-p', type=click.IntRange(1, 65534),
              default="6600", show_default=True,
              help="Listen on port")
@click.option('--host', '-h',
              default="127.0.0.1", show_default=True,
              help="Listen on address")
@click.option('--base', '-b',
              default=str(click.get_app_dir('pympvpd')),
              show_default=True,
              help="Base directory")
@click_config_file.configuration_option()
def main(loglevel, *args, **kwargs):

    if re.match(r'debug', loglevel, re.IGNORECASE):
        log.setLevel(logging.DEBUG)
        log.debug("Log level set to DEBUG")
    elif re.match(r'warn', loglevel, re.IGNORECASE):
        log.setLevel(logging.WARN)
        log.debug("Log level set to DEBUG")
    elif re.match(r'info', loglevel, re.IGNORECASE):
        log.setLevel(logging.INFO)
        log.debug("Log level set to INFO")
    elif re.match(r'error', loglevel, re.IGNORECASE):
        log.setLevel(logging.ERROR)
        log.debug("Log level set to ERROR")

    log.debug("click.get_app_dir(pympvpd): {}".format(
                 click.get_app_dir('pympvpd')))

    if args is not None:
        count = 0
        for arg in args:
            log.debug("Arg {} = {}".format(count, arg))
            count = count + 1
    if kwargs is not None:
        for key, value in kwargs.items():
            log.debug("Key: {}, Value: {}".format(key, value))
            if key == "base":
                pathinit(value)



if __name__ == '__main__':
    main()
