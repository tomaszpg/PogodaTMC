###############################################################################
# $Id: gvvectorpropdlg.py,v 1.23 2003/02/14 23:03:35 pgs Exp $
#
# Project:  OpenEV
# Purpose:  GvShapesLayer Properties Dialog
# Author:   Frank Warmerdam, warmerdam@pobox.com
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
#  $Log: gvvectorpropdlg.py,v $
#  Revision 1.23  2003/02/14 23:03:35  pgs
#  fixed typo in area_edge_width signal callback
#
#  Revision 1.21  2002/03/21 15:48:51  warmerda
#  added support for geometry specific _ogr_ogrfs_... layer properties
#
#  Revision 1.20  2001/04/16 17:06:49  warmerda
#  paul added symbol support to vector prop dialog
#
#  Revision 1.19  2001/04/03 02:29:30  warmerda
#  improved some pane geometry
#
#  Revision 1.18  2001/03/26 19:25:42  warmerda
#  fixed typo with font list
#
#  Revision 1.17  2001/03/21 22:41:27  warmerda
#  added labels support under drawing style
#
#  Revision 1.16  2000/08/10 15:59:29  warmerda
#  added help topic
#
#  Revision 1.15  2000/08/08 20:12:21  warmerda
#  close on layer teardown
#
#  Revision 1.14  2000/07/21 01:31:12  warmerda
#  added read_only flag for GvData, and utilize for vector layers
#
#  Revision 1.13  2000/07/20 02:45:04  warmerda
#  avoid doing gui updates in response to signals if dialog destroyed
#
#  Revision 1.12  2000/06/14 15:13:21  warmerda
#  updated pgu stuff
#
#  Revision 1.11  2000/06/09 01:04:14  warmerda
#  added standard headers
#

from gtk import *
from string import *
import gvutils
import pgucolorsel

from gvconst import *
import gview
import gvhtml
import gvogrfs
import pgutogglebutton

prop_dialog_list = []

def LaunchVectorPropDialog(layer):
    # Check list to see if dialog exists - make it visible
    for test_dialog in prop_dialog_list:
        if test_dialog.layer._o == layer._o:
            test_dialog.update_gui()
            test_dialog.show()
            test_dialog.get_window()._raise()
            return test_dialog

    # Create new dialog if one doesn't exist already
    new_dialog = GvVectorPropDialog(layer)
    prop_dialog_list.append( new_dialog )
    return new_dialog

symbols = [ 'cross', 'x',
             'unfilled circle', 'filled circle',
             'unfilled square', 'filled square',
             'unfilled triangle', 'filled triangle',
             'unfilled star', 'filled star',
             'vertical bar' ]

class GvVectorPropDialog(GtkWindow):

    def __init__(self, layer):
        GtkWindow.__init__(self)
        self.set_title(layer.get_name()+' Properties')
        self.layer = layer
        self.updating = FALSE

        if self.layer is not None:
            self.display_change_id = layer.connect('display-change',
                                                   self.refresh_cb)
            self.teardown_id = layer.connect('teardown',self.close)

        # create the general layer properties dialog
        self.create_notebook()
        self.create_pane1()

        # Setup Object Drawing Properties Tab
        self.pane2 = GtkVBox(spacing=10)
        self.pane2.set_border_width(10)
        self.notebook.append_page( self.pane2, GtkLabel('Draw Styles'))

        gvhtml.set_help_topic( self, "gvvectorpropdlg.html" )


        # ANTIALIASING
        box = GtkHBox(spacing=3)
        self.pane2.pack_start(box)
        box.pack_start( GtkLabel("Anti-alias:"), expand=FALSE )
        self.antialias = pgutogglebutton.pguToggleButton()
        self.antialias.connect('toggled', self.antialias_cb )
        box.pack_start( self.antialias, expand=FALSE )

        # POINT CONTROLS -----------------------------------------------------
        frame = GtkFrame('Points')
        self.pane2.pack_start(frame)

        vbox = GtkVBox(spacing=10)
        vbox.set_border_width(10)
        frame.add(vbox)

        #create a symbol control
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Symbol:'), expand=FALSE)
        self.point_symbol = GtkCombo()
        #add a default to symbol names
        self.point_symbol.set_popdown_strings( tuple(symbols) )
        self.point_symbol.entry.set_editable(FALSE)
        #self.point_symbol.set_value_in_list(TRUE, FALSE)
        self.point_symbol.entry.connect('changed', self.symbol_cb)
        box.pack_start(self.point_symbol)

        # Create Color control.
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Color:'),expand=FALSE)
        self.point_color = pgucolorsel.ColorControl('Point Color',
                                                  self.symbol_cb)
        box.pack_start(self.point_color)

        # Point size
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Point Size:'),expand=FALSE)
        self.point_size = GtkCombo()
        self.point_size.set_popdown_strings(
            ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '15', '20') )
        self.point_size.entry.connect('changed', self.point_size_cb)
        box.pack_start(self.point_size,expand=FALSE)

        # LINE CONTROLS ------------------------------------------------------
        frame = GtkFrame('Lines')
        self.pane2.pack_start(frame)

        vbox = GtkVBox()
        vbox.set_border_width(10)
        frame.add(vbox)

        # Create Color control.
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Color:'),expand=FALSE)
        self.line_color = pgucolorsel.ColorControl('Line Color',
                                         self.color_cb,'_line_color')
        box.pack_start(self.line_color)
        
        #Line Width
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Width:'), expand=FALSE)
        self.line_width = GtkEntry()
        self.line_width.connect('changed', self.line_width_cb)
        box.pack_start( self.line_width, expand=FALSE)
        

        # AREA CONTROLS ------------------------------------------------------
        frame = GtkFrame('Areas')
        self.pane2.pack_start(frame)

        vbox = GtkVBox(spacing=10)
        vbox.set_border_width(10)
        frame.add(vbox)

        # Create Color controls
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Edge Color:'),expand=FALSE)
        self.area_edge_color = pgucolorsel.ColorControl('Area Edge Color',
                                              self.color_cb,'_area_edge_color')
        box.pack_start(self.area_edge_color)

        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Fill Color:'),expand=FALSE)
        self.area_fill_color = pgucolorsel.ColorControl('Area Fill Color',
                                              self.color_cb,'_area_fill_color')
        box.pack_start(self.area_fill_color)

        #Area Edge Width
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Edge Width:'), expand=FALSE)
        self.area_edge_width = GtkEntry()
        self.area_edge_width.connect('changed', self.area_edge_width_cb)
        box.pack_start( self.area_edge_width, expand=FALSE)
        

        # LABEL CONTROLS -----------------------------------------------------
        frame = GtkFrame('Labels')
        self.pane2.pack_start(frame)

        vbox = GtkVBox(spacing=10)
        vbox.set_border_width(10)
        frame.add(vbox)

        # collect candidate field names from the schema.
        fnlist = [ 'disabled' ]
        schema = self.layer.get_parent().get_schema()
        for item in schema:
            fnlist.append( item[0] )

        # Field Name
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Label Field:'),expand=FALSE)
        self.label_field = GtkCombo()
        self.label_field.set_popdown_strings( fnlist )
        self.label_field.entry.connect('changed', self.label_change_cb)
        box.pack_start(self.label_field,expand=FALSE)

        # Create Color control.
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Color:'),expand=FALSE)
        self.label_color = pgucolorsel.ColorControl('Label Color',
                                                    self.label_change_cb)
        box.pack_start(self.label_color)

        # Font
        font_list = self.layer.get_view().get_fontnames()
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Font:'),expand=FALSE)
        self.label_font = GtkCombo()
        self.label_font.set_popdown_strings(font_list)
        self.label_font.entry.connect('changed', self.label_change_cb)
        box.pack_start(self.label_font,expand=FALSE)

        self.update_gui()

        self.show_all()

    def create_notebook(self):
        self.set_border_width(3)
        self.notebook = GtkNotebook()
        self.add( self.notebook )
        self.connect('delete-event', self.close)

    def create_pane1(self):
        # Setup General Properties Tab
        self.pane1 = GtkVBox(spacing=10)
        self.pane1.set_border_width(10)
        self.notebook.append_page( self.pane1, GtkLabel('General'))

        # Setup layer name entry box.
        box = GtkHBox(spacing=5)
        self.pane1.pack_start(box, expand=FALSE)
        label = GtkLabel('Layer:' )
        box.pack_start(label,expand=FALSE)
        self.layer_name = GtkEntry()
        self.layer_name.connect('changed', self.name_cb)
        box.pack_start(self.layer_name)

        # Setup Visibility radio buttons.
        vis_box = GtkHBox(spacing=5)
        self.pane1.pack_start(vis_box, expand=FALSE)
        vis_box.pack_start(GtkLabel('Visibility:'),expand=FALSE)
        self.vis_yes = GtkRadioButton(label='yes')
        self.vis_yes.connect('toggled', self.visibility_cb)
        vis_box.pack_start(self.vis_yes,expand=FALSE)
        self.vis_no = GtkRadioButton(label='no',group=self.vis_yes)
        self.vis_no.connect('toggled', self.visibility_cb)
        vis_box.pack_start(self.vis_no,expand=FALSE)

        # Setup Editability radio buttons.
        edit_box = GtkHBox(spacing=5)
        self.pane1.pack_start(edit_box, expand=FALSE)
        edit_box.pack_start(GtkLabel('Editable:'),expand=FALSE)
        self.edit_yes = GtkRadioButton(label='yes')
        self.edit_yes.connect('toggled', self.edit_cb)
        edit_box.pack_start(self.edit_yes,expand=FALSE)
        self.edit_no = GtkRadioButton(label='no',group=self.edit_yes)
        self.edit_no.connect('toggled', self.edit_cb)
        edit_box.pack_start(self.edit_no,expand=FALSE)

    # Initialize GUI state from underlying object state.
    def update_gui(self):

        if self.flags( DESTROYED ) > 0:
            return

        if self.layer is None or self.updating == TRUE:
            return

        self.updating = TRUE

        # Layer name.
        self.layer_name.set_text( self.layer.get_name() )

        # Visibility radio buttons
        self.vis_yes.set_active( self.layer.is_visible() )
        self.vis_no.set_active( not self.layer.is_visible() )

        # Editability radio buttons
        self.edit_yes.set_active( not self.layer.is_read_only() )
        self.edit_no.set_active( self.layer.is_read_only() )

        # colors
        self.set_color_or_default('_point_color', self.point_color)
        self.set_color_or_default('_line_color', self.line_color)
        self.set_color_or_default('_area_edge_color', self.area_edge_color)
        self.set_color_or_default('_area_fill_color', self.area_fill_color)

        # point size
        self.point_size.entry.delete_text(0,-1)
        if self.layer.get_property('_point_size') is None:
            self.point_size.entry.insert_text('6')
        else:
            self.point_size.entry.insert_text(
                self.layer.get_property('_point_size'))
                
        #line and area edge width
        self.line_width.delete_text( 0, -1 )
        if self.layer.get_property('_line_width') is None:
            self.line_width.insert_text('1.0')
        else:
            self.line_width.insert_text(
                 self.layer.get_property( '_line_width' ))

        self.area_edge_width.delete_text( 0, -1 )
        if self.layer.get_property('_area_edge_width') is None:
            self.area_edge_width.insert_text('1.0')
        else:
            self.area_edge_width.insert_text(
                 self.layer.get_property( '_area_edge_width' ))
                 
        # antialiasing
        if self.layer.get_property('_gl_antialias') is None:
            self.antialias.set_active( FALSE )
        elif self.layer.get_property('_gl_antialias') == "0":
            self.antialias.set_active( FALSE )
        else:
            self.antialias.set_active( TRUE )

        # font and symbol information

        self.label_font.entry.delete_text(0,-1)
        self.label_field.entry.delete_text(0,-1)

        ogrfs = self.layer.get_property('_gv_ogrfs_point')
        ogrfs_obj = gvogrfs.OGRFeatureStyle()
        ogrfs_label = None
        try:
            ogrfs_obj.parse( ogrfs )
        except:
            print 'update_gui: error parsing ogrfs:'
            print ogrfs

        ogrfs_label = ogrfs_obj.get_part('LABEL')
        if ogrfs_label is None:
            self.label_font.entry.insert_text('Fixed')
            self.label_field.entry.insert_text('disabled')
            self.label_color.set_color( (0.5, 1.0, 0.5, 1.0) )
        else:
            self.label_font.entry.insert_text(ogrfs_label.parms['f'].value)
            self.label_field.entry.insert_text(ogrfs_label.parms['t'].value)
            ogr_color = ogrfs_label.parms['c'].value
            gv_color = gvogrfs.ogr_to_gv_color(ogr_color)
            self.label_color.set_color(gv_color)

        ogrfs_symbol = ogrfs_obj.get_part('SYMBOL')
        if ogrfs_symbol is None:
            self.point_symbol.entry.set_text('cross')
        else:
            ogr_sym = ogrfs_symbol.parms['id'].value
            try:
                sym_num = int(ogr_sym[8:9])
                sym_name = symbols[sym_num]
            except:
                sym_name = 'cross'
            self.point_symbol.entry.set_text( sym_name )

        self.updating = FALSE

    def name_cb(self, *args):
        if self.layer_name.get_text() != self.layer.get_name():
            self.layer.set_name( self.layer_name.get_text() )

    # Set color from property, or use default color.
    def set_color_or_default(self, property_name, widget):
        if self.layer.get_property( property_name ) is None:
            widget.set_color( (0.5, 1.0, 0.5, 1.0) )
        else:
            widget.set_color_from_string(
                self.layer.get_property( property_name ))

    # Color of a feature type changed
    def color_cb( self, color, type ):
        if self.layer is None:
            print 'set ' + type + ' to ', color
            return

        prop = str(color[0]) + ' ' + str(color[1]) + ' ' \
               + str(color[2]) + ' ' + str(color[3])

        old_prop = self.layer.get_property( type )
        if old_prop is None or old_prop != prop:
            self.layer.set_property( type, prop )
            self.layer.display_change()

    # Handle updates to the point size.
    def point_size_cb(self, args):
        if self.layer is None:
            return

        new_text = self.point_size.entry.get_chars(0,-1)
        if len(new_text) == 0:
            return

        if self.layer.get_property('_point_size') is not None \
           and self.layer.get_property('_point_size') == new_text:
            return

        self.layer.set_property( '_point_size', new_text)
        self.layer.display_change()
        
    #Handle changes to the line width
    def line_width_cb( self, *args ):
        if self.layer is None:
            return
            
        new_text = self.line_width.get_chars(0, -1)
        if (len(new_text)) == 0:
            return
            
        if self.layer.get_property('_line_width') is not None \
           and self.layer.get_property('_line_width') == new_text:
            return
        
        self.layer.set_property('_line_width', new_text)
        self.layer.display_change()
        
    #Handle changes to the area edge width
    def area_edge_width_cb( self, *args ):
        if self.layer is None:
            return
            
        new_text = self.area_edge_width.get_chars(0, -1)
        if (len(new_text)) == 0:
            return
            
        if self.layer.get_property('_area_edge_width') is not None \
           and self.layer.get_property('_area_edge_width') == new_text:
            return
        
        self.layer.set_property('_area_edge_width', new_text)
        self.layer.display_change()
        
    # Handle changes to antialiasing
    def antialias_cb( self, *args ):
        if self.layer is None:
            return
            
        antialias = self.layer.get_property( "_gl_antialias" )
        if antialias is None:
            antialias = "0"
        elif antialias != "0":
            antialias = "1"
            
        if self.antialias.get_active() and antialias != "1":
            self.layer.set_property( "_gl_antialias", "1" )
            self.layer.display_change()
        elif antialias != "0":
            self.layer.set_property( "_gl_antialias", "0" )
            self.layer.display_change()
            

    # Handle updates to the label font.
    def label_change_cb(self, *args):
        if self.layer is None or self.updating:
            return

        font = self.label_font.entry.get_chars(0,-1)
        field_name = self.label_field.entry.get_chars(0,-1)

        color = self.label_color.current_color
        color = gvogrfs.gv_to_ogr_color( color )

        ogrfs = self.layer.get_property('_gv_ogrfs_point')
        ogrfs_obj = gvogrfs.OGRFeatureStyle()
        try:
            ogrfs_obj.parse( ogrfs )
        except:
            print 'an error occurred parsing the ogrfs property:\n', ogrfs

        #remove the old label
        ogrfs_obj.remove_part('LABEL')

        if field_name != 'disabled' and len(field_name) != 0:
            ogrfs_label = gvogrfs.OGRFeatureStylePart()
            ogrfs_label.parse(
                 'LABEL(t:{%s},f:"%s",c:%s)' % (field_name, font, color) )
            ogrfs_obj.add_part( ogrfs_label )

        self.layer.set_property( '_gv_ogrfs_point', ogrfs_obj.unparse() )
        self.layer.display_change()

    # Visibility changing
    def visibility_cb( self, widget ):
        self.layer.set_visible( self.vis_yes.active )

    # Visibility changing
    def edit_cb( self, widget ):
        self.layer.set_read_only( self.edit_no.active )

    #symbol changing
    def symbol_cb( self, widget, *args ):
        """
        update the symbol.  This might have been called because the color
        changed also, so update the _point_color property too.
        """

        if self.layer is None or self.updating:
            return

        symbol = self.point_symbol.entry.get_text()

        ogrfs = self.layer.get_property('_gv_ogrfs_point')
        ogrfs_obj = gvogrfs.OGRFeatureStyle()
        try:
            ogrfs_obj.parse( ogrfs )
        except:
            print 'an error occurred parsing the ogrfs property:\n', ogrfs

        #remove the old symbol
        ogrfs_obj.remove_part('SYMBOL')

        point_sym_text = '"ogr-sym-%s"' % symbols.index(symbol)
        color = self.point_color.current_color
        #should this only be done on point layers?
        point_ogr_color = gvogrfs.gv_to_ogr_color(color)
        point_size = self.point_size.entry.get_text()
        ogr_part = 'SYMBOL(c:' + point_ogr_color + ',id:' + \
            point_sym_text + ')'
        ogrfs_sym = gvogrfs.OGRFeatureStylePart()
        ogrfs_sym.parse( ogr_part )
        ogrfs_obj.add_part( ogrfs_sym )

        self.layer.set_property('_gv_ogrfs_point', ogrfs_obj.unparse())

        prop = str(color[0]) + ' ' + str(color[1]) + \
              ' ' + str(color[2]) + ' ' + str(color[3])
        self.layer.set_property( '_point_color', prop )
        self.layer.display_change()

    # Dialog closed, remove references to python object
    def close( self, widget, args ):
        self.layer.disconnect(self.teardown_id)
        self.layer.disconnect(self.display_change_id)
        prop_dialog_list.remove(self)
        self.layer = None
        self.destroy()

    # Force GUI Refresh
    def refresh_cb( self, widget, args ):
        self.update_gui()

if __name__ == '__main__':
    dialog = GvVectorPropDialog(None)
    dialog.connect('delete-event', mainquit)

    mainloop()

