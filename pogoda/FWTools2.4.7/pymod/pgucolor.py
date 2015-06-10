###############################################################################
# $Id: pgucolor.py,v 1.12 2003/09/09 15:18:46 gmwalter Exp $
#
# Project:  Python Gtk Utility Widgets
# Purpose:  Color-related widgets and utilities.
# Author:   Paul Spencer, pgs@magma.ca
#
###############################################################################
# Copyright (c) 2000, DM Solutions Group Inc. (www.dmsolutions.on.ca)
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
#  $Log: pgucolor.py,v $
#  Revision 1.12  2003/09/09 15:18:46  gmwalter
#  Update openev.py so that if default xml files are not present in xmlconfig
#  directory, old configuration is used.  Get rid of deprecation warnings
#  for python 2.3 by updating clist get_selection_info calls and colour
#  allocation (alloc) calls to use integers instead of floats.
#
#  Revision 1.11  2002/08/09 21:04:48  pgs
#  added support for DISCRETE color ramps
#
#  Revision 1.10  2001/09/17 15:26:33  pgs
#  moved more GtkColorWell code into gtkmissing.
#
#  Revision 1.9  2001/09/17 03:44:40  pgs
#  added get_color to ColorButton
#
#  Revision 1.8  2001/09/17 03:41:52  pgs
#  removed GtkColorWell (moved to gtkmissing) and added __init__ to
#  ColorButton to initialize a standard color button.
#
#  Revision 1.7  2001/09/16 03:28:37  pgs
#  Added GtkColorWell class (should be in GtkMissing?) and modified ColorButton
#  to derive from it.
#
#  Revision 1.6  2001/05/08 23:37:07  pgs
#  fixed bug allowing multiple color choosers for a single color button
#
#  Revision 1.5  2001/04/14 14:52:28  pgs
#  added color_string_to_tuple
#
#  Revision 1.4  2001/04/11 03:04:51  pgs
#  added get_color() to color swatch and opacity to ColorDialog
#
#  Revision 1.3  2000/09/28 22:45:15  pgs
#  fixed up ColorRamp
#
#  Revision 1.1  2000/09/27 13:32:33  warmerda
#  New
#
#

MIN_COLOR=0
MAX_COLOR = 65535

import gtk
from gtk import TRUE, FALSE
import GDK
from gvsignaler import Signaler
import _gv
from gtkmissing import GtkColorWell

def color_string_to_tuple(s):
    from string import replace, split
    s = replace(s, '(', '')
    s = replace(s, ')', '')
    s = replace(s, ',', '')
    r, g, b, a = split(s, None)
    return (float(r), float(g), float(b), float(a))


class ColorSwatch(gtk.GtkDrawingArea, Signaler):
    """
    Class ColorSwatch is a simple widget that
    displays a color.

    The color attribute is an RGBA tuple.  Internally, however,
    a GdkColor object is used that has values in the range 0-65535
    for red, green and blue.  The color display doesn't support
    the alpha channel (yet?)

    Don't use GdkColor(red, green, blue) to allocate colors ... use
    GdkColormap.alloc instead and get a reference to the GdkColormap
    from the widget (self.get_colormap())
    """
    def __init__(self, color=(0,0,0,0)):
        gtk.GtkDrawingArea.__init__(self)
        self.size(20, 15)
        self.connect('configure-event', self.configure_event)
        self.connect('expose-event', self.expose_event)
        self.connect('realize', self.realize_event)
        self.connect('unrealize', self.unrealize_event)
        self.color = color
        #the color - use GdkColorMap's alloc method to get it
        cm = self.get_colormap()
        self.icolor = cm.alloc(int(color[0] * MAX_COLOR), \
                               int(color[1] * MAX_COLOR), \
                               int(color[2] * MAX_COLOR))
        self.publish('color-changed')
        #cached graphics context
        self.gc = None

    def realize_event(self, *args):
        self.gc = self.get_window().new_gc(foreground=self.icolor)

    def unrealize_event(self, *args):
        #remove references to the gc to prevent leaks?
        self.gc = None

    def configure_event(self, *args):
        #is this required?
        return gtk.FALSE

    def expose_event(self, *args):
        #get the window and graphic context
        win = self.get_window()
        self.draw_rectangle(self.get_style().black_gc, gtk.FALSE, 0, 0, win.width-1, win.height-1)
        self.draw_rectangle(self.gc, gtk.TRUE, 1, 1, win.width-2, win.height-2)
        return gtk.FALSE

    def set_color(self, color=(0,0,0,0)):
        self.color = color
        #the color - use GdkColorMap's alloc method to get it
        cm = self.get_colormap()
        self.icolor = cm.alloc(int(color[0] * 65535), int(color[1] * 65535),
                               int(color[2] * 65535))
        if self.gc is not None:
            self.gc.foreground = self.icolor
        self.queue_draw()
        self.notify('color-changed')

    def get_color(self):
        return self.color


class ColorButton(GtkColorWell):
    """
    Class ColourButton extends GtkColorWell
    """

    def __init__(self, color=(0,0,0,0), title='', use_alpha=TRUE, continuous=FALSE, _obj=None):
        GtkColorWell.__init__(self, _obj)
        self.set_color( color )
        self.set_use_alpha( use_alpha )
        self.set_continuous( continuous )

class ColorDialog(gtk.GtkWindow):
    """used with a ColorButton when it is clicked"""

    def __init__(self, ok_cb = None, cancel_cb = None, cb_data = None):
        gtk.GtkWindow.__init__(self)
        self.set_title('Select a Color')
        vbox = gtk.GtkVBox(spacing=3)
        self.add(vbox)
        self.user_ok_cb = ok_cb
        self.user_cancel_cb = cancel_cb
        self.user_cb_data = cb_data

        self.connect('delete-event', self.user_cancel_cb)
        #add the color selection widget
        self.colorsel = gtk.GtkColorSelection()
        self.colorsel.set_opacity(gtk.TRUE)
        vbox.pack_start(self.colorsel)
        #add the ok and cancel buttons
        button_box = gtk.GtkHButtonBox()
        ok_button = gtk.GtkButton("OK")
        ok_button.connect('clicked', self.ok_cb, cb_data)
        cancel_button = gtk.GtkButton("Cancel")
        cancel_button.connect('clicked', self.cancel_cb, cb_data)
        button_box.pack_start(ok_button)
        button_box.pack_start(cancel_button)
        vbox.pack_start(button_box, expand=gtk.FALSE)
        vbox.show_all()
        ok_button.set_flags(gtk.CAN_DEFAULT)
        ok_button.grab_default()

    def ok_cb(self, *args):
        if self.user_ok_cb is not None:
            self.user_ok_cb(self.user_cb_data, self)
        self.hide()
        self.destroy()

    def cancel_cb(self, *args):
        if self.user_cancel_cb is not None:
            self.user_cancel_cb(self.user_cb_data, self)
        self.hide()
        self.destroy()

RAMP_GRADIENT = 0
RAMP_DISCRETE = 1

class ColorRamp(gtk.GtkFrame, Signaler):
    """encapsulate the functionality of a color ramp that
    can apply itself in a linearly interpolated number of
    steps between several colors positioned along the ramp

    Colors can be returned from the ramp by calling apply_ramp
    with a callback and the number of colors to calculate.
    """
    def __init__(self):
        """initialize the ramp
        """
        gtk.GtkFrame.__init__(self)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.colors = []
        self.gradient = ColorGradientSwatch(self)
        self.title = gtk.GtkLabel('Ramp')
        fix = gtk.GtkFixed()
        fix.put(self.gradient, 1, 0)
        fix.put(self.title, 84, 0)
        self.add(fix)
        self.type = RAMP_GRADIENT

    def serialize(self, fname = None):
        """save to a file
        """
        
        result = "%s\n" % self.title.get()
        result = result + "%s\n" % self.type
        for n in self.colors:
            if self.type == RAMP_GRADIENT:
                result = result + "%s %s\n" % (str(n[0]), str(n[1]))
            else:
                result = result + "%s\n" % str(n[1])
                
        if fname is not None:
            f = open(fname, 'w')
            f.write( result )
            f.close()
        else:
            return result      

    def deserialize(self, fname):
        """read from a file"""
        import string
        fp = open(fname, 'r')
        lines = fp.readlines()
        self.title.set_text(lines[0].strip())
        self.type = int(lines[1].strip())
        n_colors = len( lines[2:] )
        for i in range(n_colors):
            line = lines[2+i]
            line = string.replace(line, '(', '')
            line = string.replace(line, ')', '')
            line = string.replace(line, ',', '')
            if self.type == RAMP_GRADIENT:
                pos, r, g, b, a = line.split()
            else:
                r, g, b, a = line.split()
                #assume equally spaced for DISCRETE
                pos = float(i)/float(n_colors - 1)
            self.add_color((float(r), float(g), float(b), float(a)), float(pos))

        fp.close()
        self.queue_draw()

    def add_color(self, color, position):
        """add a color to the ramp at the given position.
        color - an rgba tuple
        position - between 0.0 and 1.0
        """
        for i in range(len(self.colors)):
            if position <= self.colors[i][0]:
                self.colors.insert(i, (position, color))
                break
        else:
            self.colors.append((position, color))

    def apply_ramp(self, color_cb, ncolors):
        """
        return ncolors spread over the ramp by
        calling the color_cb callback with the
        current position (in the range 0 to
        ncolors-1) and color
        """
        if len(self.colors) == 0:
            return

        #insert false entries at 0 and 1 if necessary
        bLow = gtk.FALSE
        bHi = gtk.FALSE

        if self.colors[0][0] <> 0.0:
            self.add_color(self.colors[0][1], 0.0)
            bLow = gtk.TRUE
        if self.colors[len(self.colors) - 1][0] <> 1.0:
            self.add_color(self.colors[len(self.colors)-1][1], 1.0)
            bHi = gtk.TRUE
        
        if ncolors > 1:
            for i in range(ncolors):
                if self.type == RAMP_GRADIENT:
                    color_cb(i, self.calculate_color(float(float(i)/float(ncolors - 1))))
                elif self.type == RAMP_DISCRETE:
                    pos = i % len(self.colors)
                    color_cb(i, self.colors[pos][1] )
                    
        else:
            color_cb( 0, self.calculate_color( 0 ) )
            
        #clean up
        if bLow:
            del self.colors[0]
        if bHi:
            del self.colors[len(self.colors)-1]

    def calculate_color(self, pos):
        """calculate the color at the given position.  If a color
        exists at the position, return it. Otherwise get the color
        before and after it and calculate a linear interpolation
        between them.
        """
        for i in range(len(self.colors)-1):
            below = self.colors[i]
            above = self.colors[i+1]
            if below[0] <= pos and above[0] >= pos:
                fr = below[1][0]
                fg = below[1][1]
                fb = below[1][2]
                fa = below[1][3]
                tr = above[1][0]
                tg = above[1][1]
                tb = above[1][2]
                ta = above[1][3]
                delta = (pos - below[0]) / (above[0] - below[0])
                cr = fr + ( tr - fr ) * delta
                cg = fg + ( tg - fg ) * delta
                cb = fb + ( tb - fb ) * delta
                ca = fa + ( ta - fa ) * delta
                return (cr, cg, cb, ca)

    def get_color_list(self, ncolors):
        self.color_list = []
        self.apply_ramp(self.color_list_cb, ncolors)
        return self.color_list

    def color_list_cb(self, num, color):
        self.color_list.insert(num, color)

class ColorGradientSwatch(ColorSwatch):
    """
    Class ColorGradientSwatch extends ColorSwatch to n colors
    and draws itself as a gradient between the various colors.

    This class is intended primarily to provide a GUI element for
    ColorRamps
    """
    def __init__(self, ramp):
        ColorSwatch.__init__(self)
        self.size(80, 15)
        self.ramp = ramp

    def expose_event(self, *args):
        #get the window and graphic context
        win = self.get_window()
        self.width = win.width
        self.height = win.height
        self.cm = self.get_colormap()
        if self.ramp.type == RAMP_GRADIENT:
            colors = self.ramp.get_color_list(self.width)
        else:
            colors = self.ramp.get_color_list( len(self.ramp.colors) - 1 )
        bar_width = self.width / len(colors)
        i = 0
        for color in colors:
            self.gc.foreground = self.cm.alloc(int(color[0] * MAX_COLOR),
                                               int(color[1] * MAX_COLOR),
                                               int(color[2] * MAX_COLOR))
            self.draw_rectangle(self.gc, gtk.TRUE, i, 0, bar_width, self.height)
            i = i + bar_width
        self.draw_rectangle(self.get_style().black_gc, gtk.FALSE, 0, 0, win.width-1, win.height-1)
        return gtk.FALSE


def test_cb(num, color):
    print num, ' - ', color

def color_set( widget, obj ):
    print 'color set to ', widget.get_color()

if __name__ == '__main__':
    a = ColorRamp()
    a.add_color((0.0,1.0,0.0,1.0), 0.0)
    a.add_color((1.0,1.0,0.0,1.0), 0.50)
    a.add_color((1.0,0.0,0.0,1.0), 1.0)
    print a.colors
    a.apply_ramp(test_cb, 5)
    print a.colors
    a.serialize('c:\\test_ramp')
    b = ColorRamp()
    b.deserialize('c:\\test_ramp')
    print b.colors

    c = ColorButton((1.0, 0.0, 0.0, 1.0))
    c.connect('color-set', color_set)

    dlg = gtk.GtkDialog()
    btn = gtk.GtkButton('OK')
    btn.connect('clicked', gtk.mainquit)

    dlg.vbox.pack_start(a)
    dlg.vbox.pack_start(b)
    dlg.vbox.pack_start(c)
    dlg.action_area.pack_start(btn)
    dlg.show_all()
    dlg.show()

    gtk.mainloop()
