###############################################################################
# $Id: gvogrfsgui.py,v 1.6 2001/09/17 15:27:03 pgs Exp $
#
# Project:  OpenEV
# Purpose:  GUI Widgets for displaying and manipulating OGRFS rendering
#           descriptions.
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
# Copyright (c) 2001, Frank Warmerdam <warmerdam@pobox.com>
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
#  $Log: gvogrfsgui.py,v $
#  Revision 1.6  2001/09/17 15:27:03  pgs
#  updated to work with new ColorButton
#
#  Revision 1.5  2001/07/01 03:06:51  pgs
#  hacked to get manual change of offsets working
#
#  Revision 1.4  2001/05/05 18:28:14  pgs
#  added interactive updates plus reverse dy offset
#
#  Revision 1.3  2001/05/04 02:56:56  pgs
#  a couple of bug fixes plus added label offsets
#
#  Revision 1.2  2001/04/24 14:24:02  warmerda
#  added support for applying text indirectly
#
#  Revision 1.1  2001/04/23 21:20:19  warmerda
#  New
#
#

from gtk import *
from string import *
from gvsignaler import *
import gvutils
import gview
import pgu
import sys
import pgucolorsel
import pgufont
import pgucombo
import pgucolor
import pgumenu
import gvogrfs

#map display names to ogr symbol names and an icon (for an image menu)
ogrfs_symbols = {
    'cross'             : ('"ogr-sym-0"', 'sym_cross.xpm'),
    'x'                 : ('"ogr-sym-1"', 'sym_x.xpm'),
    'unfilled circle'   : ('"ogr-sym-2"', 'sym_circle.xpm'),
    'filled circle'     : ('"ogr-sym-3"', 'sym_filled_circle.xpm'),
    'unfilled square'   : ('"ogr-sym-4"', 'sym_square.xpm'),
    'filled square'     : ('"ogr-sym-5"', 'sym_filled_square.xpm'),
    'unfilled triangle' : ('"ogr-sym-6"', 'sym_triangle.xpm'),
    'filled triangle'   : ('"ogr-sym-7"', 'sym_filled_triangle.xpm'),
    'unfilled star'     : ('"ogr-sym-8"', 'sym_star.xpm'),
    'filled star'       : ('"ogr-sym-9"', 'sym_filled_star.xpm'),
    'vertical bar'      : ('"ogr-sym-10"','sym_vertical.xpm')
         }

ogrfs_symbol_names = ['cross', 'x',
             'unfilled circle', 'filled circle',
             'unfilled square', 'filled square',
             'unfilled triangle', 'filled triangle',
             'unfilled star', 'filled star',
             'vertical bar']


###############################################################################
class GvLabelStyle(GtkVBox, Signaler):

    ###########################################################################
    def __init__(self, spacing=10, text_entry=FALSE, layer=None,
                 label_field = TRUE, enable_offsets=FALSE, interactive=FALSE):
        GtkVBox.__init__(self,spacing=spacing)

        self.ogrfs_obj = None
        self.layer = layer
        self.shape_obj = None
        self.text_entry = text_entry
        self.enable_offsets = enable_offsets
        self.interactive = interactive
        self.updating = 0
        self.old_list = []

        self.set_border_width(10)
        self.create_gui()

        self.connect('unrealize', self.close)

        self.publish('ogrfs-changed')
        self.publish('apply-text-to-field')

        self.gui_update()
        self.show_all()

        if not label_field:
            self.field_label.hide()
            self.label_field.hide()

    ###########################################################################
    def close( self, *args ):
        pass

    ###########################################################################
    def set_ogrfs( self, ogrfs_obj, layer = None, fontlist = None,
                   shape_obj = None ):

        if layer is not None:
            self.layer = layer

        if ogrfs_obj is None:
            ogrfs_obj = gvogrfs.OGRFeatureStylePart()
            font = pgufont.XLFDFontSpec()
            default_font = gview.get_preference('default-font')
            if default_font is None:
                font.set_font_part('Family', 'fixed')
            else:
                font.parse_font_spec(default_font)
            if self.enable_offsets:
                dx = self.x_offset.get_value_as_float()
                dy = self.y_offset.get_value_as_float()
            ogrfs_obj.parse('LABEL(t:"",f:"%s",c:#88FF88)' % font)

        self.ogrfs_obj = ogrfs_obj
        self.shape_obj = shape_obj

        self.gui_update()

    ###########################################################################
    def create_gui(self):

        table = GtkTable()
        table.set_row_spacings(3)
        table.set_col_spacings(3)
        self.pack_start(table)

        # collect candidate field names from the schema.
        fnlist = [ 'disabled' ]

        # Field Name
        self.field_label = GtkLabel('Label Field:')
        table.attach(self.field_label, 0, 1, 0, 1,
                xoptions=SHRINK, yoptions=SHRINK)
        self.label_field = pgucombo.pguCombo()
        self.label_field.set_popdown_strings( fnlist )
        self.label_field.entry.connect('changed', self.label_change_cb)
        table.attach(self.label_field, 1, 3, 0, 1,
                xoptions=SHRINK, yoptions=SHRINK)

        # Create Color control.
        table.attach(GtkLabel('Color:'), 0, 1, 1, 2,
                xoptions=SHRINK, yoptions=SHRINK)
        self.label_color = pgucolorsel.ColorControl('Label Color',
                                                    self.label_change_cb)
        table.attach(self.label_color, 1, 3, 1, 2,
                yoptions=SHRINK)

        # Font
        table.attach(GtkLabel('Font:'), 0, 1, 2, 3,
                xoptions=SHRINK, yoptions=SHRINK)
        self.label_font = pgufont.pguFontControl()
        self.label_font.subscribe('font-changed', self.label_change_cb)
        table.attach(self.label_font, 1, 2, 2, 3,
                xoptions=SHRINK)

        #######################################################################
        # Add Text entry/edit
        if self.text_entry:
            table.attach(GtkLabel('Text:'), 0, 1, 3, 4,
                    xoptions=SHRINK, yoptions=SHRINK)

            self.text_entry = GtkEntry()
            self.text_entry.connect('activate',self.text_change_cb)
            if self.interactive:
                self.text_entry.connect('changed', self.text_change_cb)
            else:
                self.text_entry.connect('focus-out-event',self.text_change_cb)
            table.attach(self.text_entry, 1, 3, 3, 4)
        else:
            self.text_entry = None

        if self.enable_offsets:
            #Label offsets
            table.attach(GtkLabel('Label X Offset:'), 0, 1, 4, 5,
                    xoptions=SHRINK, yoptions=SHRINK)
            spin_adjust = GtkAdjustment(value=0.0, lower=-20.0, upper=20.0, step_incr=1.0)
            self.x_offset = GtkSpinButton(spin_adjust)
            self.x_offset.set_editable(TRUE)
            self.x_offset.set_digits(1)
            self.x_offset.set_usize(75, 0)
            self.x_offset.connect('changed', self.label_change_cb)
            table.attach(self.x_offset, 1, 3, 4, 5,
                            xoptions=SHRINK, yoptions=SHRINK)

            #Label offsets
            table.attach(GtkLabel('Label Y Offset:'), 0, 1, 5, 6,
                    xoptions=SHRINK, yoptions=SHRINK)
            spin_adjust = GtkAdjustment(value=0.0, lower=-20.0, upper=20.0, step_incr=1.0)
            self.y_offset = GtkSpinButton(spin_adjust)
            self.y_offset.set_editable(TRUE)
            self.y_offset.set_digits(1)
            self.y_offset.set_usize(75, 0)
            self.y_offset.connect('changed', self.label_change_cb)
            table.attach(self.y_offset, 1, 3, 5, 6,
                            xoptions=SHRINK, yoptions=SHRINK)


    ###########################################################################
    def gui_update(self, *args):

        self.updating = TRUE

        # Update the field list.
        fnlist = [ 'disabled' ]
        if self.layer is not None:
            schema = self.layer.get_parent().get_schema()
            for item in schema:
                fnlist.append( item[0] )

        if fnlist != self.old_list:
            self.label_field.set_popdown_strings( fnlist )
            self.old_list = fnlist

        self.label_field.entry.delete_text(0,-1)

        if self.ogrfs_obj is None:
            self.label_field.entry.insert_text('disabled')
            self.label_color.set_color( (0.5, 1.0, 0.5, 1.0) )
            if self.enable_offsets:
                self.x_offset.set_value(0.0)
                self.y_offset.set_value(0.0)
        else:
            font = pgufont.XLFDFontSpec()
            font_spec = self.ogrfs_obj.parms['f'].value
            if font_spec is not None:
                font.parse_font_spec(font_spec)
            else:
                default_font = gview.get_preference('default-font')
                if default_font is None:
                    font.set_font_part('Family', 'fixed')
                else:
                    font.parse_font_spec(default_font)
            self.label_font.set_font(str(font))

            tparm = self.ogrfs_obj.parms['t']
            if tparm.role == 'field_name':
                self.label_field.entry.insert_text(tparm.value)
                if self.shape_obj is not None:
                    text_value = self.shape_obj.get_property(tparm.value,'')
                else:
                    text_value = ''
            else:
                self.label_field.entry.insert_text('disabled')
                text_value = tparm.value

            color = self.ogrfs_obj.get_color((0.5, 1.0, 0.5, 1.0))
            self.label_color.set_color( color )

            if self.text_entry is not None:
                self.text_entry.set_text(text_value)
                #self.text_entry.set_sensitive(tparm.role != 'field_name')

            if self.enable_offsets:
                try:
                    dx = float(self.ogrfs_obj.get_parm('dx'))
                    self.x_offset.set_value(dx)
                except:
                    dx = None

                if dx is None:
                    dx = 0.0

                try:
                    dy = float(self.ogrfs_obj.get_parm('dy'))
                    self.y_offset.set_value(-dy)
                except:
                    dy = None

                if dy is None:
                    dy = 0.0

                #update the widgets


        self.updating = FALSE

    ###########################################################################
    # Handle updates to the raw text.  Normally we just turn this over to
    # the generic label_change_cb(), but if we have field indirection in
    # operation, then we instead emit a signal offering the text to the
    # application to apply to the shape.

    def text_change_cb(self, *args):
        field_name = self.label_field.entry.get_chars(0,-1)
        if field_name == 'disabled' or len(field_name) == 0:
            self.label_change_cb()
            return

        #this shouldn't happen :)
        val = ''
        if self.text_entry is not None:
            val = self.text_entry.get_text()

        self.notify( 'apply-text-to-field',
                     field_name, val )
        self.gui_update()

    ###########################################################################
    # Handle updates to the label font.

    def label_change_cb(self, *args):
        if self.layer is None or self.updating:
            return

        font = self.label_font.get_font()
        field_name = self.label_field.entry.get_chars(0,-1)
        text_value = ''
        if self.text_entry is not None:
            text_value = self.text_entry.get_text()

        color = self.label_color.current_color
        color = gvogrfs.gv_to_ogr_color( color )

        import string
        x_off = ''
        y_off = ''



        if self.enable_offsets:
            #handle user editing of the values in the x and y offsets.
            #something odd happens when listening to the 'changed' signal
            #of the spin box, the text value is difference from the float
            #value, even if the values should match.  This hack forces the
            #spin buttons to update the value and exits because this
            #will be called again right away
            x = self.x_offset.get_value_as_float()
            y = self.y_offset.get_value_as_float()
            sx = self.x_offset.get_text()
            sy = self.y_offset.get_text()
            try:
                if float(sx) != x:
                    self.x_offset.set_value(float(sx))
                    return
                if float(sy) != y:
                    self.y_offset.set_value(float(sy))
                    return
            except:
                return
            if 0.0 != x:
                x_off = 'dx:%s,' % x

            if 0.0 != y:
                y_off = 'dy:%s,' % -y

        if field_name == 'disabled' or len(field_name) == 0:
            if text_value is not None:
                ogrfs = 'LABEL(%s%st:\"%s\",f:"%s",c:%s)' % \
                        (x_off, y_off, text_value,font,color)
            else:
                ogrfs = None
        else:
            ogrfs = 'LABEL(%s%st:{%s},f:"%s",c:%s)' % \
                        (x_off, y_off, field_name, font, color)

        if ogrfs is None:
            self.ogrfs_obj = None
        else:
            self.ogrfs_obj = gvogrfs.OGRFeatureStylePart()
            self.ogrfs_obj.parse( ogrfs )

        self.gui_update()

        self.notify('ogrfs-changed')

    #
    def set_sensitive(self, sensitive):
        self.text_entry.set_sensitive(sensitive)

    ###########################################################################
    # Handle updates to the label font.
    def text_input(self, keyval):
        if keyval > 31 and keyval < 256 and self.text_entry is not None:
            new_string = self.text_entry.get_text()
            new_string = new_string + chr(keyval)
            self.text_entry.set_text( new_string )

        elif keyval == GDK.Return:
            self.label_change_cb()

        # add support for delete, etc, later.



class GvSymbolStyle(GtkVBox, Signaler):
    """
    A generic embeddable widget for controlling the SYMBOL ogr feature style
    on an arbitrary object (layer or shape).
    """

    def __init__(self, spacing=10, ogrfs_obj=None, layer=None):
        """
        Initialize the widget optionally setting the ogr object for which this
        represents the SYMBOL feature style.
        """
        GtkVBox.__init__(self, spacing=spacing)
        self.create_gui()

        self.updating = FALSE
        self.publish('ogrfs-changed')
        self.set_ogrfs(ogrfs_obj, layer)

    def create_gui(self):
        """
        create the widgets for this symbol
        """

        table = GtkTable()
        table.set_row_spacings(3)
        table.set_col_spacings(3)
        self.pack_start(table)
        #symbol color
        table.attach(GtkLabel('Color: '), 0, 1, 0, 1,
                xoptions=SHRINK, yoptions=SHRINK)
        self.symbol_color = pgucolor.ColorButton((0.5, 1.0, 0.5, 1.0))
        self.symbol_color.connect('color-set', self.color_change)
        table.attach(self.symbol_color, 1, 2, 0, 1,
                xoptions=SHRINK, yoptions=SHRINK)

        # Point symbol
        table.attach(GtkLabel('Symbol:'), 0, 1, 1, 2,
                xoptions=SHRINK, yoptions=SHRINK)
        self.symbol_type = pgumenu.pguMenuFactory(MENU_FACTORY_OPTION_MENU)
        entries = []
        for i in range(len(ogrfs_symbol_names)):
            sym_name = ogrfs_symbol_names[i]
            sym_img = ogrfs_symbols[sym_name][1]
            a = '<image:' + sym_img + '>' + sym_name
            entries.append((a, None, self.symbol_change, ogrfs_symbols[sym_name][0]))

        self.symbol_type.add_entries(entries)

        self.symbol_type.set_usize(150, 30)
        table.attach(self.symbol_type, 1, 4, 1, 2,
                xoptions=SHRINK, yoptions=SHRINK)

        # Point size
        table.attach(GtkLabel('Scale: '), 0, 1, 2, 3,
                xoptions=SHRINK, yoptions=SHRINK)
        spin_adjust = GtkAdjustment(value=1.0, lower=0.2,
                        upper=4.0, step_incr=0.1)
        self.symbol_size = GtkSpinButton(spin_adjust)
        self.symbol_size.set_editable(TRUE)
        self.symbol_size.set_digits(1)
        self.symbol_size.set_usize(75, 0)
        self.symbol_size.connect('changed', self.scale_change)
        table.attach(self.symbol_size, 1, 3, 2, 3,
                xoptions=SHRINK, yoptions=SHRINK)



    def gui_update(self, *args):
        """
        refresh the screen
        """
        #get the current values
        if self.updating:
            return

        self.updating = TRUE

        sym = int(self.ogrfs_obj.parms['id'].value[8:9])
        color = gvogrfs.ogr_to_gv_color(self.ogrfs_obj.parms['c'].value)
        try:
            scale = float(self.ogrfs_obj.get_parm('s'))
        except:
            scale = None

        if scale is None:
            scale = 1.0

        #update the widgets
        self.symbol_type.set_history(sym)
        self.symbol_color.set_color(color)
        self.symbol_size.set_value(scale)

        self.updating = FALSE

    def set_ogrfs(self, ogrfs_obj, layer = None):
        """
        set the ogr feature specification from the shape object passed,
        or from the layer if the shape has none, or provide a default
        """

        if ogrfs_obj is None:
            ogrfs_obj = gvogrfs.OGRFeatureStylePart()
            ogrfs_obj.parse('SYMBOL(id:"ogr-sym-0",c:#88FF88)')

        self.ogrfs_obj = ogrfs_obj
        self.layer = layer
        self.gui_update()

    def color_change(self, widget, *args):
        """
        """
        print 'color_change(', widget, args, ')'
        val = 'c:%s' % gvogrfs.gv_to_ogr_color(widget.get_color())
        parm = gvogrfs.OGRFeatureStyleParam()
        parm.parse(val)
        self.ogrfs_obj.set_parm(parm)
        self.notify('ogrfs-changed')

    def scale_change(self, widget):
        """
        change the scale ... be careful as it may not exist beforehand
        """
        val = 's:%s' % widget.get_value_as_float()
        parm = gvogrfs.OGRFeatureStyleParam()
        parm.parse(val)
        self.ogrfs_obj.set_parm(parm)
        self.notify('ogrfs-changed')

    def symbol_change(self, widget, symbol):
        """
        change the symbol
        """
        val = 'id:%s' % symbol
        parm = gvogrfs.OGRFeatureStyleParam()
        parm.parse(val)
        self.ogrfs_obj.set_parm(parm)
        self.notify('ogrfs-changed')



pgu.gtk_register('GvLabelStyle',GvLabelStyle)
pgu.gtk_register('GvSymbolStyle', GvSymbolStyle)
