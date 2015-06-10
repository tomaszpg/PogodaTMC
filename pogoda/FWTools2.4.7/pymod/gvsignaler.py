###############################################################################
# $Id: gvsignaler.py,v 1.6 2003/01/07 18:44:32 gmwalter Exp $
#
# Project:  OpenEV
# Purpose:  Signaler - implements subscription/notification system a bit like
#           Gtk signaling.
# Author:   Frank Warmerdam, warmerda@home.com
#
###############################################################################
# Copyright (c) 2000, Atlantis Scientific Inc. (www.atlsci.com)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
###############################################################################
# 
#  $Log: gvsignaler.py,v $
#  Revision 1.6  2003/01/07 18:44:32  gmwalter
#  Changed a tuple to a list to fix a blocking bug.
#
#  Revision 1.5  2001/04/03 02:30:38  warmerda
#  fixed signal name typo
#
#  Revision 1.4  2001/03/19 21:57:14  warmerda
#  expand tabs
#
#  Revision 1.3  2000/08/09 01:04:13  warmerda
#  fixed bug in unsubscribe
#
#  Revision 1.2  2000/06/09 01:04:14  warmerda
#  added standard headers
#


"""
MODULE
   gvsignaler
   
DESCRIPTION
   Provides an event subscription/notification mechanism a bit like
   Gtk signal handling.  Classes which derive from Signaler can
   publish a list of named signals.  These signals can then be
   attached to arbitrary callback methods/functions using subscribe().
   More than one callback function per signal can be attached.
   The Signaler executes the callback functions with the notify()
   method.

   Arguments to the callback functions are (in order):
     1. The Signaler instance.
     2. Any signal specific arguments provided to notify().
     3. Subscriber baggage arguments provided to subscribe().
   The baggage arguments act like the 'data' argument of Gtk signals.
"""

class UnpublishedSignalError(Exception): pass
class SignalExistsError(Exception): pass

class Signaler:
    "Base class for objects with published signals"
    signal = {}  # Prevents AttributeErrors

    def publish(self, *sigs):
        "Publish one or more named signals"
        if not self.__dict__.has_key('signal'):
            self.signal = {}
        for s in sigs:
            if self.signal.has_key(s):
                raise SignalExistsError
            self.signal[s] = [0, []]  # Blocked flag, handlers list

    def subscribe(self, name, meth, *args):
        "Attach a callback function/method to a signal"
        try:
            self.signal[name][1].append((meth, args))
        except KeyError:
            raise UnpublishedSignalError

    def unsubscribe(self, name, meth):
        "Remove a callback function/method for a named signal"
        try:
            l = len(self.signal[name][1])
            for si in range(l):
                if self.signal[name][1][si][0] == meth:
                    del self.signal[name][1][si]
                    break
        except KeyError:
            raise UnpublishedSignalError

    def notify(self, name, *args):
        "Execute callbacks attached to the named signal"
        try:
            sig = self.signal[name]
        except KeyError:
            raise UnpublishedSignalError
        # Check for blocked signal
        if sig[0] == 0:
            for s in sig[1]:
                apply(s[0], (self,) + args + s[1])

    def block(self, name):
        "Prevent a signal from being emitted"
        try:
            self.signal[name][0] = 1
        except KeyError:
            raise UnpublishedSignalError

    def unblock(self, name):
        "Allows a blocked signal to be emitted"
        try:
            self.signal[name][0] = 0
        except KeyError:
            raise UnpublishedSignalError

    
