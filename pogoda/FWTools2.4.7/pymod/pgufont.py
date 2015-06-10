#!/usr/bin/env python
###############################################################################
# $Id: pgufont.py,v 1.4 2004/07/20 12:26:43 pgs Exp $
#
# Project:  OpenEV Python GTK Utility classes
# Purpose:  Embeddable Font class and font utility classes
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
#  $Log: pgufont.py,v $
#  Revision 1.4  2004/07/20 12:26:43  pgs
#  added ability to load font and report statistics on it
#
#  Revision 1.3  2002/08/28 18:44:17  pgs
#  fixed typo from last change :(
#
#  Revision 1.2  2002/08/28 18:07:35  pgs
#  removed sys.stdout.flush() to prevent problems on windows with no console
#
#  Revision 1.1  2001/04/29 15:23:40  pgs
#  new file
#
#

import gtk
from gtk import TRUE, FALSE
import gview
from gvsignaler import Signaler
import string
import sys
import gdal


"""
pgufont contains utility classes for manipulating and selecting fonts
"""

class XLFDFontSpec:
    """
    encapsulate an X Logical Font Description (XLFD) font specification

    -adobe-helvetica-bold-r-normal--12-120-75-75-p-70-iso8859-1

    The fields in the XLFD are:

    Foundry          the company or organization where the font originated.
    Family           the font family (a group of related font designs).
    Weight           A name for the font's typographic weight For example,
                     'bold' or 'medium').
    Slant            The slant of the font. Common values are 'R' for Roman,
                     'I' for italoc, and 'O' for oblique.
    Set              Width A name for the width of the font. For example,
                     'normal' or 'condensed'.
    Add Style        Additional information to distinguish a font from other
                     fonts of the same family.
    Pixel Size       The body size of the font in pixels.
    Point Size       The body size of the font in 10ths of a point. (A point
                     is 1/72.27 inch)
    Resolution X     The horizontal resolution that the font was designed for.
    Resolution Y     The vertical resolution that the font was designed for .
    Spacing          The type of spacing for the font - can be 'p' for
                     proportional, 'm' for monospaced or 'c' for charcell.
    Average Width    The average width of a glyph in the font. For monospaced
                     and charcell fonts, all glyphs in the font have this width
    Charset Registry The registration authority that owns the encoding for the
                     font. Together with the Charset Encoding field, this
                     defines the character set for the font.
    Charset Encoding An identifier for the particular character set encoding.
    """

    xlfd_field_names = ['Foundry','Family','Weight',
                   'Slant','Set','Add Style','Pixel Size',
                   'Point Size','Resolution X','Resolution Y',
                   'Spacing','Average Width','Charset Registry',
                   'Charset Encoding']

    def __init__(self, fontspec = None):
        """
        initialize, optionally parsing a font spec
        """
        self.gdk_font = None
        self.parts = []
        for i in range(14):
            self.parts.append('*')
        if fontspec is not None:
            self.parse_font_spec(fontspec)

    def parse_font_spec(self, font_spec):
        """
        parse a font specification
        """
        self.gdk_font = None
        result = ''

        #coerce XLFDFontSpec classes into strings to parse them
        font_spec = str(font_spec)

        if font_spec[0:1] != '-':
            gdal.Debug( "pgufont", "invalid XLFD(%s), should start with -" % font_spec )
            return

        new_parts = string.split(font_spec, '-')
        del new_parts[0] #remove first (empty) part produced by split

        if len(new_parts) != 14:
            gdal.Debug( "pgufont", 'invalid XLFD(%s), should have 14 parts' % font_spec )
            return

        else:
            self.parts = new_parts

    def get_font_part(self, field_name=None, field_number=None):
        """
        Get one part of the font description by field name or number.  If
        both are specified, the result of the field name will be returned
        if it is valid, or if invalid, the field number, or if that is also
        invalid, the an empty string.
        """
        result = ''
        if field_number is not None:
            if field_number < 1 or field_number > 14:
                gdal.Debug( "pgufont", 'invalid field number (%s), should be 1-14' % field_number)
            else:
                result = self.parts[field_number]

        if field_name is not None:
            if self.xlfd_field_names.count(field_name) == 0:
                gdal.Debug( "pgufont", 'invalid field name (%s), should be one of %s' \
                    % (field_name, self.xlfd_field_names) )
            else:
                result = self.parts[self.xlfd_field_names.index(field_name)]

        return result

    def set_font_part(self, field_name, value):
        """
        set a part of the font description
        """
        self.gdk_font = None
        if self.xlfd_field_names.count(field_name) != 0:
            self.parts[self.xlfd_field_names.index(field_name)] = value
        else:
            gdal.Debug( "pgufont", 'invalid field name (%s), should be one of %s' \
                % (field_name, self.xlfd_field_names) )

    def get_display_string(self):
        """
        return a human readable display string for this font
        """
        family = self.get_font_part('Family') + ' '
        weight = self.get_font_part('Weight') + ' '
        if weight == '* ' or weight == 'normal ': weight = ''
        slant = self.get_font_part('Slant') + ' '
        if slant == '* ': slant = ''
        elif slant == 'r ': slant = ''
        elif slant == 'i ' or slant == 'o ': slant = 'Italic '

        unit = ' pt'
        size = self.get_font_part('Point Size')
        if size == '*' or size == '':
            size = self.get_font_part('Pixel Size')
            unit = ' px'
        else:
            size = size[0:len(size)-1]
        return family + weight + slant + size + unit

    def get_font_string(self):
        """
        return this font as a string (for cases where automatic coercion
        doesn't work ...)
        """
        return str(self)

    def __str__(self):
        """
        return a representation of this xfld as a string
        """
        result = ''
        for val in self.parts:
            result = result + '-' + val

        return result
        
    def load_font( self ):
        """
        load the real GDK font associated with this font spec so
        we can do calculations on it.
        """
        if self.gdk_font is not None:
            return
        self.gdk_font = gtk.load_font(str(self))

    def text_size( self, text ):
        """
        return the size (w,h) of a text string in the current font
        """
        self.load_font()
        w = self.gdk_font.width(text)
        h = self.gdk_font.height(text)
        return (w, h)
        
class pguFontDisplay(gtk.GtkDrawingArea):
    """
    a widget for displaying some text in a given font.
    """

    def __init__(self, text='Sample', font=None):
        """
        """
        gtk.GtkDrawingArea.__init__(self)
        self.size(10, 10)
        self.connect('expose-event', self.expose_event)
        self.connect('configure-event', self.configure_event)
        self.connect('realize', self.realize_event)
        self.connect('unrealize', self.unrealize_event)
        self.text = text
        self.font = font
        if font is not None:
            self.gdk_font = gtk.load_font(font)
        else:
            self.gdk_font = None

        self.set_events(gtk.GDK.BUTTON_PRESS_MASK)

    def realize_event(self, *args):
        pass

    def unrealize_event(self, *args):
        self.gdk_font = None
        pass

    def configure_event(self, *args):
        #is this required?
        return gtk.FALSE

    def expose_event(self, *args):
        #get the window and graphic context
        resize = FALSE

        if self.gdk_font is None:
            resize = TRUE
            if self.font is None:
                self.gdk_font = self.get_style().font
            else:
                self.gdk_font = gtk.load_font(self.font)

        w = self.gdk_font.width(self.text)
        h = self.gdk_font.height(self.text)

        if resize:
            self.set_usize(w + 6, h + 6)
            self.queue_draw()

        win = self.get_window()
        #self.draw_rectangle(self.get_style().black_gc, gtk.FALSE, 0, 0, win.width-1, win.height-1)
        self.draw_rectangle(self.get_style().white_gc, gtk.TRUE, 0, 0, win.width-1, win.height-1)
        self.draw_string(self.gdk_font, self.get_style().black_gc, 3, h+3, self.text)
        return gtk.FALSE

    def set_text(self, text):
        """
        set the text for this widget and resize if appropriate
        """
        if self.text == text:
            return

        self.text = text
        #try to resize.  If no font, wait for the next redraw
        if self.gdk_font is not None:
            w = self.gdk_font.width(self.text)
            h = self.gdk_font.height(self.text)
            self.set_usize(w + 6, h + 6)
        self.queue_draw()

    def set_font(self, font):
        self.font = font
        self.gdk_font = None
        self.queue_draw()

class pguFontControl(gtk.GtkHBox, Signaler):
    """
    an embeddable control for selecting fonts.  It displays the current
    font in a pguFontDisplay widget and provides a button to click to
    change the font.  If the widget is double-clicked, the displayed
    text will toggle between the default font and the selected font.

    Uses gvsignaler.Signaler to provide a 'font-changed' signal ... use
    font_control.subscribe('font-changed', call_back)

    Use font_control.get_font to retrieve an XLFDFontSpec object or
    font_control.get_font_string to get a font string.
    """

    def __init__(self, fontspec=None, use_font=FALSE):
        """
        Initialize the font selector and optionally load a previous
        font spec
        """
        gtk.GtkHBox.__init__(self)

        self.use_font = use_font
        self.font = XLFDFontSpec()

        tips = gtk.GtkTooltips()

        if fontspec is not None:
            self.font.parse_font_spec( fontspec )
        else:
            self.font.set_font_part('Family', 'Arial')
            self.font.set_font_part('Point Size', '100')

        table = gtk.GtkTable()
        self.pack_start(table)

        table.set_row_spacings(6)
        table.set_col_spacings(6)
        table.set_border_width(6)

        self.font_label = pguFontDisplay()
        self.font_label.set_text(self.font.get_display_string())
        table.attach(self.font_label, 0, 1, 0, 1, xoptions=gtk.SHRINK,
                    yoptions=gtk.SHRINK)
        tips.set_tip(self.font_label, 'double click to toggle sample mode')

        font_button = gtk.GtkButton('...')
        font_button.connect('clicked', self.show_font_dialog)
        table.attach(font_button, 1, 2, 0, 1, xoptions=gtk.SHRINK,
                    yoptions=gtk.SHRINK)
        tips.set_tip(font_button, 'click to select a different font')

        self.show_all()

        self.font_label.set_events(gtk.GDK.BUTTON_PRESS_MASK)
        self.font_label.connect('button-press-event', self.label_clicked)

        self.update_gui()
        self.publish('font-changed')

    def show_font_dialog(self, *args):
        """
        show the font selection dialog
        """
        dlg = gtk.GtkFontSelectionDialog('Select a font')
        dlg.set_font_name(str(self.font))
        dlg.ok_button.connect('clicked', self.update_font, dlg)
        dlg.cancel_button.connect('clicked', dlg.destroy)
        dlg.show()

    def update_font(self, widget, dlg):
        """
        update the font as a result of the user selecting a new one
        """
        self.set_font(dlg.get_font_name())
        dlg.destroy()

    def update_gui(self, *args):
        """
        update the GUI to reflect the state of the current font spec
        """
        #style = self.font_label.get_style().copy()
        #if self.use_font:
        #    style.font = gtk.load_font(str(self.font))
        #else:
        #    style.font = self.get_style().font
        if self.use_font:
            self.font_label.set_font(str(self.font))
        else:
            self.font_label.set_font(None)
        self.font_label.set_text(self.font.get_display_string())
        self.queue_resize()

    def set_font(self, fontspec):
        """
        set the font from the fontspec and update the gui
        """
        self.font.parse_font_spec(fontspec)
        self.update_gui()
        self.notify('font-changed')

    def get_font(self):
        """
        return the current font specification
        """
        #should this be a string or a font spec?
        return self.font

    def get_font_string(self):
        return str(self.font)

    def label_clicked(self, widget, event):
        """
        toggle the sample mode if the user double clicks on the label
        """
        if event.type == gtk.GDK._2BUTTON_PRESS:
            self.use_font = (self.use_font == FALSE)
            self.update_gui()


def print_font(widget,font_selector):
    """
    test case
    """
    font =  font_selector.get_font()
    print font

if __name__ == '__main__':
    """
    test case
    """

    dlg = gtk.GtkDialog()

    font_selector = pguFontControl(use_font=FALSE)
    font_selector.subscribe('font-changed', print_font, font_selector)
    dlg.vbox.pack_start(font_selector)

    ok = gtk.GtkButton('ok')
    dlg.action_area.pack_start(ok)
    ok.connect('clicked', gtk.mainquit)
    dlg.connect('delete-event', gtk.mainquit)
    dlg.show_all()
    gtk.mainloop()