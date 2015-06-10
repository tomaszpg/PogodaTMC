###############################################################################
# $Id: reproject.py,v 1.1 2006/03/25 18:13:51 andrey_kiselev Exp $
#
# Project:  OpenEV Python tools
# Purpose:  Tool to reproject georeferenced datasets
# Author:   Andrey Kiselev, dron@ak4719.spb.edu
#
###############################################################################
# Copyright (c) 2006, Andrey Kiselev <dron@ak4719.spb.edu>
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################
#
#  $Log: reproject.py,v $
#  Revision 1.1  2006/03/25 18:13:51  andrey_kiselev
#  Added new 'Reprojection' tool.
#
#

from gtk import *

import gview
import gviewapp
import gvutils
import pgufilesel
from gdalconst import *
import gdal
import osr

def layer_is_raster(layer):
    """Return TRUE if layer is raster and FALSE otherwise"""
    try:
        layer.get_nodata(0)
        return TRUE
    except:
        return FALSE

class ReprojectionTool(gviewapp.Tool_GViewApp):
    
    def __init__(self,app=None):
        gviewapp.Tool_GViewApp.__init__(self,app)
        self.init_menu()

    def launch_dialog(self,*args):
	self.win = ReprojectionDialog()
        self.win.show()

    def init_menu(self):
        self.menu_entries.set_entry("Tools/Reproject...",2,self.launch_dialog)

class ReprojectionDialog(GtkWindow):
    def __init__(self,app=None):
        
	self.layer = gview.app.sel_manager.get_active_layer()
	if not layer_is_raster(self.layer):
	    gvutils.error("Please select a raster layer.");
	    return
	
	# Fetch projection record
	self.proj_full = ''
	self.proj_name = ''
	projection = self.layer.get_projection()

        self.sr = None
        if projection is not None and len(projection) > 0:
            self.sr = osr.SpatialReference()
            if self.sr.ImportFromWkt(projection) == 0:
                self.proj_full = self.sr.ExportToPrettyWkt(simplify = 1)
		if self.proj_full is None:
		    self.proj_full = ''
		self.proj_name = self.sr.GetAttrValue("PROJECTION")
		if self.proj_name is None:
		    self.proj_name = ''

	GtkWindow.__init__(self)
        self.set_title('Reproject')
        self.create_gui()
        self.show()
	self.app=app

    def show(self):
        GtkWindow.show_all(self)

    def close(self, *args):
        self.hide()
        self.visibility_flag = 0
        return TRUE

    def create_gui(self):
        box1 = GtkVBox(spacing = 10)
	box1.set_border_width(10)
        self.add(box1)
        box1.show()

	box2 = GtkHBox(spacing=10)
        box1.pack_start(box2, expand=TRUE)
        box2.show()

	# Input WKT frame
	inproj_frame = GtkFrame('Input Well Known Text')
	inproj_frame.show()
        box2.pack_start(inproj_frame, expand=TRUE)

	inproj_text = GtkText()
	inproj_text.set_line_wrap(TRUE)
	inproj_text.set_word_wrap(FALSE)
	inproj_text.set_editable(FALSE)
	inproj_text.show()
	inproj_text.insert_defaults(self.proj_full)

	proj_scrollwin = GtkScrolledWindow()
        proj_scrollwin.add(inproj_text)
	proj_scrollwin.set_usize(300, 300)
	inproj_frame.add(proj_scrollwin)

	# Separation label
	box2.pack_start(GtkLabel('-->'), expand=FALSE)

	# Output projection box
	box3 = GtkVBox(spacing = 10)
	box2.pack_start(box3, expand=FALSE)
	box3.show()

	# Projection frame
	proj_frame = GtkFrame('Output Projection')
	proj_frame.show()
        box3.pack_start(proj_frame, expand=FALSE)
	self.proj_vbox = GtkVBox(spacing=5)

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
	self.proj_index = self.projs.index(self.proj_name)

	self.proj_table = None
	self.proj_om = gvutils.GvOptionMenu(proj_names, self.set_proj_cb)
	self.create_projparms()
	self.proj_om.set_history(self.proj_index)
	proj_hbox.pack_start(self.proj_om, padding=5)
	self.proj_vbox.pack_start(proj_hbox, expand=FALSE)

	proj_frame.add(self.proj_vbox)

	# Datum frame
	datum_frame = GtkFrame('Output Datum')
	datum_frame.show()
        box3.pack_start(datum_frame, expand=FALSE)
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

	# Reprojection parameters frame
	rparmsframe = GtkFrame('Reprojection parameters')
	rparmsframe.show()
        box3.pack_start(rparmsframe, expand=FALSE)

	rparmstable = GtkTable(2, 3, FALSE)
	rparmstable.set_border_width(5)
        rparmstable.set_row_spacings(5)
        rparmstable.set_col_spacings(5)
	rparmsframe.add(rparmstable)
	rparmstable.show()

	label = GtkLabel('Interpolation Method:')
        label.set_alignment(0, 0.5)
        rparmstable.attach(label, 0, 1, 0, 1)

	self.interp_methods = [
	    'Nearest Neighbour', \
	    'Bilinear', \
	    'Cubic Convolution', \
	    'Cubic Spline' \
	]
	self.interp_menu = gvutils.GvOptionMenu(self.interp_methods)
        self.interp_menu.set_history(0)
        rparmstable.attach(self.interp_menu, 1, 2, 0, 1)

	# Output file frame
	fileframe = GtkFrame('Select output file')
	fileframe.show()
        box3.pack_start(fileframe, expand=FALSE)

	filetable = GtkTable(2, 3, FALSE)
	filetable.set_border_width(5)
        filetable.set_row_spacings(5)
        filetable.set_col_spacings(5)
	fileframe.add(filetable)
	filetable.show()

	open_btn = GtkButton('Open...')
	open_btn.connect("clicked", self.open_cb)
	filetable.attach(open_btn, 0, 1, 0, 1)
	self.open_entry = GtkEntry()
	self.open_entry.set_editable(TRUE)
	self.open_entry.set_text('')
	filetable.attach(self.open_entry, 1, 2, 0, 1)
	fileframe.add(filetable)

	label = GtkLabel('Output Format:')
        label.set_alignment(0, 0.5)
        filetable.attach(label, 0, 1, 1, 2)

        self.format_list = []
        hist_idx = 0
	for driver in gdal.GetDriverList():
	    create = None
	    try:
		create = driver.GetMetadata()["DCAP_CREATE"]
	    except KeyError:
		pass        
	    if create == "YES":
		if driver.ShortName == 'DTED':
		    # DTED is a special case that needs certain
		    # conditions to be valid.  Skip it.
		    continue
		self.format_list.append(driver.ShortName)
        self.format_list.sort()
        # Default to GTiff if possible
	try:
	    hist_idx = self.format_list.index('GTiff')
	except ValueError:
	    pass
	
	self.format_menu = gvutils.GvOptionMenu(self.format_list)
        self.format_menu.set_history(hist_idx)
        filetable.attach(self.format_menu,1,2,1,2)

	optlabel = GtkLabel('Create Options:')
        optlabel.set_alignment(0, 0.5)
	filetable.attach(optlabel, 0, 1, 2, 3)

        self.optentry = GtkEntry()
        self.optentry.set_editable(editable = TRUE)
        self.optentry.set_text('')
	filetable.attach(self.optentry, 1, 2, 2, 3)

	# WKT frame
	proj_text_frame = GtkFrame('Output Well Known Text')
	proj_text_frame.show()
	box2.pack_start(proj_text_frame, expand=TRUE)

	self.proj_text = GtkText()
	self.proj_text.set_line_wrap(TRUE)
	self.proj_text.set_word_wrap(FALSE)
	self.proj_text.set_editable(FALSE)
	self.proj_text.show()
	self.proj_text.insert_defaults(self.proj_full)

	proj_scrollwin = GtkScrolledWindow()
	proj_scrollwin.set_usize(300, 300)
        proj_scrollwin.add(self.proj_text)
	proj_text_frame.add(proj_scrollwin)

	self.switch_new_view = GtkCheckButton("Create new view")
	box1.pack_start(self.switch_new_view, expand=FALSE)
	self.switch_new_view.show()

	separator = GtkHSeparator()
	box1.pack_start(separator, expand=FALSE)

	box4 = GtkHBox(spacing=10)
        box1.pack_end(box4, expand=FALSE)
        box4.show()

        execute_btn = GtkButton("Ok")
        execute_btn.connect("clicked", self.execute_cb)
	box4.pack_start(execute_btn)
        
        close_btn = GtkButton("Cancel")
        close_btn.connect("clicked", self.close)
        box4.pack_start(close_btn)

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
	
    def open_cb(self, *args):
        if gview.get_preference('save_recent_directory') == 'on':
	    recent_dir = gview.get_preference('recent_directory')
	else:
	    recent_dir = None
            
        filename = pgufilesel.GetFileName(title = "Select output file", \
		default_filename = recent_dir)
        if filename is None:
            return
        self.open_entry.set_text(filename)

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

    def execute_cb( self, *args ):
	src_ds = self.layer.get_parent().get_dataset()

	dst_filename = self.open_entry.get_text()
	dst_wkt = self.proj_full

	dst_driver = gdal.GetDriverByName( \
	    self.format_list[self.format_menu.get_history()])

	# Parse creation options:
        optstr = self.optentry.get_text().strip()
        if len(optstr) > 0:
            # should be able to deal with several
            # types of entries, eg.
            # 'TILED=YES','TFW=YES'
            # and
            # TILED=YES,TFW=YES

            if optstr[0] in ["'", '"']:
                split1 = optstr.split(",")
                create_options = []
                for item in split1:
                    if len(item) > 2:
                        create_options.append(item[1:len(item)-1])
            else:    
                create_options = optstr.split(",")
        else:
            create_options = []

	eResampleAlg = self.interp_menu.get_history()

	gdal.CreateAndReprojectImage(src_ds, dst_filename, None, \
	    dst_wkt, dst_driver, create_options, eResampleAlg, \
	    warp_memory = 0.0, maxerror = 0.0 )

	if self.switch_new_view.get_active():
	    gview.app.new_view()
	gview.app.file_open_by_name(dst_filename)

TOOL_LIST = ['ReprojectionTool']

