###############################################################################
# $Id: filedlg.py,v 1.9 2004/08/16 16:47:24 pgs Exp $
#
# Project:  CIET Map
# Purpose:  Multi-purpose file selection dialog
# Author:   Paul Spencer, spencer@dmsolutions.ca
#
# Developed by DM Solutions Group (www.dmsolutions.ca) for CIETcanada
#
###############################################################################
# Copyright (c) 2000-2002, CIETcanada
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
#  $Log: filedlg.py,v $
#  Revision 1.9  2004/08/16 16:47:24  pgs
#  modified handling of filters to respect order in which they are specified when populating the dropdown list
#
#  Revision 1.8  2004/07/20 12:22:18  pgs
#  added patch from Zak James for handling manual input of filenames correctly
#
#  Revision 1.7  2003/09/13 22:09:41  pgs
#  changed add_with_viewport to add to prevent problem with many entries
#
#  Revision 1.6  2003/09/09 15:18:46  gmwalter
#  Update openev.py so that if default xml files are not present in xmlconfig
#  directory, old configuration is used.  Get rid of deprecation warnings
#  for python 2.3 by updating clist get_selection_info calls and colour
#  allocation (alloc) calls to use integers instead of floats.
#
#  Revision 1.5  2003/04/03 21:56:34  pgs
#  added localization support
#
#  Revision 1.4  2003/04/03 15:06:27  pgs
#  made filedlg safe if pygtkextra not installed
#
#  Revision 1.3  2003/02/14 17:58:35  pgs
#  added ability to multi-select files
#
#  Revision 1.2  2002/11/06 16:38:10  warmerda
#  minor fix to pref handling
#
#  Revision 1.1  2002/11/06 16:05:51  pgs
#  ported from CIETmap
#
#  Revision 1.38  2002/08/27 19:01:37  pspencer
#  made the filename widget type dependent on dialog type.
#
#  Revision 1.37  2002/08/15 18:01:49  pspencer
#  changed prints for ciet_utils.debug_msg()
#
#  Revision 1.36  2002/08/01 18:14:12  pspencer
#  updated copyright text
#
#  Revision 1.35  2002/08/01 15:24:03  warmerda
#  added fallback if pref_manager not available
#
#  Revision 1.34  2002/08/01 13:44:09  pspencer
#  put keypresses into the filename box
#
#  Revision 1.33  2002/07/30 02:53:38  pspencer
#  modified to use the new CmTopmostWindow base class to prevent conflicts
#  with message boxes that fight to be on top
#
#  Revision 1.32  2002/07/12 22:39:13  pspencer
#  added filters to file dialogs
#
#  Revision 1.31  2001/10/02 00:02:24  pspencer
#  modified for new preference manager architecture
#
#  Revision 1.30  2001/09/27 02:30:43  pspencer
#  changed Save to OK for FILE_SAVE
#
#  Revision 1.29  2001/09/21 21:30:51  pspencer
#  changed DIRECTORY_SELECT mode to display OK instead of Open
#
#  Revision 1.28  2001/08/29 20:27:49  pspencer
#  removed dependence on cmnormpath and modified directory listing
#  to not have '..' when at the root of a drive.
#
#  Revision 1.27  2001/08/29 18:46:32  pspencer
#  use cmnormpath to avoid  bug in ntpath.py
#
#  Revision 1.26  2001/07/01 03:15:12  pspencer
#  misc bug fixes
#
#  Revision 1.25  2001/06/06 02:51:56  pspencer
#  use pguentry
#
#  Revision 1.24  2001/05/24 14:03:44  pspencer
#  added case-insensitive filtering
#
#  Revision 1.23  2001/05/14 22:05:50  pspencer
#  added expanduser to file name expansion for linux users
#
#  Revision 1.22  2001/05/08 23:15:15  pspencer
#  minor change to update gui before loading files to allow for slow network
#  connections.
#
#  Revision 1.21  2001/05/05 17:35:26  pspencer
#  modifications to allow modal state to work properly under certain circumstances
#
#  Revision 1.20  2001/04/13 18:50:17  pspencer
#  fixed bug in help topic
#
#  Revision 1.19  2001/04/12 18:14:24  pspencer
#  implemented nls'd helpfiles and preferences.
#
#  Revision 1.18  2001/03/23 02:18:18  pspencer
#  fixed conflicts from merging v_1_1_4
#
#  Revision 1.17  2001/03/05 03:20:24  pspencer
#  fixed a bug in cwd not existing that was fixed earlier but got lost in a merge.
#
#  Revision 1.16  2001/03/01 14:04:16  pspencer
#  fixed conflicts during merge of bug fixes from v_1_1_3
#
#  Revision 1.15  2001/02/26 18:52:04  pspencer
#  fixed bug when gview working directory doesn't exist
#
#  Revision 1.14  2001/02/23 17:12:52  pspencer
#  Merged bug fixes from v_1_1_2
#
#  Revision 1.13.2.2  2001/02/28 18:11:43  pspencer
#  fixed a bug in the file dialog code (need to destroy it
#
#  Revision 1.13.2.1  2001/02/23 02:12:49  pspencer
#  fixed cwd, made dialog 'stay' on top.
#
#  Revision 1.13  2001/02/10 18:13:32  pspencer
#  added combo box for rfl and made filename editable.  when a path
#  is entered, the dialog switches to that path.
#
#  Revision 1.12  2001/02/08 17:41:44  pspencer
#  fixed (I hope) a bug in determining drive letters
#
#  Revision 1.11  2001/01/29 15:26:14  pspencer
#  missing import fixed
#
#  Revision 1.10  2001/01/24 18:54:07  warmerda
#  fixed FALSE and TRUE constants
#
#  Revision 1.9  2001/01/22 19:48:54  fredrock
#  adjusted self.set_policy(as=FALSE, ag=FALSE, autos=TRUE)
#
#  Revision 1.8  2001/01/20 20:00:53  pspencer
#  fixed directory sorting and added missing drive letters
#
#  Revision 1.7  2001/01/17 03:08:21  pspencer
#  editorial change
#
#  Revision 1.6  2000/10/20 16:23:08  pspencer
#  fixed bug in get_directory()
#
#  Revision 1.5  2000/10/19 22:46:26  pspencer
#  Modified to use os module for os specific path separators.  Removed
#  os.chdir() code so it no longer changes the working directory.
#
#  Revision 1.4  2000/10/19 05:15:38  warmerda
#  fixed some DOS path specific issues
#
#  Revision 1.3  2000/10/17 19:00:38  pspencer
#  made this a modal dialog
#
#  Revision 1.2  2000/10/09 14:02:59  pspencer
#  added comments and regular expressions for filter matching.
#
#  Revision 1.1  2000/10/08 17:17:55  pspencer
#  initial version
#
#

import os
import gtk
from gtk import TRUE, FALSE
from gvsignaler import Signaler
import gview
import string
from pguentry import pguEntry
try:
    from pgucombo import pguCombo
except:
    pguCombo = gtk.GtkCombo

#pguCombo = gtk.GtkCombo

import gdal
import nls
import re
import string

"""
This module contains a single class, FileDialog that presents a common interface
to several directory/file operations.

The class is initialized for file saving, file opening, or directory selection
through the dialog_type parameter of __init__.

FILE_OPEN -- allows the user to select an existing file

FILE_SAVE -- allows the user to pick an existing file or type a new one

DIRECTORY_SELECT -- allows the user to pick an existing directory

Usage -- connect signals to FileDialog.ok_button and FileDialog.cancel_button
      -- FileDialog.get_filename() returns the file name
      -- FileDialog.get_directory() returns the directory
      -- FileDialog.set_filter() sets a filter for file name that limits the
         display of files in the file list.
         
Filter specifications

A file filter is specified as a text string containing the filter name and 
filter items.  Filter items are separated by commas.  The filter name and
filter items are separated by a vertical bar |

Multiple filters are separated by a vertical bar

i.e. DBF (*.dbf)|*.dbf|REC (*.rec)|*.rec|All Files (*.*)|*.*
"""

#dialog_types
FILE_OPEN = 0
FILE_SAVE = 1
DIRECTORY_SELECT = 2


class FilterSpec:

    """
    implements a single filter
    """
    
    def __init__(self, filterspec):
        """
        Initialize the filter based on the spec string
        """
        #parse the filterspec
        parts = filterspec.split("|" )
        if len(parts) != 2:
            gdal.Debug( "OpenEV", "an error occurred parsing the FilterSpec %s" % filterspec )
            pass
        
        
        self.name = parts[0].strip()
        filters = parts[1].split( "," )
        
        self.filters = []
        for i in range(len(filters)):
            re_filter = string.replace(string.strip(filters[i]), "\\", "\\\\")
            re_filter = string.replace(re_filter, ".", "\.")
            re_filter = string.replace(re_filter, "*", ".*?")
            re_comp = re.compile(re_filter, re.I)
            self.filters.append( re_comp )
        
    def match(self, filename):
        """
        compare the filename to the filter spec and return None if not matched,
        otherwise the result of the match is returned
        """
        for i in range(len(self.filters)):
            result = self.filters[i].match( filename )
            if result is not None:
                return result
        return None


class FileDialog(gtk.GtkWindow, Signaler):
    """FileDialog provides a multipurpose file selection dialog."""

    def __init__(self, title=None, cwd=None, dialog_type=FILE_OPEN, filter=None, app=None, multiselect=0):
        gtk.GtkWindow.__init__(self)

        if dialog_type >= FILE_OPEN and dialog_type <= DIRECTORY_SELECT:
            self.dialog_type = dialog_type
        else:
            self.dialog_type = FILE_OPEN

        self.filter = None #current filter
        self.filters = {} #active filter objects
        self.filter_keys = [] #ordered list of the names of the filters
        
        self.file_selection = []
        
        self.multiselect = multiselect
                
        self.set_border_width(5)
        self.set_policy(as=gtk.FALSE, ag=gtk.FALSE, autos=gtk.TRUE)
        self.drives = None

        if title == None:
            if dialog_type == FILE_OPEN:
                title = nls.get('filedlg-title-open-file', 'Open File ...')
            elif dialog_type == FILE_SAVE:
                title = nls.get('filedlg-title-save-file', 'Save File ...')
            elif dialog_type == DIRECTORY_SELECT:
                title = nls.get('filedlg-title-select-directory', 'Select Directory ...')
        self.set_title(title)

        #setup the current working directory
        if cwd is None or not os.path.exists(cwd):
            cwd = gview.get_preference('working-directory')
            if cwd is None:
                cwd = os.getcwd()
        self.cwd = cwd
        
        #widgets
        vbox = gtk.GtkVBox(spacing=5)
        if dialog_type == FILE_OPEN or dialog_type == DIRECTORY_SELECT:
            lbl = gtk.GtkLabel(nls.get('filedlg-label-open-from', 'Open From:'))
        elif dialog_type == FILE_SAVE:
            lbl = gtk.GtkLabel(nls.get('filedlg-label-save-in', 'Save In:'))
        self.opt_menu = gtk.GtkOptionMenu()
        self.opt_menu.set_menu(gtk.GtkMenu())
        hbox = gtk.GtkHBox()
        hbox.pack_start(lbl, expand=gtk.FALSE)
        hbox.pack_start(self.opt_menu)
        vbox.pack_start(hbox, expand = gtk.FALSE)

        self.list_directory = gtk.GtkCList()
        scr_directories = gtk.GtkScrolledWindow()
        scr_directories.add(self.list_directory)
        self.list_directory.connect('button-press-event', self.directory_selected_cb)

        if dialog_type == DIRECTORY_SELECT:
            self.list_files = None
            vbox.pack_start(scr_directories)
        else:
            self.list_files = gtk.GtkCList()
            if self.multiselect:
                self.list_files.set_selection_mode( gtk.SELECTION_EXTENDED )
            scr_files = gtk.GtkScrolledWindow()
            scr_files.add(self.list_files)
            self.list_files.connect('button-press-event', self.file_clicked_cb)
            self.list_files.connect('select-row', self.file_selected_cb )
            self.list_files.connect('unselect-row', self.file_unselected_cb )
            pane = gtk.GtkHPaned()
            scr_directories.set_usize(100, -1)
            scr_files.set_usize(100, -1)
            pane.add1(scr_directories)
            pane.add2(scr_files)
            pane.set_position(200)
            vbox.pack_start(pane)

        widget = None
        if dialog_type == FILE_SAVE:
            self.txt_filename = gtk.GtkEntry()
            widget = self.txt_filename            
        
        elif dialog_type == FILE_OPEN:
            combo = gtk.GtkCombo()
            combo.set_value_in_list(gtk.FALSE, gtk.FALSE)
            combo.disable_activate()
            if app is not None:
                rfl = app.get_rfl()
                rfl.insert(0, '')
                combo.set_popdown_strings( rfl )
            self.txt_filename = combo.entry
            widget = combo
            
        if widget is not None:
            table = gtk.GtkTable(rows=2, cols=2)
            lbl = gtk.GtkLabel(nls.get('filedlg-label-file-name', 'File Name:'))
            self.txt_filename.connect('focus-out-event', self.map_path_cb)
            self.txt_filename.connect('key-press-event', self.map_path_cb)

            table.attach(lbl, 0, 1, 0, 1)
            table.attach(widget, 1, 2, 0, 1)
            lbl = gtk.GtkLabel(nls.get('filedlg-label-filter-extension', 'Filter extension:'))
            self.cmb_filter = pguCombo()
            self.set_filter(filter)
            self.cmb_filter.entry.connect('changed', self.filter_cb)
            table.attach(lbl, 0, 1, 1, 2)
            table.attach(self.cmb_filter, 1, 2, 1, 2)
            vbox.pack_start(table, expand=gtk.FALSE)

        if dialog_type == FILE_SAVE:
            self.ok_button = gtk.GtkButton(nls.get('filedlg-button-ok', 'OK'))
        elif dialog_type == FILE_OPEN:
            self.ok_button = gtk.GtkButton(nls.get('filedlg-button-open', 'Open'))
        elif dialog_type == DIRECTORY_SELECT:
            self.ok_button = gtk.GtkButton(nls.get('filedlg-button-ok', 'OK'))

        self.cancel_button = gtk.GtkButton(nls.get('filedlg-button-cancel', 'Cancel'))

        self.ok_button.connect('clicked', self.remove_grab)
        self.ok_button.connect('clicked', self.update_cwd)
        self.cancel_button.connect('clicked', self.remove_grab)
        btn_box = gtk.GtkHButtonBox()
        btn_box.pack_start(self.ok_button)
        btn_box.pack_start(self.cancel_button)
        vbox.pack_start(btn_box, expand=gtk.FALSE)

        self.add(vbox)
        self.show_all()
        
        #make modal
        gtk.grab_add(self)


        self.ok_button.set_flags(gtk.CAN_DEFAULT)
        self.ok_button.grab_default()

        self.set_usize(400, 400)
        self.menu_update = gtk.FALSE

        while gtk.events_pending():
            gtk.mainiteration(FALSE)

        self.refresh_directory()
        self.connect('delete-event', self.quit)
        self.ok_button.connect('clicked', self.quit)
        self.cancel_button.connect('clicked', self.quit)
        self.publish('quit')
        
        self.add_events(gtk.GDK.KEY_PRESS_MASK)
        self.connect('key-press-event', self.key_press_cb)

        self.result = 'cancel'

    def key_press_cb( self, widget, event ):
        """
        process key presses
        """
        #focus on cmdline and disable further processing of this signal
        self.txt_filename.grab_focus()    
        return FALSE
        
    def update_cwd(self, *args):
        #gview.set_preference('working-directory', self.cwd)
        pass

    def remove_grab(self, widget, *args):
        if widget == self.ok_button:
            self.result = 'ok'
        gtk.grab_remove(self)

    def refresh_directory(self, *args):
        """refresh the directory menu and cause a rebuild of the
        file/directory lists"""
        self.menu_update = gtk.TRUE
        self.opt_menu.remove_menu()
        paths = []
        drive, head = os.path.splitdrive(self.cwd)
        while head <> os.sep and head <> "":
            paths.append(drive + head)
            head, tail = os.path.split(head)

        paths.append(drive + os.sep)

        menu = gtk.GtkMenu()
        for path in paths:
            item = gtk.GtkMenuItem(path)
            item.show()
            item.connect('activate', self.directory_cb, path)
            menu.append(item)

        self.opt_menu.set_menu(menu)
        self.opt_menu.set_history(len(paths))
        self.refresh_files()
        self.menu_update = gtk.FALSE

    def map_path_cb(self, entry, event):
        """user has entered a value into txt_filename.  If it maps to
           a path, change to it"""
        if event.type == gtk.GDK.KEY_PRESS:
            if event.keyval == gtk.GDK.Return:
                path = os.path.normpath(os.path.join(self.cwd, entry.get_text()))
                path = os.path.expanduser(path)
                if os.path.isdir(path):
                    self.cwd = path
                    self.refresh_directory()
                    entry.set_text('')
            else:
                """for text entry deselect in list"""
                if len(self.file_selection) > 0:
                    self.file_selection = []
                    self.refresh_directory()
            
        elif event.type == gtk.GDK.FOCUS_CHANGE:
            if os.path.isdir(entry.get_text()):
                self.cwd = entry.get_text()
                self.refresh_directory()
                entry.set_text('')
            elif os.path.isfile(entry.get_text()):
                self.update_filename_box()



    def directory_cb(self, widget, path, *args):
        """called when the directory menu changes"""
        if not self.menu_update:
            self.cwd = os.path.normpath(path)
            self.refresh_directory()

    def refresh_files(self, *args):
        """rebuild the file and directory lists.  Use regular expressions to
        filter."""
        files = os.listdir(self.cwd)
        files.sort(self.cmp_dir)
        if self.list_files <> None:
            self.list_files.freeze()
            self.list_files.clear()
        self.list_directory.freeze()
        self.list_directory.clear()
        
        drive, path = os.path.splitdrive( self.cwd )
        if path != '\\':
            self.list_directory.append([os.pardir])

        for file in files:
            file_path = os.path.join(self.cwd, file)
            if os.path.isfile(file_path) and self.list_files <> None:
                if self.filter <> None:
                    match = self.filter.match(file_path)
                    if match <> None:
                    #f, ext = os.path.splitext(file)
                    #if ext == self.filter:
                        self.list_files.append([file])
                else:
                    self.list_files.append([file])
            elif os.path.isdir(file_path):
                self.list_directory.append([file])
        # add drive letters
        drives = self.get_drives()
        for drive in drives:
            self.list_directory.append([drive])

        if self.list_files <> None:
            self.list_files.thaw()
        self.list_directory.thaw()

    def file_clicked_cb(self, widget, event, *args):
        """called when the user selects a file in the file list"""
        if event.type == gtk.GDK._2BUTTON_PRESS:
            self.ok_button.clicked()
                        
    def file_selected_cb(self, widget, row, col, event, *args):
        """handle the user selecting a row"""
        try:
            idx = self.file_selection.index( row )
        except:
            self.file_selection.append( row )     
            self.update_filename_box()

    def file_unselected_cb( self, widget, row, col, event, *args):
        """handle the user unselecting a row"""
        try:
            self.file_selection.remove( row )
            self.update_filename_box()
        except:
            pass            
            
    def update_filename_box( self ):
        """update the contents of the filename box"""
        filenames = ""
        spc = ''
        if len(self.file_selection) > 1:
            quote='"'
        else:
            quote = ''
        for row in self.file_selection:
            filenames = filenames + spc + quote + "%s" % self.list_files.get_text( row, 0 ) + quote    
            spc = " "
        self.txt_filename.set_text(filenames)

    def directory_selected_cb(self, widget, event, *args):
        """called when the user selects a directory in the directory list"""
        if event.type <> gtk.GDK._2BUTTON_PRESS:
            return
        try:
            row, col = widget.get_selection_info(int(event.x), int(event.y))
        except:
            return

        new_dir = widget.get_text(row, col)
        self.cwd = os.path.normpath(os.path.join(self.cwd, new_dir))
        self.refresh_directory()

    def filter_cb(self, widget, *args):
        """called when the filter changes"""
        import string
        filter = string.strip(widget.get_text())
        if filter == '':
            self.filter = FilterSpec( nls.get("filedlg-default-filter", "All Files (*.*)|*.*"))
        else:
            self.filter = self.filters[filter]
        self.refresh_directory()

    def set_filter(self, filter):
        """programmatically set the filename filter"""
        
        self.filters = {}
        self.filter_keys = []
        self.filter = None
        #build the filters
        if filter != None and len(filter) > 0:
            filterSpecs = filter.split( "|" )
            if len(filterSpecs) % 2 != 0:
                gdal.Debug( "OpenEV", "invalid filter spec: %s" % filter )
                pass
            else:
                for i in range(0, len(filterSpecs), 2):
                    spec = FilterSpec(filterSpecs[i] + "|" + filterSpecs[i+1])
                    self.filters[spec.name] = spec
                    self.filter_keys.append( spec.name )
        else:
            self.filters[nls.get("filedlg-default-filter", "All Files (*.*)|*.*")] = FilterSpec( nls.get("filedlg-default-filter", "All Files (*.*)|*.*") )

        self.cmb_filter.set_popdown_strings( self.filter_keys )
        self.filter = self.filters[self.cmb_filter.entry.get_text()]
    
    def set_filename(self, filename):
        """set the filename"""
        self.txt_filename.set_text(filename)

    def get_filename(self, *args):
        """return the first filename"""
        if self.dialog_type == FILE_OPEN:
            if len(self.file_selection) > 0:
                filename = self.list_files.get_text( self.file_selection[0], 0 )
            elif len(self.txt_filename.get_text()) > 0:
                filename = self.txt_filename.get_text()
            else:
                filename = ""
        elif self.dialog_type == FILE_SAVE:
            filename = self.txt_filename.get_text()
        return os.path.join(self.get_directory(), filename)
        
    def get_filenames(self, *args):
        """return all the filenames as a list"""
        filenames = []
        for row in self.file_selection:
            filename = self.list_files.get_text( row, 0 )
            filenames.append( os.path.join(self.get_directory(), filename) )
            
        return filenames

    def get_directory(self, *args):
        """return the directory"""
        return self.cwd

    def get_drives(self, *args):
        if self.drives is None:
            self.drives = []
            for d in range(ord('c'), ord('z') + 1):
                drive = chr(d) + ':' + os.sep
                if os.path.exists(drive):
                    self.drives.append(drive)
        return self.drives

    def cmp_dir(self, a, b):
        if string.lower(a) < string.lower(b):
            return -1
        elif string.lower(a) == string.lower(b):
            return 0
        else:
            return 1

    def quit(self, *args):
        """close the dialog"""
        self.remove_grab(None)
        self.hide()
        self.notify('quit')
        return gtk.FALSE

if __name__ == '__main__':
    dlg = FileDialog(title='Testing', dialog_type=FILE_OPEN)
    dlg.show()
    dlg.subscribe('quit', gtk.mainquit)
    gtk.mainloop()
