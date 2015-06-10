import gtk; _gtk = gtk; del gtk
import _gtkmissing
import _gv
import pgu

###############################################################################
class GtkColorWell(_gtk.GtkButton):
    get_type = _gv.gtk_color_well_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gtk_color_well_new('')
        if self._o is None:
            raise ValueError, "Failed to create GtkColorWell."

    def set_d( self, r, g, b, a ):
        _gv.gtk_color_well_set_d( self._o, r, g, b, a )

    def set_i8( self, r, g, b, a ):
        _gv.gtk_color_well_set_i8( self._o, r, g, b, a )

    def set_i16( self, r, g, b, a ):
        _gv.gtk_color_well_set_i16( self._o, r, g, b, a )

    def set_use_alpha( self, use_alpha ):
        _gv.gtk_color_well_set_use_alpha( self._o, use_alpha )

    def set_continuous( self, update_continuous ):
        _gv.gtk_color_well_set_continuous( self._o, update_continuous )

    def set_title( self, title ):
        _gv.gtk_color_well_set_title( self._o, title )

    def get_d(self):
        return _gv.gtk_color_well_get_d( self._o );

    def get_color( self ):
        return self.get_d()

    def set_color( self, color ):
        self.set_d( color[0], color[1], color[2], color[3] )



pgu.gtk_register( "GtkColorWell", GtkColorWell )


###############################################################################

def toolbar_append_element(self, type, widget, text, tooltip, tp,
                           icon, callback, *extra):
    if widget: widget = widget._o
    if icon: icon = icon._o
    return _gtk._obj2inst(_gtkmissing.gtk_toolbar_append_element(
        self._o, type, widget, text, tooltip, tp, icon, callback, extra))

_gtk.GtkToolbar.append_element = toolbar_append_element

###############################################################################

def gtk_window_get_position( self ):
    return _gtkmissing.gtk_window_get_position( self._o )

def gtk_window_move( self, x, y ):
    return _gtkmissing.gtk_window_move( self._o, x, y )

_gtk.GtkWindow.get_position = gtk_window_get_position
_gtk.GtkWindow.window_move = gtk_window_move

del toolbar_append_element

