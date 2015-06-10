###############################################################################
# $Id: pgucolourswatch.py,v 1.3 2003/09/09 15:18:46 gmwalter Exp $
#
# Project:  Python Gtk Utility Widgets
# Purpose:  Embeddable color swatch.
# Author:   Paul Spencer, pgs@magma.ca
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
#  $Log: pgucolourswatch.py,v $
#  Revision 1.3  2003/09/09 15:18:46  gmwalter
#  Update openev.py so that if default xml files are not present in xmlconfig
#  directory, old configuration is used.  Get rid of deprecation warnings
#  for python 2.3 by updating clist get_selection_info calls and colour
#  allocation (alloc) calls to use integers instead of floats.
#
#  Revision 1.2  2001/03/19 21:57:14  warmerda
#  expand tabs
#
#  Revision 1.1  2000/07/26 21:20:01  warmerda
#  New
#
#

import gtk
from gvsignaler import Signaler

class ColourSwatch(gtk.GtkDrawingArea, Signaler):
    '''
    Class ColourSwatch is a simple widget that
    displays a colour.
    
    The colour attribute is an RGBA tuple.  Internally, however,
    a GdkColour object is used that has values in the range 0-65535
    for red, green and blue.      
    '''
    def __init__(self, colour=(0,0,0,0)):
        gtk.GtkDrawingArea.__init__(self)
        self.size(30, 15)
        self.connect('configure-event', self.configure_event)
        self.connect('expose-event', self.expose_event)
        self.connect('realize', self.realize_event)
        self.connect('unrealize', self.unrealize_event)
        self.colour = colour
        #the color - use GdkColourMap's alloc method to get it
        cm = self.get_colormap()
        self.icolour = cm.alloc(int(colour[0] * 65535),
                                int(colour[1] * 65535),
                                int(colour[2] * 65535))
        self.publish('colour-changed')
        #cached graphics context
        self.gc = None
        
    def realize_event(self, *args):
        self.gc = self.get_window().new_gc(foreground=self.icolour)

    def unrealize_event(self, *args):
        #don't know the correct way to destroy a gc yet
        #self.gc.destroy()
        pass
                
    def configure_event(self, *args):
        #is this required?
        return gtk.FALSE

    def expose_event(self, *args):
        #get the window and graphic context 
        win = self.get_window()
        self.draw_rectangle(self.get_style().black_gc, gtk.FALSE, 2, 2, win.width-2, win.height-2)
        self.draw_rectangle(self.gc, gtk.TRUE, 3, 3, win.width-3, win.height-3)
        return gtk.FALSE
        
    def set_colour(self, colour=(0,0,0,0)):
        self.colour = colour
        #the color - use GdkColourMap's alloc method to get it
        cm = self.get_colormap()
        self.icolour = cm.alloc(int(colour[0] * 65535),
                                int(colour[1] * 65535),
                                int(colour[2] * 65535))
        if self.gc is not None:
                self.gc.foreground = self.icolour
        self.notify('colour-changed')
        if self.flags() & gtk.REALIZED:
            self.expose_event()

