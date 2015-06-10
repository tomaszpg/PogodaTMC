###############################################################################
# $Id: gvrasterpropdlg.py,v 1.59 2007/11/20 06:11:43 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  GvRasterLayer Properties Dialog
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
#  $Log: gvrasterpropdlg.py,v $
#  Revision 1.59  2007/11/20 06:11:43  warmerda
#  improve resiliency for large floating point values
#
#  Revision 1.58  2006/03/25 15:09:44  andrey_kiselev
#  Unused vbox removed.
#
#  Revision 1.57  2005/06/27 19:37:24  gmwalter
#  Bring in Vincent's slider fix.
#
#  Revision 1.56  2004/12/03 00:24:10  gmwalter
#  Fix scaling slider page increments so that
#  they work for small floating-point valued
#  images.
#
#  Revision 1.55  2004/10/30 18:25:44  warmerda
#  Don't barf out of projection is None.
#
#  Revision 1.54  2004/08/31 21:26:46  warmerda
#  trap failed efforts to fetch datum
#
#  Revision 1.53  2004/06/23 14:35:17  gmwalter
#  Added support for multi-band complex imagery.
#
#  Revision 1.52  2004/06/03 20:13:07  andrey_kiselev
#  Use reasonable values when projections and datums are not set.
#
#  Revision 1.51  2004/05/12 19:26:06  andrey_kiselev
#  Preliminary support for changing projection on the fly.
#
#  Revision 1.50  2004/04/02 17:28:45  gmwalter
#  Fix initialization bug from last changes.
#
#  Revision 1.49  2004/04/02 17:01:02  gmwalter
#  Updated nodata support for complex and
#  rgb data.
#
#  Revision 1.48  2004/02/20 12:34:19  andrey_kiselev
#  Generate different band names to avoid problems with equally named keys.
#
#  Revision 1.47  2004/01/22 21:28:42  andrey_kiselev
#  New control to display and change NODATA value for viewed RasterSource.
#
#  Revision 1.46  2003/11/05 20:27:23  gmwalter
#  Fix to allow dialog to recognize GCPProjection string if Projection
#  string isn't present.
#
#  Revision 1.45  2003/06/17 14:58:39  gmwalter
#  gvplot: changed so that graphs don't immediately disappear
#  in the gnuplot terminal case.
#  gvrasterpropdlg: fix so that user can go back to opaque white modulation
#  colour.
#
#  Revision 1.44  2003/04/30 15:05:24  gmwalter
#  Fixed a typo that was preventing a tuple from being formed and causing
#  bands to wrap around.
#
#  Revision 1.43  2003/02/20 19:27:22  gmwalter
#  Updated link tool to include Diana's ghost cursor code, and added functions
#  to allow the cursor and link mechanism to use different gcps
#  than the display for georeferencing.  Updated raster properties
#  dialog for multi-band case.  Added some signals to layerdlg.py and
#  oeattedit.py to make it easier for tools to interact with them.
#  A few random bug fixes.
#
#  Revision 1.42  2002/12/17 16:11:47  gmwalter
#  Clamp lower bound of Scale_Max to 0.0 in RLM_COMPLEX case in gui_refresh
#  to avoid confusing phase flips at the 0 crossing when phase display is used.
#
#  Revision 1.41  2002/03/04 21:52:26  warmerda
#  add support for band names
#
#  Revision 1.40  2002/03/04 16:26:42  warmerda
#  added greyscale lock option for RGB layers
#
#  Revision 1.39  2001/10/17 16:24:55  warmerda
#  move complex luts to gview.py
#
#  Revision 1.38  2001/10/12 19:25:15  warmerda
#  improved logic for setting the initial scaling min/max of the scaling controls
#
#  Revision 1.37  2001/08/22 02:16:28  warmerda
#  ensure that gvraster reference not kept from GvRasterSource
#
#  Revision 1.36  2001/07/24 21:21:45  warmerda
#  added EV style phase colormap
#
#  Revision 1.35  2001/07/16 15:20:40  warmerda
#  switched around so magnitude is default for complex layers
#
#  Revision 1.34  2001/04/03 02:29:30  warmerda
#  improved some pane geometry
#
#  Revision 1.33  2001/03/19 21:57:14  warmerda
#  expand tabs
#
#  Revision 1.32  2000/08/25 20:20:03  warmerda
#  added limited nodata support, upped max band count to 30
#
#  Revision 1.31  2000/08/11 20:17:15  warmerda
#  added metadata to image info, made scrollable
#
#  Revision 1.30  2000/08/11 19:19:31  warmerda
#  don't show scaling min for complex layers
#

from gtk import *
from string import *
import gvutils
import pgucolorsel
import sys
import gdal
import osr
import gvhtml
import Numeric

from gvconst import *
import gview

prop_dialog_list = []

def LaunchRasterPropDialog(layer):
    # Check list to see if dialog exists - make it visible
    for test_dialog in prop_dialog_list:
        if test_dialog.layer._o == layer._o:
            test_dialog.update_gui()
            test_dialog.show()
            test_dialog.get_window()._raise()
            return test_dialog

    # Create new dialog if one doesn't exist already
    new_dialog = GvRasterPropDialog(layer)
    prop_dialog_list.append( new_dialog )
    return new_dialog

class GvRasterSource(GtkFrame):
    def __init__(self,name,layer,src_index,master_dialog):
        GtkFrame.__init__(self,name)
        self.master_dialog = master_dialog
        self.updating = FALSE
        self.src_index = src_index

        # Eventually the following will have to be more sophisticated.
        if layer is not None:
            self.layer = layer
            self.gvraster = layer.get_parent()
            self.display_change_id = layer.connect('display-change',
                                                   self.gui_refresh)

        vbox = GtkVBox(spacing=5)
        vbox.set_border_width(5)
        self.add(vbox)
        self.updating = TRUE
        
        # ------ Band Selection -------
        hbox = GtkHBox(spacing=5)
        vbox.pack_start(hbox,expand=FALSE)
        hbox.pack_start(GtkLabel('Band:'))
        self.band_combo = GtkCombo()
        hbox.pack_start(self.band_combo)
        self.band_combo.entry.connect('changed', self.set_band_cb)
        self.band_combo.entry.connect('key_press_event', \
	    self.combo_entry_key_press_cb)
        prototype_data = self.layer.get_parent()
        band_list = ['constant']
        ds = prototype_data.get_dataset()
        band_count = ds.RasterCount

        # Fill in the dictionary
        #
        self.__bandDic = {}
        self.__allBands = []
        self.__bandNums = []
        for band in range(band_count) :
            bandKey = self.band_desc(band+1)
            self.__allBands.append( bandKey )
            self.__bandNums.append( str(band+1) )
            self.__bandDic[bandKey] = str(band+1)

        for band in range(min(30,band_count)):
            band_list.append( self.band_desc(band+1) )

        if band_count > 30:
            band_list.append( '...'+self.__allBands[-1] )

        self.band_combo.set_popdown_strings( band_list )

        # ------ Establish scaling range ------

        smin = layer.min_get(src_index)
        smax = layer.max_get(src_index)
        if str(smin) == '-inf':
            smin = -10000000.0
        if str(smax) == 'inf':
            smax = 10000000.0
            
        delta = smax - smin
        smax = smax + delta * 0.25
        smin = smin - delta * 0.25
        
        if self.layer.get_mode() == gview.RLM_COMPLEX:
            smin = 0.0
        elif self.layer.get_parent().get_band().DataType == gdal.GDT_Byte:
            smin = 0
            smax = 255
        elif self.layer.get_parent().get_band().DataType == gdal.GDT_UInt16:
            smin = 0
        elif self.layer.get_parent().get_band().DataType == gdal.GDT_UInt32:
            smin = 0

        # Make sure slider still has reasonable step sizes
        # for cases where image has small, floating point
        # values.
        if delta > 10:
            new_inc = 1
        else:
            new_inc = delta/100.0
            
        # calculate #digits for slider. If datatype is integer, #digits will
        # be 0.  if datatype is floating point, #digits will be set depending
        # on order of magnitude of delta:
	if self.layer.get_parent().get_band().DataType == gdal.GDT_Byte \
	or self.layer.get_parent().get_band().DataType == gdal.GDT_UInt16 \
	or self.layer.get_parent().get_band().DataType == gdal.GDT_Int16 \
	or self.layer.get_parent().get_band().DataType == gdal.GDT_UInt32 \
	or self.layer.get_parent().get_band().DataType == gdal.GDT_Int32:
		sliderDigits = 0
	else:
            try:
                sliderDigits = max(0, 2 - int(Numeric.log10(delta)))
            except:
                sliderDigits = 0

                    
        # ------ Scale Min -------
        hbox = GtkHBox(spacing=5)
        self.min_hbox = hbox
        vbox.pack_start(hbox)
        hbox.pack_start(GtkLabel('Scale Min:'),expand=FALSE)
        self.min_adjustment = GtkAdjustment(layer.min_get(src_index),
                                smin, smax, new_inc, new_inc, new_inc)
        self.min_adjustment.connect('value-changed',self.adjustment_cb)
        self.min_slider = GtkHScale(self.min_adjustment)
        self.min_slider.set_digits(sliderDigits)
        hbox.pack_start(self.min_slider)
        self.min_entry = GtkEntry(maxlen=8)
        self.min_entry.connect('activate',self.entry_cb)
        self.min_entry.connect('leave-notify-event',self.entry_cb)
        hbox.pack_start(self.min_entry,expand=FALSE)

        # ------ Scale Max -------
        hbox = GtkHBox(spacing=5)
        self.max_hbox = hbox
        vbox.pack_start(hbox)
        hbox.pack_start(GtkLabel('Scale Max:'),expand=FALSE)
        self.max_adjustment = GtkAdjustment(layer.max_get(src_index),
                                smin, smax, new_inc, new_inc, new_inc)
        self.max_adjustment.connect('value-changed',self.adjustment_cb)
        self.max_slider = GtkHScale(self.max_adjustment)
        self.max_slider.set_digits(sliderDigits)
        hbox.pack_start(self.max_slider)
        self.max_entry = GtkEntry(maxlen=8)
        self.max_entry.connect('activate',self.entry_cb)
        self.max_entry.connect('leave-notify-event',self.entry_cb)
        hbox.pack_start(self.max_entry,expand=FALSE)

        # ------ NODATA -------
        hbox = GtkHBox(spacing=5)
        self.nodata_hbox = hbox
        vbox.pack_start(hbox)
        hbox.pack_start(GtkLabel('NODATA value:'), expand=FALSE)
        self.nodata_entry = GtkEntry(maxlen=19)
        self.nodata_entry.connect('activate', self.entry_cb)
        self.nodata_entry.connect('leave-notify-event', self.entry_cb)
        hbox.pack_start(self.nodata_entry, expand=FALSE)
        if (src_index < 3) and (ds.RasterCount > src_index):
            nodata=ds.GetRasterBand(src_index+1).GetNoDataValue()
            if nodata is not None:
                if (type(nodata) != type(complex(1,0))):
                    nodata=complex(nodata,0)
                self.layer.nodata_set(src_index,nodata.real,nodata.imag)
            
        # ------- Constant Value -----
        self.const_entry = GtkEntry(maxlen=8)
        self.const_entry.connect('activate',self.const_cb)
        self.const_entry.connect('leave-notify-event',self.const_cb)
        vbox.pack_start(self.const_entry)

        self.updating = FALSE
            
        self.gui_refresh()
        
        self.connect( 'destroy', self.cleanup)

    def combo_entry_key_press_cb( self, entryBox, event, *args ) :
        import GDK

        if self.updating:
            return

        if( event.keyval == GDK.Right ) :
            try :
                currentIndex = self.__allBands.index( entryBox.get_text() )
                nextIndex = min( len(self.__allBands)-1, currentIndex+1 )
                entryBox.set_text( self.__allBands[nextIndex] )
            except ValueError : 
                return

        elif( event.keyval == GDK.Left ) : 
            try :
                currentIndex = self.__allBands.index( entryBox.get_text() )
                prevIndex = max( 0, currentIndex - 1 )
                entryBox.set_text( self.__allBands[prevIndex] )
            except ValueError : 
                return

        elif( event.keyval == GDK.Return ) : 
            entryText = entryBox.get_text()
            if( entryText in self.__bandDic.keys() ) : 
                pass
            else : 
                try :
                    bandIndex = self.__bandNums.index(entryText)
                    entryBox.set_text( self.__allBands[bandIndex] )
                except ValueError : 
                    entryBox.set_text("")
                except KeyError :
                    entryBox.set_text("")
        
    def __del__(self):
        print 'Destroying GvRasterSource'

    def cleanup(self, *args):
        self.layer = None
        self.gvraster = None

    def band_desc(self,iband):
        band = self.layer.get_parent().get_dataset().GetRasterBand(iband)
        if len(band.GetDescription()) > 0:
	    # XXX: band descriptions must be different, because we will use
	    # them as keys in dictionary. That's why we print band number
	    # here.
            return '%d: %s' % (iband,band.GetDescription())
        else:
            return '%d' % iband
        
    def gui_refresh(self, *args):

        if self.layer is None:
            return
        
        if self.flags( DESTROYED ) > 0:
            self.layer.disconnect( self.display_change_id )
            return

        if self.updating:
            return

        self.updating = TRUE
        if self.layer.get_mode() == gview.RLM_COMPLEX:
            new_min = max(0.0,self.layer.min_get(self.src_index))
        else:
            new_min = self.layer.min_get(self.src_index)

        if self.layer.min_get(self.src_index) < self.min_adjustment.lower:               
            self.min_adjustment.set_all( new_min,
                                         new_min,
                                         self.min_adjustment.upper,
                                         self.min_adjustment.step_increment,
                                         self.min_adjustment.page_increment,
                                         self.min_adjustment.page_size)
            self.min_adjustment.changed()                
            self.max_adjustment.set_all( new_min,
                                         new_min,
                                         self.max_adjustment.upper,
                                         self.max_adjustment.step_increment,
                                         self.max_adjustment.page_increment,
                                         self.max_adjustment.page_size)
            self.max_adjustment.changed()
            
        if self.layer.max_get(self.src_index) > self.max_adjustment.upper:
            self.min_adjustment.set_all( new_min,
                                         self.min_adjustment.lower,
                                         self.layer.max_get(self.src_index),
                                         self.min_adjustment.step_increment,
                                         self.min_adjustment.page_increment,
                                         self.min_adjustment.page_size)
            self.min_adjustment.changed()
            self.max_adjustment.set_all( new_min,
                                         self.max_adjustment.lower,
                                         self.layer.max_get(self.src_index),
                                         self.max_adjustment.step_increment,
                                         self.max_adjustment.page_increment,
                                         self.max_adjustment.page_size)
            self.max_adjustment.changed()

        self.min_adjustment.set_value(new_min)
        self.min_entry.set_text(str(new_min))
            
        self.max_adjustment.set_value(self.layer.max_get(self.src_index))
        self.max_entry.set_text(str(self.layer.max_get(self.src_index)))
        nodata=self.layer.nodata_get(self.src_index)
        if type(nodata) == type((1,)):
  	    self.nodata_entry.set_text(str(nodata[0])+'+'+str(nodata[1])+
                                       'j')
        else:
  	    self.nodata_entry.set_text(str(nodata))
            
        self.const_entry.set_text( \
                str(self.layer.get_const_value(self.src_index)))
        
        if self.layer.get_data(self.src_index) is None:
            self.const_entry.show()
            self.min_hbox.hide()
            self.max_hbox.hide()
            self.nodata_hbox.hide()
            self.band_combo.entry.set_text('constant')
        else:
            self.const_entry.hide()
            self.max_hbox.show()
            if ((self.layer.get_mode() != gview.RLM_COMPLEX) and
                (band_is_complex(self.layer,self.src_index) == 0)):
                self.min_hbox.show()
            else:
                self.min_hbox.hide()
            self.nodata_hbox.show()

            # Set the band selector.
            band = self.layer.get_data(self.src_index).get_band()
            dataset = self.layer.get_data(self.src_index).get_dataset()
            for iband in range(dataset.RasterCount):
                test_band = dataset.GetRasterBand(iband+1)
                if test_band._o == band._o:
                    self.band_combo.entry.set_text(self.band_desc(iband+1))
                    break

        self.updating = FALSE

    def set_band_cb(self,*args):
        if self.updating:
            return

        if self.band_combo.entry.get_text() == 'constant':
            self.layer.set_source(self.src_index, None,
                                  self.layer.min_get(self.src_index),
                                  self.layer.max_get(self.src_index),
                                  self.layer.get_const_value(self.src_index),
                                  self.layer.source_get_lut(self.src_index),
                                  None)
        else:
            try:            
                tokens = self.__bandDic[self.band_combo.entry.get_text()],
            except KeyError :
                tokens = ""
                
            try:
                band_number = int(tokens[0])
            except:
                return

            dataset = self.layer.get_parent().get_dataset()
            raster = gview.manager.get_dataset_raster( dataset, band_number )
            if raster is not None:
                if( self.layer.get_property('_scale_lock') is not None and 
                    self.layer.get_property('_scale_lock') == 'locked' ) : 

                    if( self.layer.get_property("_scale_limits") ) :
                        rasterMin, rasterMax = \
                            map(atof, split(self.layer.get_property("_scale_limits")))
                else :
                    rasterMin = raster.get_min()
                    rasterMax = raster.get_max()

                self.layer.set_source(self.src_index, raster,
                                    rasterMin, rasterMax,
                                    self.layer.get_const_value(self.src_index),
                                    self.layer.source_get_lut(self.src_index),
                          dataset.GetRasterBand(band_number).GetNoDataValue())
                
        if self.src_index < 3 and self.master_dialog.greyscale_is_set():
            self.master_dialog.enforce_greyscale(self.src_index)

        # enable alpha support if user modifies alpha band.
        if self.src_index == 3:
            self.layer.blend_mode_set( RL_BLEND_FILTER )

        self.gui_refresh()
        
    def adjustment_cb(self,adjustment,*args):
        if self.updating:
            return

        value = adjustment.value
        if value < -1 or value > 1:
            value = int(value*10) / 10.0

        if adjustment == self.min_adjustment:
            self.layer.min_set( self.src_index, value )
        else:
            self.layer.max_set( self.src_index, value )
        
        if self.src_index < 3 and self.master_dialog.greyscale_is_set():
            self.master_dialog.enforce_greyscale(self.src_index)

    
    def entry_cb(self,entry,*args):
        if self.updating:
            return

        try:
            value = complex(entry.get_text())
	except:
	    return

	if entry == self.min_entry:
	    self.layer.min_set( self.src_index, value.real )
	elif entry == self.max_entry:
	    self.layer.max_set( self.src_index, value.real )
	else:
            self.layer.nodata_set( self.src_index, value.real, value.imag )

        if self.src_index < 3 and self.master_dialog.greyscale_is_set():
            self.master_dialog.enforce_greyscale(self.src_index)

    def const_cb(self,entry,*args):
        if self.updating:
            return

        try:
            self.layer.set_source(self.src_index,
                                  self.layer.get_data(self.src_index),
                                  self.layer.min_get(self.src_index),
                                  self.layer.max_get(self.src_index),
                                  int(entry.get_text()),
                                  self.layer.source_get_lut(self.src_index),
                                  self.layer.nodata_get(self.src_index))
        except:
            self.const_entry.set_text( \
                str(self.layer.get_const_value(self.src_index)))

        # enable alpha support if user modifies alpha band.
        if self.src_index == 3:
            self.layer.blend_mode_set( RL_BLEND_FILTER )
    
        if self.src_index < 3 and self.master_dialog.greyscale_is_set():
            self.master_dialog.enforce_greyscale(self.src_index)

class GvRasterPropDialog(GtkWindow):

    def __init__(self, layer):
        GtkWindow.__init__(self)
        self.set_border_width(3)
        if layer is not None:
            self.set_title(layer.get_name()+' Properties')
        else:
            self.set_title('Raster Properties')

        gvhtml.set_help_topic( self, "gvrasterpropdlg.html" )
        self.layer = layer
        self.updating = FALSE

        if self.layer is not None:
            self.display_change_id = self.layer.connect('display-change',
                                                        self.refresh_cb)
            self.teardown_id = layer.connect('teardown',self.close)

        
        # create the general layer properties dialog
        self.create_notebook()

        self.create_pane1()
        
        self.updating = TRUE
        self.create_sourcepane()
        self.updating = FALSE
        
        self.create_openglprop()
        self.create_lutprop()
	self.create_projprop()
        self.create_imageinfo()

        self.update_gui()
        self.show_all()
        self.update_gui()
        
        for source in self.sources:
            source.gui_refresh()

    def __del__(self):
        print 'disconnect:', self.display_change_id
        self.layer.disconnect(self.display_change_id)

    def create_notebook(self):
        self.notebook = GtkNotebook()
        self.add( self.notebook )
        self.connect('delete-event', self.close)

    def create_lutprop(self):
        
        self.lut_pane = GtkVBox(spacing=10)
        self.lut_pane.set_border_width(10)
        self.notebook.append_page( self.lut_pane, GtkLabel('LUT'))

        self.lut_preview = GtkPreview()
        self.lut_preview.size(256,32)
        self.lut_pane.pack_start(self.lut_preview)

        self.complex_lut_om = \
            gvutils.GvOptionMenu(('Magnitude', 'Phase',
                                  'Magnitude & Phase', 'Real','Imaginary'),
                                 self.complex_lut_cb)
        self.lut_pane.pack_start(self.complex_lut_om, expand=FALSE)

    def create_sourcepane(self):
        self.sources = []
        self.source_pane = GtkVBox(spacing=10)
        self.source_pane.set_border_width(10)
        self.notebook.append_page( self.source_pane, GtkLabel('Raster Source'))

        if self.layer.get_mode() == gview.RLM_RGBA:

            source = GvRasterSource('Red',self.layer,0,self)
            self.source_pane.pack_start(source, expand=FALSE)
            self.sources.append(source)
            
            source = GvRasterSource('Green',self.layer,1,self)
            self.source_pane.pack_start(source, expand=FALSE)
            self.sources.append(source)
            
            source = GvRasterSource('Blue',self.layer,2,self)
            self.source_pane.pack_start(source, expand=FALSE)
            self.sources.append(source)
            
            source = GvRasterSource('Alpha',self.layer,3,self)
            self.source_pane.pack_start(source, expand=FALSE)
            self.sources.append(source)

            self.grey_toggle = GtkCheckButton(label='Greyscale Lock')
            self.grey_toggle.connect('toggled', self.greyscale_cb)
            self.source_pane.pack_start(self.grey_toggle, expand=FALSE)
            self.grey_toggle.set_active( self.greyscale_is_set() )

            scaleHBox = GtkHBox(spacing=10)
            self.scale_toggle = GtkCheckButton(label="Scale Lock")
            self.scale_min_entry = GtkEntry()
            self.scale_max_entry = GtkEntry()
            self.scale_min_entry.connect( "activate", self.activateLockEntry_cb )
            self.scale_max_entry.connect( "activate", self.activateLockEntry_cb )
            w, h = self.scale_min_entry.size_request()
            self.scale_min_entry.set_usize(50, h)
            self.scale_max_entry.set_usize(50, h)


            scaleHBox.pack_start( self.scale_toggle    ) 
            scaleHBox.pack_start( self.scale_min_entry )
            scaleHBox.pack_start( self.scale_max_entry )
            
            self.scale_toggle.connect( "toggled", self.scalelock_cb)
            self.source_pane.pack_start( scaleHBox, expand=FALSE )
            self.scale_toggle.set_active( self.scalelock_is_set() )
            
        else:
            source = GvRasterSource('Raster',self.layer,0,self)
            self.source_pane.pack_start(source, expand=FALSE)
            self.sources.append(source)
        
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

    def create_openglprop(self):
        oglpane = GtkVBox(spacing=10)
        oglpane.set_border_width(10)
        self.notebook.append_page(oglpane, GtkLabel('Draw Style'))

        # Create Modulation Color
        box = GtkHBox(spacing=5)
        oglpane.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Modulation Color:'),expand=FALSE)
        self.mod_color = pgucolorsel.ColorControl('Modulation Color',
                                                  self.color_cb,None)
        box.pack_start(self.mod_color)

        # Create Interpolation Control
        box = GtkHBox(spacing=5)
        oglpane.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Subpixel Interpolation:'),expand=FALSE)
        self.interp_om = gvutils.GvOptionMenu(('Linear','Off (Nearest)'), \
                                              self.set_interp_cb)
        box.pack_start(self.interp_om,expand=FALSE)

    def create_projparms(self):
	"""Create projection parameters controls"""

	self.parm_dict = {}
	if self.proj_table is not None:
	    self.proj_table.destroy()
	self.proj_table = GtkTable(2, len(self.proj_parms[self.proj_index]))
	self.proj_table.set_border_width(5)
	self.proj_table.set_row_spacings(5)
	self.proj_table.set_col_spacings(5)
        self.proj_table.show()
	row = 0
	for i in self.proj_parms[self.proj_index]:
	    parm_label = GtkLabel(i[1])
	    parm_label.set_alignment(0, 0.5)
	    self.proj_table.attach(parm_label, 0, 1, row, row + 1)
	    parm_label.show()
	    parm_value = self.sr.GetProjParm(i[0])
	    if parm_value is None:
		parm_value = str(i[3])
	    parm_entry = GtkEntry()
	    parm_entry.set_text(str(parm_value))
	    self.parm_dict[i[0]] = parm_value
	    parm_entry.set_editable(TRUE)
	    parm_entry.connect('changed', self.parm_entry_cb, i[0])
	    self.proj_table.attach(parm_entry, 1, 2, row, row + 1)
	    parm_entry.show()
	    row += 1

	self.proj_vbox.pack_end(self.proj_table, expand=FALSE)
	
    def create_projprop(self):
        projpane = GtkVBox(spacing=10)
        projpane.set_border_width(10)
        self.notebook.append_page(projpane, GtkLabel('Coordinate System'))

	# Projection frame
	proj_frame = GtkFrame('Projection')
	proj_frame.show()
        projpane.pack_start(proj_frame, expand=FALSE)
	self.proj_vbox = GtkVBox(spacing=5)

	# Fetch projection record
	self.proj_full = ''
	proj_name = ''
	projection = self.layer.get_projection()

        self.sr = None
        if projection is not None and len(projection) > 0:
            self.sr = osr.SpatialReference()
            if self.sr.ImportFromWkt( projection ) == 0:
                self.proj_full = self.sr.ExportToPrettyWkt( simplify = 1 )
		if self.proj_full is None:
		    self.proj_full = ''
		proj_name = self.sr.GetAttrValue("PROJECTION")
		if proj_name is None:
		    proj_name = ''

        # Create projection switch
	proj_hbox = GtkHBox(spacing=5)
	proj_hbox.pack_start(GtkLabel('Projection Name:'), \
	    expand=FALSE, padding=5)
	proj_methods = osr.GetProjectionMethods()
	self.projs = map(lambda x: x.__getitem__(0), proj_methods)
	self.projs.insert(0, '')
	proj_names = map(lambda x: x.__getitem__(1), proj_methods)
	proj_names.insert(0, 'None')
	self.proj_parms = map(lambda x: x.__getitem__(2), proj_methods)
	self.proj_parms.insert(0, [])
	self.proj_index = self.projs.index(proj_name)

	self.proj_table = None
	self.proj_om = gvutils.GvOptionMenu(proj_names, self.set_proj_cb)
	self.create_projparms()
	self.proj_om.set_history(self.proj_index)
	proj_hbox.pack_start(self.proj_om, padding=5)
	self.proj_vbox.pack_start(proj_hbox, expand=FALSE)

	proj_frame.add(self.proj_vbox)

	# Datum frame
	datum_frame = GtkFrame('Datum')
	datum_frame.show()
        projpane.pack_start(datum_frame, expand=FALSE)
	datum_hbox = GtkHBox(spacing=5)
	datum_hbox.pack_start(GtkLabel('Datum Name:'), expand=FALSE, padding=5)

        try:
            self.datum_name = self.sr.GetAttrValue("DATUM")
        except:
            self.datum_name = None
            
	self.datum_names = {None:"None", osr.SRS_DN_NAD27:"NAD27", \
	    osr.SRS_DN_NAD83:"NAD83", osr.SRS_DN_WGS72:"WGS72", \
	    osr.SRS_DN_WGS84:"WGS84"}
	try:
	    self.datum_index = self.datum_names.keys().index(self.datum_name)
	except ValueError:
	    self.datum_index = self.datum_names.keys().index(None)
	self.datum_om = gvutils.GvOptionMenu(self.datum_names.values(), \
	    self.set_datum_cb)
	self.datum_om.set_history(self.datum_index)
	datum_hbox.pack_start(self.datum_om, expand=FALSE, padding=5)

	datum_frame.add(datum_hbox)

	# Units frame
	units_frame = GtkFrame('Units')
	#units_frame.show()
        #projpane.pack_start(units_frame, expand=FALSE)
	units_hbox = GtkHBox(spacing=5)
	units_hbox.pack_start(GtkLabel('Units:'), expand=FALSE, padding=5)

	units_frame.add(units_hbox)

	# WKT frame
	proj_text_frame = GtkFrame('Well Known Text')
	proj_text_frame.show()
	projpane.pack_end(proj_text_frame, expand=TRUE)

	self.proj_text = GtkText()
	self.proj_text.set_line_wrap(TRUE)
	self.proj_text.set_word_wrap(FALSE)
	self.proj_text.set_editable(FALSE)
	self.proj_text.show()
	self.proj_text.insert_defaults(self.proj_full)

	proj_scrollwin = GtkScrolledWindow()
	proj_scrollwin.set_usize(0, 300)
        proj_scrollwin.add(self.proj_text)
	proj_text_frame.add(proj_scrollwin)

    def create_imageinfo(self):
        iipane = GtkVBox(spacing=10)
        iipane.set_border_width(10)
        self.notebook.append_page( iipane, GtkLabel('Image Info') )

        self.ii_text = GtkText()
        self.ii_text.set_line_wrap(FALSE)
        self.ii_text.set_word_wrap(FALSE)
        self.ii_text.set_editable(FALSE)
        self.ii_text.show()

        self.ii_scrollwin = GtkScrolledWindow()
        self.ii_scrollwin.add( self.ii_text)
        iipane.pack_start(self.ii_scrollwin,expand=TRUE)

        # Now create and assign the text contents.
        gdal_ds = self.layer.get_parent().get_dataset()

        text = ''

        text = text + 'Filename: ' + gdal_ds.GetDescription() + '\n'

        text = text + 'Size: ' + str(gdal_ds.RasterXSize) + 'P x '
        text = text +            str(gdal_ds.RasterYSize) + 'L x '
        text = text +            str(gdal_ds.RasterCount) + 'Bands\n'

        driver = gdal_ds.GetDriver()
        text = text + 'Driver: ' + driver.LongName + '\n'

        transform = gdal_ds.GetGeoTransform()
        if transform[2] == 0.0 and transform[4] == 0.0:
            text = text + 'Origin: ' + str(transform[0])               \
                               + ' ' + str(transform[3]) + '\n'
            text = text + 'Pixel Size: ' + str(transform[1])           \
                                 + ' x ' + str(transform[5]) + '\n'
                                               
        projection = gdal_ds.GetProjection()
        if ((projection is None) or (len(projection) == 0)):
            projection = gdal_ds.GetGCPProjection()

        if projection is None:
            projection=""
            
        if len(projection) > 0:
            sr = osr.SpatialReference()
            if sr.ImportFromWkt( projection ) == 0:
                projection = sr.ExportToPrettyWkt( simplify = 1 )

        text = text + 'Projection:\n'
        text = text + projection + '\n'

        metadata = gdal_ds.GetMetadata()
        if len(metadata) > 0:
            text = text + 'Metadata:\n'
            for item in metadata.items():
                text = text + '    '+item[0]+': '+item[1]+'\n'

        for band_index in range(gdal_ds.RasterCount):
            band = gdal_ds.GetRasterBand(band_index+1)

            text = text + 'Band %2d: Type=' % (band_index+1)
            text = text + gdal.GetDataTypeName(band.DataType)
            if len(band.GetDescription()) > 0:
                text = text + ' - ' + band.GetDescription()
            text = text + '\n'

        self.ii_text.insert_defaults(text)

    # Initialize GUI state from underlying object state.
    def update_gui(self):
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

        # modulation color
        tflag, tcolor = self.layer.texture_mode_get()
        if tflag == 0:
            tcolor = (1,1,1,1)
        self.mod_color.set_color(tcolor)

        # Interpolation Mode
        zmin, zmax = self.layer.zoom_get()
        if zmax == RL_FILTER_BILINEAR:
            self.interp_om.set_history(0)
        else:
            self.interp_om.set_history(1)

        self.updating = FALSE

        # LUT
        if self.layer.get_mode() != gview.RLM_RGBA:
            lut_tuple = self.layer.lut_get()
        else:
            if self.greyscale_is_set() and band_is_complex(self.layer,0):
                # Only show complex lut frame when bands are locked,
                # because that's the only time it makes sense
                # to apply non-magnitude luts.
                lut_tuple = self.layer.lut_get(rgba_complex=1)
                # Don't let the user modulate alpha by a band, because
                # results won't make sense unless the LUT is magnitude
                # (when alpha is not constant, it uses the red component
                # of the lookup table for the modulating band- this will
                # give the expected behaviour if the LUT is magnitude,
                # but will give non-sensible results if the LUT
                # is phase). 
                self.sources[3].hide()
            else:
                lut_tuple = self.layer.lut_get()
                self.sources[3].show()
            
        if lut_tuple is None:
            self.lut_pane.hide()
        elif lut_tuple[2] == 1:
            lut_rgba = lut_tuple[0]
            lut_rgb = gview.rgba_to_rgb(lut_rgba)
            
            self.lut_pane.show()
            self.lut_preview.size(256,32)

            for i in range(32):
                self.lut_preview.draw_row( lut_rgb, 0, i, 256)

            self.complex_lut_om.hide()
            self.lut_preview.queue_draw()
        else:
            lut_rgba = lut_tuple[0]
            lut_rgb = gview.rgba_to_rgb(lut_rgba)
            
            self.lut_pane.show()
            self.lut_preview.size(256,256)
            for row in range(256):
                row_data = lut_rgb[row*768:(row+1)*768]
                self.lut_preview.draw_row( row_data, 0, row, 256)

            self.complex_lut_om.show()
            self.lut_preview.queue_draw()

    def name_cb(self, *args):
        if self.layer_name.get_text() != self.layer.get_name():
            self.layer.set_name( self.layer_name.get_text() )

    # Visibility changing
    def visibility_cb( self, widget ):
        self.layer.set_visible( self.vis_yes.active )

    # Readonly changing
    def edit_cb( self, widget ):
        self.layer.set_read_only( self.edit_no.active )

    def scalelock_is_set( self ) : 
        if( self.layer.get_property('_scale_lock') is not None and
            self.layer.get_property('_scale_lock') == 'locked' ) :
                return 1
        else :
            return 0

    def activateLockEntry_cb( self, *args ) : 
        if( self.scale_toggle.get_active() ) :
            self.scalelock_cb()

    def scalelock_cb( self, *args ) : 
        if( self.scalelock_is_set() ) : 
            self.layer.set_property('_scale_lock', 'unlocked')
        else :
            self.layer.set_property('_scale_lock', 'locked'  )

        if( self.scalelock_is_set() ):
            try :
                min_scale = atof( self.scale_min_entry.get_text() )
                max_scale = atof( self.scale_max_entry.get_text() )
            except ValueError : 
                min_scale, max_scale = self.layer.min_get(0), self.layer.max_get(0)
                self.scale_min_entry.set_text( str(min_scale) )
                self.scale_max_entry.set_text( str(max_scale) )

            self.layer.set_property \
                ('_scale_limits', str(min_scale) + ' ' + str(max_scale) )

            for iSource in [0,1,2] :
                self.layer.min_set(iSource, min_scale)
                self.layer.max_set(iSource, max_scale)
            
    def greyscale_is_set(self):
        if self.layer.get_property('_greyscale_lock') is not None \
           and self.layer.get_property('_greyscale_lock') == 'locked':
            return 1
        else:
            return 0
    
    def greyscale_cb(self, *args):
        if self.greyscale_is_set():
            self.layer.set_property('_greyscale_lock','unlocked')

            if self.layer.get_mode() == gview.RLM_RGBA:
                self.complex_lut_om.set_history(0)
                self.layer.complex_lut('magnitude')
        else:
            self.layer.set_property('_greyscale_lock','locked')

        self.grey_toggle.set_active( self.greyscale_is_set() )

        if self.greyscale_is_set():
            self.enforce_greyscale(0)

        # show/hide lut as necessary    
        self.update_gui()

    def enforce_greyscale(self, isrc):
        if isrc != 0:
            self.layer.set_source(0, self.layer.get_data(isrc),
                                  self.layer.min_get(isrc),
                                  self.layer.max_get(isrc),
                                  self.layer.get_const_value(isrc),
                                  self.layer.source_get_lut(isrc),
                                  self.layer.nodata_get(isrc))

        if isrc != 1:
            self.layer.set_source(1, self.layer.get_data(isrc),
                                  self.layer.min_get(isrc),
                                  self.layer.max_get(isrc),
                                  self.layer.get_const_value(isrc),
                                  self.layer.source_get_lut(isrc),
                                  self.layer.nodata_get(isrc))

        if isrc != 2:
            self.layer.set_source(2, self.layer.get_data(isrc),
                                  self.layer.min_get(isrc),
                                  self.layer.max_get(isrc),
                                  self.layer.get_const_value(isrc),
                                  self.layer.source_get_lut(isrc),
                                  self.layer.nodata_get(isrc))

        # In multi-band complex case, reset alpha band to a constant
        if band_is_complex(self.layer,0):
            self.layer.set_source(3, None,
                                  self.layer.min_get(3),
                                  self.layer.max_get(3),
                                  self.layer.get_const_value(3),
                                  self.layer.source_get_lut(3),
                                  None)
    
    def complex_lut_cb(self, *args):
        # Magnitude
        if self.complex_lut_om.get_history() == 0:
            method = 'magnitude'
            
        # Phase
        elif self.complex_lut_om.get_history() == 1:
            method = 'phase'

        # Magnitude and Phase
        elif self.complex_lut_om.get_history() == 2:
            method = 'magphase'

        # Real
        elif self.complex_lut_om.get_history() == 3:
            method = 'real'

        # Imaginary
        elif self.complex_lut_om.get_history() == 4:
            method = 'imaginary'

        self.layer.complex_lut( method )
        
        self.update_gui()

    # Set modulation color
    def color_cb( self, color, type ):
        #if color[0] == 1.0 and color[1] == 1.0 \
        #   and color[2] == 1.0 and color[3] == 1.0:
        #    pass
        #else:
        if color[3] != 1.0:
            self.layer.blend_mode_set( RL_BLEND_FILTER )
        self.layer.texture_mode_set( 1, color )
            

    def set_interp_cb(self,*args):
        if self.interp_om.get_history() == 0:
            self.layer.zoom_set(RL_FILTER_BILINEAR,RL_FILTER_BILINEAR)
        else:
            self.layer.zoom_set(RL_FILTER_NEAREST,RL_FILTER_NEAREST)

    def update_proj_text(self):
	"""Update text control showing projection information"""
	self.proj_full = self.sr.ExportToPrettyWkt( simplify = 1 )
	if self.proj_full is None:
		self.proj_full = ''
	self.proj_text.delete_text(0, self.proj_text.get_length())
	self.proj_text.insert_defaults(self.proj_full)
    
    def parm_entry_cb(self, entry, parm):
	"""Set projection parameters"""
	self.parm_dict[parm] = float(entry.get_text())
	self.sr.SetNormProjParm(parm, self.parm_dict[parm])

	self.update_proj_text()

    def set_proj_cb(self,*args):
	"""Set projection"""
	if self.proj_index != self.proj_om.get_history():
	    self.proj_index = self.proj_om.get_history()
	    self.sr = osr.SpatialReference()
	    self.sr.SetWellKnownGeogCS(self.datum_names[self.datum_name])
	    self.sr.SetProjection(self.projs[self.proj_index])
	    for i in self.proj_parms[self.proj_index]:
		try:
		    self.sr.SetNormProjParm(i[0], self.parm_dict[i[0]])
		except KeyError:
		    self.sr.SetNormProjParm(i[0], i[3])
	    self.layer.set_projection(self.sr.ExportToWkt())
	    self.create_projparms()

	    self.update_proj_text()

    def set_datum_cb(self, *args):
	"""Set datum"""
	if self.datum_index != self.datum_om.get_history():
	    self.datum_index = self.datum_om.get_history()
	    self.datum_name = self.datum_names.keys()[self.datum_index]
	    self.sr.SetWellKnownGeogCS(self.datum_names[self.datum_name])
	    self.update_proj_text()

    # Dialog closed, remove references to python object
    def close( self, *args ):
        prop_dialog_list.remove(self)
        self.layer.disconnect(self.display_change_id)
        self.layer.disconnect(self.teardown_id)

        self.sources = None
        self.layer = None
        self.destroy()
        
    # Force GUI Refresh
    def refresh_cb( self, widget, args ):
        self.update_gui()

def band_is_complex(layer,src_index):
    """ Returns 1 if src_index'th band of layer is present
        and complex; 0 otherwise.
    """
    
    try:
        srctype=layer.get_data(src_index).get_band().DataType
        ctypes=[gdal.GDT_CInt16, gdal.GDT_CInt32, gdal.GDT_CFloat32,
                        gdal.GDT_CFloat64]
        if srctype in ctypes:
            return 1

        return 0
    except:
        return 0
        
if __name__ == '__main__':
    dialog = GvRasterPropDialog(None)
    dialog.connect('delete-event', mainquit)

    mainloop()
