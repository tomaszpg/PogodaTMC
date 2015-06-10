###############################################################################
# $Id: pgumenu.py,v 1.3 2002/08/13 16:09:29 pgs Exp $
#
# Project:  OpenEV
# Purpose:  Extended Menu handling classes
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
#  $Log: pgumenu.py,v $
#  Revision 1.3  2002/08/13 16:09:29  pgs
#  added a pguToggleMenuItem and an option in the menu factory for adding
#  a <toggle> menu item.
#
#  Revision 1.2  2002/07/23 17:29:21  warmerda
#  Recover if menu pixmap not found.
#
#  Revision 1.1  2001/05/02 03:32:18  pgs
#  new file
#
#

import gtk
from gtk import TRUE, FALSE
import string
import os
import gview
import pgu

MENU_FACTORY_MENU_BAR    = 0
MENU_FACTORY_MENU        = 1
MENU_FACTORY_OPTION_MENU = 2

# type is MENU_FACTORY_{MENU,MENU_BAR,OPTION_MENU}
class pguMenuFactory:
    """
    Utility class for creating different kinds of menus.  Taken verbatim
    from the pygtk MenuFactory class in GtkExtra.py with an enhancement
    to add images to the menu and with comments added.

    TODO:
    right now, all menu items are indented by a spacing factor of 22 pixels
    if no image is specified (to make everything line up.  This means that
    any images put in the menu should be 22 pixels wide.

    """

    def __init__(self, type=MENU_FACTORY_MENU_BAR):
        """
        Initialize the menu factory
        """
        self.accelerator = gtk.GtkAccelGroup()
        if type == MENU_FACTORY_MENU_BAR:
            self.__w = gtk.GtkMenuBar()
            self.__ret = self.__w
        elif type == MENU_FACTORY_MENU:
            self.__w =gtk. GtkMenu()
            self.__w.set_accel_group(self.accelerator)
            self.__ret = self.__w
        elif type == MENU_FACTORY_OPTION_MENU:
            self.__w = gtk.GtkMenu()
            self.__w.set_accel_group(self.accelerator)
            self.__ret = gtk.GtkOptionMenu()
            self.__ret.set_menu(self.__w)
        self.__menus = {}
        self.__items = {}

    def __getattr__(self, key):
        """
        map getattr calls through to the menu instead of this object
        """
        return getattr(self.__ret, key)

    def add_entries(self, entries):
        """
        add multiple entries at once
        """
        for entry in entries:
            apply(self.create, tuple(entry))

    def create(self, path, accelerator=None, callback=None, *args):
        """
        create a single menuitem and add it to one of the menus already
        created (or create a new one)
        """
        last_slash = string.rfind(path, '/')
        if last_slash < 0:
            parentmenu = self.__w
        else:
            parentmenu = self.get_menu(path[:last_slash])
        label = path[last_slash+1:]
        if label == '<separator>':
            item = gtk.GtkMenuItem()
        elif label[:7] == '<image:':
            end = string.find(label, '>')
            img_name = label[7:end]
            hbox = gtk.GtkHBox(spacing=2)
            try:
                hbox.pack_start(self.create_pixmap(img_name), expand=FALSE)
            except:
                print 'Unable to load menu pixmap: ' + img_name
        
            lbl = gtk.GtkLabel(label[end+1:])
            lbl.set_justify(gtk.JUSTIFY_LEFT)
            hbox.pack_start(lbl, expand=FALSE)
            item = gtk.GtkMenuItem()
            item.add(hbox)
            item.show_all()
        elif label[:8] == '<toggle>':
            item = pguToggleMenuItem(label[8:])
                
        elif label[:7] == '<check>':
            item = gtk.GtkCheckMenuItem(label[7:])
        else:
            if parentmenu == self.__w:
                item = gtk.GtkMenuItem(label)
            else:
                hbox = gtk.GtkHBox()
                spc = gtk.GtkLabel('')
                spc.set_usize(22,18)
                hbox.pack_start(spc, expand=FALSE)
                lbl = gtk.GtkLabel(label)
                lbl.set_justify(gtk.JUSTIFY_LEFT)
                hbox.pack_start(lbl, expand=FALSE)
                item = gtk.GtkMenuItem()
                item.add(hbox)
        if label != '<nothing>':
            item.show()
        if accelerator:
            key, mods = self.parse_accelerator(accelerator)
            item.add_accelerator("activate", self.accelerator,
                         key, mods, 'visible')
        if callback:
            apply(item.connect, ("activate", callback) + args)
        # right justify the help menu automatically
        if string.lower(label) == 'help' and parentmenu == self.__w:
            item.right_justify()
        parentmenu.append(item)
        self.__items[path] = item
        return item

    def get_menu(self, path):
        """
        get the menu rooted at the given path
        """
        if path == '':
            return self.__w
        if self.__menus.has_key(path):
            return self.__menus[path]
        wid = self.create(path)
        menu = gtk.GtkMenu()
        menu.set_accel_group(self.accelerator)
        wid.set_submenu(menu)
        self.__menus[path] = menu
        return menu

    def parse_accelerator(self, accelerator):
        """
        parse an accelerator entry
        """
        key = 0
        mods = 0
        done = FALSE
        while not done:
            if accelerator[:7] == '<shift>':
                mods = mods | gtk.GDK.SHIFT_MASK
                accelerator = accelerator[7:]
            elif accelerator[:5] == '<alt>':
                mods = mods | gtk.GDK.MOD1_MASK
                accelerator = accelerator[5:]
            elif accelerator[:6] == '<meta>':
                mods = mods | gtk.GDK.MOD1_MASK
                accelerator = accelerator[6:]
            elif accelerator[:9] == '<control>':
                mods = mods | gtk.GDK.CONTROL_MASK
                accelerator = accelerator[9:]
            else:
                done = TRUE
                key = ord(accelerator[0])
        return key, mods

    def remove_entry(self, path):
        """
        remove a single entry by its path
        """
        if path not in self.__items.keys():
            return
        item = self.__items[path]
        item.destroy()
        length = len(path)
        # clean up internal hashes
        for i in self.__items.keys():
            if i[:length] == path:
                del self.__items[i]
        for i in self.__menus.keys():
            if i[:length] == path:
                del self.__menus[i]
    def remove_entries(self, paths):
        """
        remove menuitems based on the menu path name used to add them
        """
        for path in paths:
            self.remove_entry(path)

    def find(self, path):
        """
        find a menuitem instance by the path for the menu item.  This
        is the text used in the add_entries call.
        """
        return self.__items[path]

    def create_pixmap(self, filename):
        """
        create a pixmap from a filename

        filename - string, the filename to create the pixmap from
        """
        full_filename = os.path.join(gview.home_dir, 'pics', filename)
        if not os.path.isfile(full_filename):
            print '%s filename not found, using default.xpm' % full_filename
            full_filename = os.path.join(gview.home_dir, 'pics', 'default.xpm')
        pix, mask = gtk.create_pixmap_from_xpm(self, None, full_filename)
        return gtk.GtkPixmap(pix, mask)

class pguToggleMenuItem( gtk.GtkMenuItem ):
    
    def __init__(self, label=""):
        import pgutogglebutton
        gtk.GtkMenuItem.__init__( self )
            
        hbox = gtk.GtkHBox( spacing = 2 )
        self.tb = pgutogglebutton.pguToggleButton( )
        self.tb.connect( 'toggled', self.toggled_cb)
        hbox.pack_start( self.tb, expand=FALSE )
        
        evt_box = gtk.GtkEventBox()
        evt_box.connect( 'button-release-event', self.toggle_it )
        
        lbl = gtk.GtkLabel( label )
        evt_box.add( lbl )
        
        hbox.pack_start( evt_box )
        self.add( hbox )
        self.show_all()
        
    def set_active( self, bState ):
        self.tb.set_active( bState )
        
    def get_active( self ):
        return self.tb.get_active()
        
    def toggle_it( self, widget, event, *args ):
        self.set_active( not self.tb.get_active() )
        
    def toggled_cb( self, widget, *args ):
        self.activate()
        self.get_ancestor( gtk.GtkMenuShell.get_type() ).deactivate()
        