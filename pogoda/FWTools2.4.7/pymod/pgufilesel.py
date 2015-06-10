###############################################################################
# $Id: pgufilesel.py,v 1.1 2000/06/14 13:57:30 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  Simplified File Selection API.
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
#  $Log: pgufilesel.py,v $
#  Revision 1.1  2000/06/14 13:57:30  warmerda
#  New
#
#

import gtk; _gtk = gtk; del gtk
from string import *
import os.path

simple_file_sel = None
simple_file_sel_dir= None

def SFSOkCB( item, cb, cb_data ):
    global simple_file_sel

    simple_file_sel.hide()
    cb( os.path.normpath(simple_file_sel.get_filename()), cb_data )

def SFSCancelCB( item, cb, cb_data ):
    global simple_file_sel

    simple_file_sel.hide()
    if cb is not None:
        cb( cb_data )

def SFSDestroyCB( item, cb, cb_data ):
    global simple_file_sel

    simple_file_sel = None
    if cb is not None:
        cb( cb_data )

def SimpleFileSelect( ok_cb,
                         cb_data = None,
                         title = None,
                         default_filename = None,
                         cancel_cb = None,
                         help_topic = None ):

    """Simplified File Selection

    This method launches a file selector, and calls the caller supplied
    OK callback when the user selects a file.  Creation, tailoring and
    cleanup of the GtkFileselection is managed internally.

    Arguments:

    ok_cb -- callback to call when user selects a file.  It should take
    a filename and cb_data argument.

    cb_data -- extra data to pass to ok, and cancel callbacks.  Defaults to
    None.

    title -- the title to use for the dialog.  Defaults to nothing.

    default_filename -- the initial filename to be shown in the file selector.
    Defaults to no file, and the current (or last accessed) directory.

    cancel_cb -- callback called when the user hits the cancel button or
    closes the file selection dialog.  If defaulted the caller isn't notified
    of cancels.  If supplied, the callback should take one argument which is
    the callback data.

    Example:

    The following code launches a simple file selector, and does an action
    in the callback.  The title, and default filename are set, but
        pgufilesel.SimpleFileSelect( self.save_vector_layer_with_file,
                                     cb_data = layer.get_parent(),
                                     title = 'Shapefile To Save to',
                                     default_filename = layer.get_name() )

    def save_vector_layer_with_file( self, filename, shapes_data ):
        shapes_data.save_to( filename )

    """

    global simple_file_sel

    if simple_file_sel is not None:
        simple_file_sel.destroy()

    simple_file_sel = _gtk.GtkFileSelection()
    simple_file_sel.hide_fileop_buttons()
    simple_file_sel.ok_button.connect('clicked', SFSOkCB, ok_cb, cb_data )
    simple_file_sel.cancel_button.connect('clicked', SFSCancelCB, cancel_cb, cb_data )
    simple_file_sel.connect('destroy', SFSDestroyCB, cancel_cb, cb_data)

    if title is not None:
        simple_file_sel.set_title( title )

    if default_filename is not None:
        simple_file_sel.set_filename( default_filename )
    else:
        if simple_file_sel_dir is not None:
            simple_file_sel.set_filename(simple_file_sel_dir)

    if help_topic is not None:
        import gvhtml
        gvhtml.set_help_topic( simple_file_sel, help_topic )


    simple_file_sel.show()


def SimpleFileSelectCB( item, ok_cb, *args ):

    """Simple file selection suitable to use as a callback.

    This function is suitable to be used as a callback from a menu item,
    and will launch a file selector, using the SimpleFileSelect() API.
    See that function for details on meaning of arguments.

    The callback should be passed one, two or three arguments which
    would be the SimpleFileSelect() arguments ok_cb, cb_data and title.

    Example:

    The following fragment passed to GtkExtra.MenuFactory creates a File
    Open menu item, and it launches a file selector.  When a file is called
    the caller supplied self.file_open_by_name() method is called.
    
            ('File/Open', '<control>O', pgufilesel.SimpleFileSelectCB,
                                        self.file_open_by_name ),

    def file_open_by_name(self, filename, *args):
        ...
                                        
    """

    if len(args) == 0: 
        SimpleFileSelect( ok_cb )
    elif len(args) == 1:
        SimpleFileSelect( ok_cb, cb_data = args[0] )
    else:
        SimpleFileSelect( ok_cb, cb_data = args[2], title = args[0] )


# For directly grabbing a filename within a single callback
class pguFileSelection(_gtk.GtkFileSelection):
    def __init__(self, title, default_filename = None):
        _gtk.GtkFileSelection.__init__(self)
        self.set_title(title)
        if default_filename is not None:
            self.set_filename(default_filename)

        elif simple_file_sel_dir is not None:
            self.set_filename(simple_file_sel_dir)
            
        self.ok_button.connect  ("clicked", self.ok_cb)
        self.cancel_button.connect("clicked", self.cancel_cb)
        self.connect("delete_event", self.cancel_cb)
        self.ret = None
        self.set_modal(_gtk.TRUE)

    def ok_cb(self, *args):
        self.ret = self.get_filename()
	self.hide()
	self.destroy()
	_gtk.mainquit()

    def cancel_cb(self, *args):
        self.ret = None
        self.selected = None
	self.hide()
	self.destroy()
	_gtk.mainquit()
	

def GetFileName(title = 'Select File', default_filename = None):
    win = pguFileSelection(title, default_filename)
    win.show_all()
    _gtk.mainloop()
    return win.ret

