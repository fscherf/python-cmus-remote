#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Florian Scherf <fscherf@gmx.net>
# License: MIT License

import os
import sys
import re
import socket


class regex:
    status = r'(tag|set)? ?(\w+) (.*)\n'
    playing = r'^status playing\n(.*)'
    paused = r'^status paused\n(.*)'
    stopped = r'^status stopped\n(.*)'
    paused_or_stopped = r'^status (paused|stopped)\n(.*)'


class CmusConnectionError(Exception):
    def __init__(self, msg):
        super(CmusConnectionError, self).__init__(msg)


class CmusRemote(object):
    def __init__(self, user=None):
        if user:
            self.socket_path = os.path.join(os.expanduser('~' + user),
                                            '.cmus/socket')
        else:
            self.socket_path = os.path.join(os.environ['HOME'], '.cmus/socket')
        self._connect()

    def __del__(self):
        self._disconnect()

    def _connect(self):
        try:
            self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._socket.connect(self.socket_path)
        except socket.error as e:
            if e.errno == 2:
                raise CmusConnectionError(
                    'No such file or directory: \'%s\'' % self.socket_path)
            raise e

    def _disconnect(self):
        self._socket.close()

    def reconnect(self):
        self._disconnect()
        self._connect()

    def _send_cmd(self, cmd, bufsize=4096):
        try:
            self._socket.send(('%s\n' % cmd).encode('ascii'))
            return self._socket.recv(bufsize)
        except socket.error as e:
            if e.errno == 32:
                raise CmusConnectionError('Broken pipe')
            elif e.errno == 107:
                raise CmusConnectionError(
                    'Transport endpoint is not connected')
            raise e

    def is_playing(self):
        """
        Returns True if status is 'playing'.
        """
        status = self._send_cmd('status')
        return re.match(regex.playing, status) != None

    def is_paused(self):
        """
        Returns True if status is 'paused'.
        """
        status = self._send_cmd('status')
        return re.match(regex.paused, status) != None

    def is_stopped(self):
        """
        Returns True if status is 'stopped'.
        """
        status = self._send_cmd('status')
        return re.match(regex.stopped, status) != None

    def is_paused_or_stopped(self):
        """
        Returns True if status is 'paused' or 'stopped'.
        """
        status = self._send_cmd('status')
        return re.match(regex.paused_or_stopped, status) != None

    def status(self):
        """
        Returns current status as dict.
        """
        status = self._send_cmd('status')
        ret = re.findall(regex.status, status, re.MULTILINE)
        ret = {i[1]: i[2] for i in ret}

        for k, v in ret.items():
            if k in ['artist', 'album', 'comment', 'date', 'genre']:
                continue

            if v == 'true':
                ret[k] = True
            elif v == 'false':
                ret[k] = False
            else:
                try:
                    ret[k] = int(v)
                    continue
                except ValueError:
                    pass

                try:
                    ret[k] = float(v)
                    continue
                except ValueError:
                    pass

        return ret

    def timestring(self, status_bit=False, utf8=False):
        status = self.status()

        if status_bit:
            if status['status'] == 'playing':
                status_bit = '▶ ' if utf8 else  '> '
            elif status['status'] == 'paused':
                status_bit = '▮▮ ' if utf8 else  '| '
            else:
                status_bit = '◼ ' if utf8 else  '. '
        else:
            status_bit = ''

        try:
            return '%s%02d:%02d / %02d:%02d' % (status_bit,
                                                status['position'] / 60,
                                                status['position'] % 60,
                                                status['duration'] / 60,
                                                status['duration'] % 60)
        except KeyError:
            return '%s00:00 / 00:00' % status_bit

    def play(self):
        """
        Toggles play.
        """
        if self.is_paused_or_stopped():
            self._send_cmd('player-play')
            return self.is_playing()
        elif self.is_playing():
            self._send_cmd('player-pause')
            return self.is_paused()
        self._send_cmd('player-play')
        return self.is_playing()

    def pause(self):
        """
        Pause player.
        Returns False if player is already paused.
        """
        if self.is_paused():
            return False
        self._send_cmd('player-pause')
        return self.is_paused()

    def stop(self):
        """
        Stop player.
        Returns False if player is already stopped.
        """
        if self.is_stopped():
            return False
        self._send_cmd('player-stop')
        return self.is_stopped()

    def next(self):
        file = self.status()['file']
        self._send_cmd('player-next')
        return self.status()['file'] != file

    def prev(self):
        file = self.status()['file']
        self._send_cmd('player-prev')
        return self.status()['file'] != file
