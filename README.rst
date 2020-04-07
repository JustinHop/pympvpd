=========
 pympvpd
=========

Control an mpv(mplayer/ffmpeg) instance using Music Player Daemon protocol.


Status
======

.. image:: https://secure.travis-ci.org/JustinHop/pympvpd.png?branch=master
   :target: http://travis-ci.org/JustinHop/pympvpd
.. image:: https://coveralls.io/repos/JustinHop/pympvpd/badge.png?branch=master
   :target: https://coveralls.io/r/JustinHop/pympvpd?branch=master
.. image:: https://img.shields.io/pypi/v/pympvpd.svg
   :target: https://pypi.python.org/pypi/pympvpd
.. image:: https://readthedocs.org/projects/pympvpd/badge/?version=latest
   :target: https://readthedocs.org/projects/pympvpd/?badge=latest
   :alt: Documentation Status


Requirements
============

* Python 3.7 over

* You need to use my version of python-mpd-server https://github.com/JustinHop/python-mpd-server.git

* You can try older, but I'm not

Features
========

* Plan:
    Support configfile and positional args for port, user, logging, paths....
      Use click and click-config-file

      Done.

      Needs test

    Start up mpd compliant tcp server

      Done.

      Needs test

    Add media/urls over mpd

    Stateful playlist, maybe sqlite, maybe mongdb, maybe pickle

    Maybe m3u8 playlists with modified tags to support streaming metadata

    Parse youtube-dl able content and map data, artist=channel, track=title etc

    Store original url, release date, views, thumbnails, etc

    Map playback commands

    Package nicely with systemd units, Dockerfiles, etc

* Ideas:
    Map youtube/bitchute channel to directory

    Map youtube playlists to playlists

    use aio_mpv_jsonipc



Setup
=====

::

  $ python -m pip install --user pympvpd
  or
  (venv)$ python -m pip install pympvpd

Usage
=====

ToDo: Rewrite me.

::

  $ python
  >>> import pympvpd
  >>> pympvpd.sample.hello()
  'hello'
  >>>

