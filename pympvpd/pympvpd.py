# -*- coding: utf-8 -*-
"""pympvpd.py"""

from __future__ import print_function

import click
import click_config_file
import os
import re
from pathlib import Path
# import aio_mpv_jsonipc
from python_mpv_jsonipc import MPV

import mpdserver
from .mpv import *

from .server import PyMPD

try:
    basestring
except NameError:  # python3
    basestring = str

import logging
logging.basicConfig()

logger = logging.getLogger(__name__)

# mpv = aio_mpv_jsonipc.MPV(socket='/tmp/mpv.socket')
mpv = MPV(start_mpv=False, ipc_socket='/tmp/mpv.socket')


def pathinit(base):
    """Creates base directories

    :rtype: bool
    :return: True

    :param str base: Path for the dir base

    """
    logger.debug("pathinit({})".format(base))
    for dir in [
        base, os.path.join(
            base, "playlists"), os.path.join(
            base, "cache")]:
        if not os.path.isdir(dir):
            os.makedirs(dir)
    # os.makedirs(os.path.join(base, "playlists"))
    # os.makedirs(os.path.join(base, "cache"))
    return(True)

class Play(mpdserver.Play):
    def handle_args(self, songPos=0):
        logger.info("*** Set player to play state ***")
        mpv.command('set', 'pause', 'no')


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
@click.option('--socket', '-s',
              type=click.Path(exists=True),
              default=None, show_default=True,
              help="MPV IPC socket path. This arg assumes already running mpv")
@click_config_file.configuration_option()
def main(loglevel, socket, *args, **kwargs):

    if re.match(r'debug', loglevel, re.IGNORECASE):
        logger.setLevel(logging.DEBUG)
        logger.debug("logger level set to DEBUG")
    elif re.match(r'warn', loglevel, re.IGNORECASE):
        logger.setLevel(logging.WARN)
        logger.debug("logger level set to DEBUG")
    elif re.match(r'info', loglevel, re.IGNORECASE):
        logger.setLevel(logging.INFO)
        logger.debug("logger level set to INFO")
    elif re.match(r'error', loglevel, re.IGNORECASE):
        logger.setLevel(logging.ERROR)
        logger.debug("logger level set to ERROR")

    logger.debug("click.get_app_dir(pympvpd): {}".format(
                 click.get_app_dir('pympvpd')))

    if args is not None:
        count = 0
        for arg in args:
            logger.debug("Arg {} = {}".format(count, arg))
            count = count + 1
    if kwargs is not None:
        for key, value in kwargs.items():
            logger.debug("Key: {}, Value: {}".format(key, value))
            if key == "base":
                pathinit(value)

    #mpv = None
    #if socket is not None:
    #    mpv = aio_mpv_jsonipc.MPV(socket=socket)
    mpd = PyMPD(**kwargs)



#   mpd.requestHandler.RegisterCommand(mpdserver.Outputs)
#   mpd.requestHandler.RegisterCommand(PlayId)
    mpd.requestHandler.RegisterCommand(Play)
#   mpd.requestHandler.Playlist = MpdPlaylist

    try:
        while mpd.wait(1):
            pass
    except KeyboardInterrupt:
        logger.error("Stopping on interrupt")
        mpd.quit()


if __name__ == '__main__':
    main()
