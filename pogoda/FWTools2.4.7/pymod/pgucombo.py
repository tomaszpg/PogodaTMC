###############################################################################
# $Id: pgucombo.py,v 1.7 2005/11/08 15:51:44 andrey_kiselev Exp $
#
# Project:  CIET Map
# Purpose:  CIET Map
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
#  $Log: pgucombo.py,v $
#  Revision 1.7  2005/11/08 15:51:44  andrey_kiselev
#  Properly import gtkextra module, should work on Debian system now.
#
#  Revision 1.6  2004/09/28 17:50:42  warmerda
#  change fallback for how pygtkextra is imported
#
#  Revision 1.5  2003/11/19 15:20:53  warmerda
#  try looking in alternate location for pygtkextra if import fails
#
#  Revision 1.4  2002/08/13 12:44:15  pgs
#  made dropdown list scrollable and added capture of esc key to
#  close dropdown
#
#  Revision 1.3  2002/08/09 21:04:24  pgs
#  fixed bug in set_popdown_strings (make copy of list)
#
#  Revision 1.2  2002/08/01 14:49:37  pgs
#  modified, now dependent on gtkextra but much nicer control
#
#  Revision 1.1  2001/04/29 15:24:38  pgs
#  new file
#
#

import gtk
try:
    from pygtkextra import GtkComboBox
except:
    from gtkextra import GtkComboBox

"""
pgucombo contains a single class, pguCombo, which implements a better combobox
based on gtkextra's GtkComboBox (and the python bindings)
"""

class pguCombo(GtkComboBox):
    """
    this class mimics GtkCombo but the selection process is somewhat simpler
    and the entry box only changes when you actually select an item, not when
    you drag through it.
    """

    def __init__(self, strings = [ "" ]):
        """Initialize the combo box, default strings can be passed.
        """
        GtkComboBox.__init__(self)
        
        self.items = strings
        self.current_item = 0
        
        #widgets to go into the combo box
        self.list = gtk.GtkCList( cols=1 )
        self.list.set_selection_mode( gtk.SELECTION_SINGLE )
        
        self.entry = gtk.GtkEntry()
        self.entry.set_editable( gtk.FALSE )
        
        #fix up the style of the entry
        #style = self.entry.get_style().copy()

        #fake a background color the same as the button widget
        #for i in range(5):
        #    style.base[i] = self.button.get_style().bg[i]
        #self.entry.set_style( style )
        
        self._scrolled_win = gtk.GtkScrolledWindow()
        self._scrolled_win.set_policy( gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC )
        self._scrolled_win.add( self.list )

        #################################
        #
        # TODO: figure out how to resize this on the fly
        #
        #################################
        self._scrolled_win.set_usize( 150, 175 )
        self._scrolled_win.show_all()
        #frame is the popdown window frame
        self.frame.add( self._scrolled_win )
        
        #button is the main area to the left of the dropdown arrow
        self.button.add( self.entry )
        
        #initialize the widgets
        self.set_popdown_strings( self.items )
        self.select_item( self.current_item )
        
        #connect up signals
        self.list.connect( 'select-row', self.list_row_selected )
        
        self.list.add_events(gtk.GDK.KEY_PRESS_MASK)
        self.list.connect('key-press-event', self.key_press_cb)
        
        self.arrow.connect( 'toggled', self.toggle_cb )
        
        
        #make sure they all get shown
        self.show_all()     
        
        
    def toggle_cb( self, widget, *args ):
        if widget.get_active():
            self.list.grab_focus()
        else:
            self.entry.grab_focus()

    def key_press_cb( self, widget, event, *args ):
        """
        The user pressed a key.  Find out if we should respond to it
        """
        if event.keyval == gtk.GDK.Escape:
            self.hide_popdown_window()
        
    def list_row_selected( self, widget, row, col, event, *args ):
        """private callback for list selections
        """
        self.select_item( row )
        self.hide_popdown_window()
             
    def get_text( self ):
        """Return the text associated with the currently selected item
        """
        return self.items[ self.current_item ]
        
    def get_selected_item( self ):
        """Return the index of the selected item
        """
        return self.current_item
        
    def select_item( self, item = 0 ):
        """Select an item by it's index
        """
        if item >= 0 and item < len(self.items):
            self.current_item = item
            self.entry.set_text( self.items[self.current_item] )
            return gtk.TRUE
        else:
            return gtk.FALSE
    def select_string( self, string = "" ):
        """Cause an item to be selected by a string value
        """
        try:
            idx = self.items.index( string )
            self.select_item( idx )
            return gtk.TRUE
        except:
            return gtk.FALSE

    ############################################################################
    #
    # GtkCombo API
    #
    ############################################################################
    def set_popdown_strings( self, items ):
        """set the strings to display
        """
        del self.items
        self.items = []
        for item in items:
            self.items.append( item )
        self.list.clear()
        for item in self.items:
            self.list.append( [item] )
        self.list.set_column_width( 0, self.list.optimal_column_width( 0 ) )
        self.list.show_all()
        self.select_item( 0 )
        
    def disable_activate( self ):
        pass

    def set_use_arrows( self, val):
        pass

    def set_use_arrows_always( self, val ):
        pass

    def set_case_sensitive( self, val ):
        pass

    def set_value_in_list( self, val, ok_if_empty ):
        pass
    
class TestWindow( gtk.GtkWindow ):

    def __init__(self):
        gtk.GtkWindow.__init__(self)
        
        vbox = gtk.GtkVBox()
        self.add(vbox)
        
        self.cmb = pguCombo([ 'test1', 'test2', 'long test string' ])
        self.cmb.entry.connect( 'changed', self.item_changed )
        
        vbox.pack_start( self.cmb )
        
        self.connect( 'delete-event', gtk.mainquit )
        self.show_all()
        
    def item_changed( self, *args ):
        print self.cmb.get_text()
        
if __name__ == "__main__":
    win = TestWindow()
    gtk.mainloop()
