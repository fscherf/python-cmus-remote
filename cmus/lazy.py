#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Florian Scherf <fscherf@gmx.net>
# License: MIT License

from lib import CmusRemote, CmusConnectionError

def play(user=None):
    try:
        c = CmusRemote(user=user)
        return c.play()
    except CmusConnectionError:
        return False

def pause(user=None):
    try:
        c = CmusRemote(user=user)
        return c.pause()
    except CmusConnectionError:
        return False

def stop(user=None):
    try:
        c = CmusRemote(user=user)
        return c.stop()
    except CmusConnectionError:
        return False

def next(user=None):
    try:
        c = CmusRemote(user=user)
        return c.next()
    except CmusConnectionError:
        return False

def prev(user=None):
    try:
        c = CmusRemote(user=user)
        return c.prev()
    except CmusConnectionError:
        return False
