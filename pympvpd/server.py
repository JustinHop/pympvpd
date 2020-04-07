# -*- coding: utf-8 -*-
"""server.py"""

import socketserver
socketserver.TCPServer.allow_reuse_address = True

import time
import re
import threading
import sys

import mpdserver
# from import mpdserver *
import logging

#try:
#    basestring
#except NameError:  # python3
#    basestring = str

logger = logging.getLogger(__name__)

class PyPlay(mpdserver.Play):
    def handle_args(self, songPos=0):
        logger.info("*** Set player to play state ***")


class PyPlayId(mpdserver.PlayId):
    # This method is called when playid command is sent by a client
    def handle_args(self, songId=0):
        logger.info("*** Play a file with Id '%d' ***" % songId)

# Define a MpdPlaylist based on mpdserver.MpdPlaylist
# This class permits to generate adapted mpd respond on playlist command.


class PyMpdPlaylist(mpdserver.MpdPlaylist):
    playlist = [mpdserver.MpdPlaylistSong(file='file0', songId=0)]
    # How to get song position from a song id in your playlist

    def songIdToPosition(self, i):
        for e in self.playlist:
            if e.id == i:
                return e.playlistPosition
    # Set your playlist. It must be a list a MpdPlaylistSong

    def handlePlaylist(self):
        return self.playlist
    # Move song in your playlist

    def move(self, i, j):
        self.playlist[i], self.playlist[j] = self.playlist[j], self.playlist[i]

class PyMpdRequestHandler(mpdserver.MpdRequestHandler):
    """ Manage the connection from a mpd client. Each client
    connection instances this object."""
    Playlist = PyMpdPlaylist
    __player = None
    __SupportedCommands = {
                           'currentsong': {'class': mpdserver.CurrentSong, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': ["sonata"]},
                           'outputs': {'class': mpdserver.Outputs, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': ["gmpc"]},
                           'status': {'class': mpdserver.Status, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': ["sonata"]},
                           'stats': {'class': mpdserver.Stats, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'notcommands': {'class': mpdserver.NotCommands, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': ["gmpc"]},
                           'commands': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'lsinfo': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'tagtypes': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'playlistinfo': {'class': mpdserver.PlaylistInfo, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'playlistid': {'class': mpdserver.PlaylistId, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'listplaylistinfo': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'plchanges': {'class': mpdserver.PlChanges, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': ["sonata"]},
                           'plchangesposid': {'class': mpdserver.PlChangesPosId, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'moveid': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'move': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'delete': {'class': mpdserver.Delete, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'deleteid': {'class': mpdserver.DeleteId, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'add': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'playid': {'class': PyPlayId, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'play': {'class': PyPlay, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'password': {'class': mpdserver.Password, 'users': ['default'], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': ["all"]},
                           'clear': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'stop': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'seek': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'pause': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'next': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'previous': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'random': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'listplaylists': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'load': {'class': None, 'users': [], 'group': 'write', 'mpdVersion': "0.12", 'neededBy': None},
                           'save': {'class': None, 'users': [], 'group': 'write', 'mpdVersion': "0.12", 'neededBy': None},
                           'search': {'class': None, 'users': [], 'group': 'read', 'mpdVersion': "0.12", 'neededBy': None},
                           'rm': {'class': None, 'users': [], 'group': 'write', 'mpdVersion': "0.12", 'neededBy': None},
                           'setvol': {'class': None, 'users': [], 'group': 'control', 'mpdVersion': "0.12", 'neededBy': None}
                           }

    def __init__(self, request, client_address, server):
        self.playlist = self.Playlist()
        self.frontend = mpdserver.Frontend()
        logger.debug(
            "Client connected (%s)" %
            threading.currentThread().getName())
        socketserver.StreamRequestHandler.__init__(
            self, request, client_address, server)

    """ Handle connection with mpd client. It gets client command,
    execute it and send a respond."""

    def handle(self):
        welcome = "OK MPD 0.16.0\n"
        self.request.send(welcome.encode("utf-8"))
        while True:
            msg = ""
            try:
                cmdlist = None
                cmds = []
                while True:
                    self.data = self.rfile.readline().strip()
                    if len(self.data) == 0:
                        raise IOError  # To detect last EOF
                    if self.data.decode("utf-8") == "command_list_ok_begin":
                        cmdlist = "list_ok"
                    elif self.data.decode("utf-8") == "command_list_begin":
                        cmdlist = "list"
                    elif self.data.decode("utf-8") == "command_list_end":
                        break
                    else:
                        cmds.append(self.data)
                        if not cmdlist:
                            break
                logger.debug(
                    "Commands received from %s" %
                    self.client_address[0])
                respond = False
                try:
                    for c in cmds:
                        c = c.decode("utf-8")
                        logger.debug("Command '" + c + "'...")
                        (respond, rspmsg) = self.__cmdExec(c)
                        msg += rspmsg
                        if cmdlist == "list_ok":
                            msg = msg+"list_OK\n"
                except mpdserver.MpdCommandError as e:
                    logger.info("Command Error: %s" % e.toMpdMsg())
                    msg = e.toMpdMsg()
                except BaseException:
                    raise
                else:
                    msg = msg+"OK\n"
                logger.debug("Message sent:\n\t\t"+msg.replace("\n", "\n\t\t"))
                if respond:
                    self.request.send(msg.encode("utf-8"))
            except IOError as e:
                logger.debug(
                    "Client disconnected (%s)" %
                    threading.currentThread().getName())
                break

    def __cmdExec(self, c):
        """ Execute mpd client command. Take a string, parse it and
        execute the corresponding server.Command function."""
        try:
            # WARNING An argument cannot contains a '"'
            pcmd = [m.group()
                    for m in re.compile('(\w+)|("([^"])+")').finditer(c)]
            cmd = pcmd[0]
            for i in range(1, len(pcmd)):
                pcmd[i] = pcmd[i].replace('"', '')
            args = pcmd[1:]
            logger.debug(
                "Command executed : %s %s for frontend '%s'" %
                (cmd, args, self.frontend.get()))
            commandCls = self.__getCommandClass(cmd, self.frontend)
            msg = commandCls(
                args,
                playlist=self.playlist,
                frontend=self.frontend,
                player=self.__class__.__player,
                request=self.request).run()
        except mpdserver.MpdCommandError:
            raise
        except mpdserver.CommandNotSupported:
            raise
        except BaseException:
            logger.critical(
                "Unexpected error on command %s (%s): %s" %
                (c, self.frontend.get(), sys.exc_info()[0]))
            raise
        logger.debug("Respond:\n\t\t"+msg.replace("\n", "\n\t\t"))
        return (commandCls.respond, msg)

    # Manage user rights
    @classmethod
    def RegisterCommand(cls, cls_cmd, users=['default']):
        """ Register a command. Make this command supported by a mpd
        server which use this request handler class. cls_cmd is a
        class which inherits from :class:`command_base.Command`."""
        cls.__SupportedCommands[cls_cmd.GetCommandName()]['class'] = cls_cmd
        for a in users:
            cls.__SupportedCommands[cls_cmd.GetCommandName()]['users'].append(a)

    @classmethod
    def UnregisterCommand(cls, commandName):
        """ Unregister a command"""
        cls.__SupportedCommands[commandName] = None

    @classmethod
    def UserPermissionsCommand(cls, user, commandName=None, group=None):
        """ Add permissions for user 'user'. If commandName is not specified, group should be specified. """
        if commandName is not None:
            cls.__SupportedCommands[commandNames]['users'].append(user)
        elif group is not None:
            for c in cls.__SupportedCommands.values():
                if c['group'] == group:
                    c['users'].append(user)
        else:
            raise TypeError

    @classmethod
    def SupportedCommand(cls):
        """Return a list of command and allowed users."""
        return [
            "%s\t\t%s" %
            (k,
             v['users']) for (
                k,
                v) in cls.__SupportedCommands.items() if v['class'] is not None]

    def __getCommandClass(self, commandName, frontend):
        """ To get a command class to execute on received command
        string. This method raise supported command errors."""
        if commandName not in self.__SupportedCommands:
            logger.warning("Command '%s' is not a MPD command!" % commandName)
            raise mpdserver.CommandNotMPDCommand(commandName)
        elif self.__SupportedCommands[commandName]['class'] is None:
            if self.__SupportedCommands[commandName]['neededBy'] is not None:
                logger.critical(
                    "Command '%s' is needed for client(s) %s" %
                    (commandName, " ".join(
                        self.__SupportedCommands[commandName]['neededBy'])))
            logger.warning("Command '%s' is not supported!" % commandName)
            raise mpdserver.CommandNotSupported(commandName)
        elif not (mpdserver.Frontend.GetDefaultUsername() in self.__SupportedCommands[commandName]['users']
                  or mpdserver.frontend.getUsername() in self.__SupportedCommands[commandName]['users']):
            raise mpdserver.UserNotAllowed(commandName, frontend.getUsername())
        else:
            return self.__SupportedCommands[commandName]['class']

    @classmethod
    def SetPlayer(cls, player):
        """To set player object. It is passed to executed commands."""
        cls.__player = player

    @classmethod
    def GetPlayer(cls):
        """To get player object associated to pympdserver."""
        return cls.__player


# Define a playid command based on mpdserver.PlayId squeleton

class PyMPD(mpdserver.MpdServerDaemon):
    """Just reimplement MpdServerDaemon"""

    def __init__(self, port=6600, host="127.0.0.1", base="/tmp"):
        self.port = port
        self.host = host
        mpdserver.MpdServerDaemon.__init__(self, self.port, mpdRequestHandler=PyMpdRequestHandler)
                                           # RequestHandlerClass=PyMpdRequestHandler)

    def quit(self):
        """Stop MPD server deamon."""
        logger.info("Quiiting Mpd Server")
        self.shutdown()

    def wait(self,timeout=None):
        """ Return True if mpd is alive, False otherwise. This method
        is useful to catch Keyboard interrupt for instance."""
        if timeout==None:
            self.thread.join()
        else:
            self.thread.join(timeout)
        return self.thread.isAlive()

# Create a deamonized mpd server that listen on port 9999
# mpd=mpdserver.MpdServerDaemon(9999)
# Register provided outputs command
# mpd.requestHandler.RegisterCommand(mpdserver.Outputs)
# Register your own command implementation
# mpd.requestHandler.RegisterCommand(PlayId)
# mpd.requestHandler.RegisterCommand(Play)
# Set the user defined playlist class
# mpd.requestHandler.Playlist=MpdPlaylist
# mpd.requestHandler.Playlist=mpdserver.MpdPlaylistDummy


