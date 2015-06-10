#!/usr/bin/env python
###############################################################################
# $Id: oeattedit.py,v 1.9 2003/02/20 19:27:23 gmwalter Exp $
#
# Project:  OpenEV
# Purpose:  Shape attribute display, and editing.
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
#  $Log: oeattedit.py,v $
#  Revision 1.9  2003/02/20 19:27:23  gmwalter
#  Updated link tool to include Diana's ghost cursor code, and added functions
#  to allow the cursor and link mechanism to use different gcps
#  than the display for georeferencing.  Updated raster properties
#  dialog for multi-band case.  Added some signals to layerdlg.py and
#  oeattedit.py to make it easier for tools to interact with them.
#  A few random bug fixes.
#
#  Revision 1.8  2002/11/14 15:43:14  gmwalter
#  Fixed a few bugs in the closing/reopening code.
#
#  Revision 1.7  2002/09/12 17:08:45  gmwalter
#  *** empty log message ***
#
#  Revision 1.6  2002/09/12 13:08:14  gmwalter
#  Updated oeattedit.py so that new fields can be added to shapefiles via the
#  gui.  Minor changes to aclocal.m4/configure to ensure that specified
#  libraries are picked up rather than defaults.
#
#  Revision 1.5  2002/07/12 12:46:06  warmerda
#  expanded tabs
#
#  Revision 1.4  2001/04/09 18:27:45  warmerda
#  upgraded to support subselection
#
#  Revision 1.3  2000/08/11 20:46:48  warmerda
#  get rid of horizontal scrollbar, fix original width
#
#  Revision 1.2  2000/08/04 14:10:48  warmerda
#  report shapeid in titlebar
#
#  Revision 1.1  2000/07/10 20:59:04  warmerda
#  New
#
#

from gtk import *
import gview
import string           
import gvselbrowser
import gvutils
import GtkExtra
import gvsignaler

def launch():
    try:
        gview.oeattedit.get_window()._raise()
        gview.oeattedit.show()
        gview.oeattedit.reconnect()
        gview.oeattedit.gui_update()
    except:
        try:
            # oeattedit has been created,
            # but not shown
            gview.oeattedit.show()
            gview.oeattedit.reconnect()
            gview.oeattedit.gui_update()
        except:    
            gview.oeattedit = OEAttEdit()
            gview.oeattedit.show()

    return gview.oeattedit

def launch_hidden():
    if not hasattr(gview,'oeattedit'):
        gview.oeattedit = OEAttEdit()
        
class OEAttEdit(GtkWindow,gvsignaler.Signaler):

    def __init__(self):
        GtkWindow.__init__(self)
        
        self.set_title('Shape Attributes')
        gview.app.sel_manager.subscribe( 'selection-changed',
                                         self.gui_update )
        gview.app.sel_manager.subscribe( 'subselection-changed',
                                         self.gui_update )

        # signal for external tools to connect to
        self.publish('hidden')
        self.publish('shown')
        
        self.text_contents = ''
        self.selected_shape = None
        self.layer = None
        self.create_gui()

        self.visibility_flag = 0
        self.gui_update()
        self.connect('delete-event', self.close)

    def show(self):
        GtkWindow.show(self)
        self.visibility_flag = 1
        self.notify('shown')

    def close(self, *args):
        gview.app.sel_manager.unsubscribe( 'selection-changed',
                                           self.gui_update )
        gview.app.sel_manager.unsubscribe( 'subselection-changed',
                                           self.gui_update )
        self.hide()
        self.visibility_flag = 0
        self.notify('hidden')
        
        return TRUE

    def reconnect(self, *args):
        gview.app.sel_manager.subscribe( 'selection-changed',
                                         self.gui_update )
        gview.app.sel_manager.subscribe( 'subselection-changed',
                                         self.gui_update )
        
    def create_gui(self):
        box1 = GtkVBox()
        self.add(box1)
        box1.show()

        self.selbrowser = gvselbrowser.GvSelBrowser()
        self.selbrowser.set_border_width(10)
        box1.pack_start( self.selbrowser, expand=FALSE )

        box2 = GtkVBox(spacing=10)
        box2.set_border_width(10)
        box1.pack_start(box2)
        box2.show()

        table = GtkTable(2, 2)
        table.set_row_spacing(0, 2)
        table.set_col_spacing(0, 2)
        box2.pack_start(table)
        table.show()

        text = GtkText()
        text.set_usize(400,100)
        text.set_line_wrap(FALSE)
        text.set_word_wrap(FALSE)
        text.set_editable(TRUE)
        table.attach(text, 0,1, 0,1)
        text.show()
        self.text = text
        self.text.connect('activate', self.att_update_cb)
        self.text.connect('leave-notify-event', self.att_update_cb)

        vscrollbar = GtkVScrollbar(text.get_vadjustment())
        table.attach(vscrollbar, 1,2, 0,1, xoptions=FILL)
        vscrollbar.show()


        separator = GtkHSeparator()
        box1.pack_start(separator, expand=FALSE)
        separator.show()

        box2 = GtkVBox(spacing=10)
        box2.set_border_width(10)
        box1.pack_start(box2, expand=FALSE)
        box2.show()

        # new field options
        box3 = GtkHBox(spacing=10)
        box3.set_border_width(10)
        nf_frame = GtkFrame('New field properties: type/width/precision')
        nf_frame.add(box3)
        self.new_field_width_entry = GtkEntry(2)
        self.new_field_width_entry.set_text('20')
        self.new_field_width_entry.set_editable(TRUE)        
        self.new_field_precision_entry = GtkEntry(2)
        self.new_field_precision_entry.set_text('0')
        self.new_field_precision_entry.set_editable(FALSE)
        self.new_field_precision_entry.set_sensitive(FALSE)
        
        self.new_field_types = ('string','integer','float')
        self.new_field_type_menu = gvutils.GvOptionMenu(self.new_field_types, self.new_field_precision_cb)
        self.new_field_type_menu.set_history(0)
        box3.pack_start(self.new_field_type_menu)
        box3.pack_start(self.new_field_width_entry,expand=FALSE,fill=FALSE)
        box3.pack_start(self.new_field_precision_entry,expand=FALSE,fill=FALSE)
        box2.pack_start(nf_frame)
        nf_frame.show_all()
        
        button = GtkButton("close")
        button.connect("clicked", self.close)
        box2.pack_start(button)
        button.set_flags(CAN_DEFAULT)
        button.grab_default()
        button.show()

    def new_field_precision_cb(self,*args):
        if self.new_field_types[self.new_field_type_menu.get_history()] == 'float':
            # precision is only relevant for float
            self.new_field_precision_entry.set_editable(TRUE)
            self.new_field_precision_entry.set_sensitive(TRUE)
        else:
            self.new_field_precision_entry.set_text('0')
            self.new_field_precision_entry.set_editable(FALSE)
            self.new_field_precision_entry.set_sensitive(FALSE)
            
    def gui_update(self,*args):
        self.text_contents = ''
        self.text.freeze()
        self.text.delete_text(0,-1)

        self.selected_shape = None

        try:
            self.layer = gview.app.sel_manager.get_active_layer()
            shapes = self.layer.get_parent()
            self.selected_shape = self.layer.get_subselected()
            properties = shapes[self.selected_shape].get_properties()
            for att_name in properties.keys():
                self.text_contents = self.text_contents + \
                        att_name + ': ' + properties[att_name] + '\n'
            self.text.insert_defaults(self.text_contents)
        except:
            pass

        self.text.thaw()

    def att_update_cb(self,*args):
        if self.text_contents == self.text.get_chars(0,-1):
            return

        if self.selected_shape is None:
            return

        shapes = self.layer.get_parent()
        shape = shapes[self.selected_shape]
        if shape is None:
            return

        shape = shape.copy()
        
        lines = string.split(self.text.get_chars(0,-1),'\n')
        for line in lines:
            tokens = string.split(line,':',1)
            if len(tokens) == 2:
                value = string.strip(tokens[1])
                shape.set_property(tokens[0],value)
                property_exists=0
                for cprop in shapes.get_schema():
                    if cprop[0] == tokens[0]:
                        property_exists=1
                if property_exists != 1:
                    ftype = self.new_field_types[self.new_field_type_menu.get_history()]
                       
                    response = \
                       GtkExtra.message_box('Confirmation',
                         'Create new ' + ftype + '-type property ' + tokens[0] + '?' ,
                                            ('Yes','No'))
                    if response == 'Yes':
                        try:
                            fwidth = int(self.new_field_width_entry.get_text())
                        except:
                            gvutils.error('Field width must be an integer!')
                            continue
                        
                        if ftype == 'float':
                            try:
                                fprec = int(self.new_field_width_entry.get_text())
                            except:
                                gvutils.error('Precision width must be an integer!')
                                continue
                        else:
                            fprec = 0
                            
                        shapes.add_field(tokens[0],ftype,fwidth,fprec)

        shapes[self.selected_shape] = shape
        self.gui_update()

    def insert_text_cb(self,new_text,*args):
        if new_text[0] == '\n':
            self.att_update_cb()
            return FALSE
