##############################################################################
# $Id: isodata.py,v 1.1 2005/08/26 18:27:35 andrey_kiselev Exp $
#
# Project:  OpenEV
# Purpose:  ISODATA clustering
# Author:   Iscander Latypov
#	    Andrey Kiselev, dron@remotesensing.org
#
###############################################################################
# Copyright (c) 2004, American Museum of Natural History. All rights reserved.
# This software is based upon work supported by NASA under award
# number NAG5-12333
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
#  $Log: isodata.py,v $
#  Revision 1.1  2005/08/26 18:27:35  andrey_kiselev
#  New.
#
#

from gtk import *

from Numeric import *
import gview
import gvutils
import gviewapp
import gdal
from gdalconst import *
import gdalnumeric


   
########################################################################
def get_raster_size(_layer):
    w =  _layer.get_parent().get_dataset().GetRasterBand(1).XSize
    h =  _layer.get_parent().get_dataset().GetRasterBand(1).YSize
    return (w,h)

########################################################################
def get_list_of_layers_as_dict():
    """Returns dictionary of opened layers. The key of dictionary is
    the name of layer, members of dictionary are view object (index = 0)
    and layer object (index = 1)"""

    dict = {}
    for curview in gview.app.view_manager.view_list:
        for curlayer in curview.viewarea.list_layers():
    	    curname = curlayer.get_name()
	    dict[curname] = (curview,curlayer) 
    if dict is None:
	return None
    return dict

########################################################################
def get_list_of_layers_as_menu():
    """Returns GtkMenu object for selecting of opened layers. 
    If number of opened layers is zero, the result is None"""
    menu = GtkMenu()
    group = None
    for curview in gview.app.view_manager.view_list:
        for curlayer in curview.viewarea.list_layers():
    	    curname = curlayer.get_name()
	    menuitem = GtkRadioMenuItem(group,curname)
	    group = menuitem
	    menu.append(menuitem)
	    menuitem.show()
    if group is None:
	return None
    return menu
	    
#########################################################################
def get_list_of_bands_as_dict():
    """Returns dictionary of the bands of the opened layers. The key 
    of dictionary is the name of layer+band number, members of dictionary 
    are view-object (index = 0), layer-object (index = 1) and band-number"""

    _size = get_raster_size(gview.app.sel_manager.get_active_layer())
    dict = {}
    for curview in gview.app.view_manager.view_list:
        for curlayer in curview.viewarea.list_layers():
    	    curname = curlayer.get_name()
	    cursize = get_raster_size(curlayer)
	    if cursize == _size:
		num_bands = curlayer.get_parent().get_dataset().RasterCount
		for i in range(num_bands):
	    	    curband = curname + '['+ str(i) + ']'
		    dict[curband] = (curview,curlayer,i) 
    if dict is None:
	return None
    return dict

############################################################################
#
#
############################################################################
def L1(v1,v2):
    return sum(abs(v1-v2))
###########################################################################    
def L2(v1,v2):
    delta = (v1-v2)
    return dot(delta,delta)
###########################################################################
def L3(v1,v2):
    delta = abs(v1-v2)
    return max(delta)
###########################################################################
class IsodataTool(gviewapp.Tool_GViewApp):
    
    def __init__(self,app=None):
        gviewapp.Tool_GViewApp.__init__(self,app)
        self.init_menu()

    def launch_dialog(self,*args):
        self.win = ISODATADialog()
	if self.win is None:
	    return
	else:
	    self.win.update_gui()
    	    self.win.show()

    def init_menu(self):
        self.menu_entries.set_entry("Image/Classification/ISOData",2,
                                    self.launch_dialog)

############################################################################
class ClassesTable(GtkWindow):
    def __init__(self,nBands,app=None):
	GtkWindow.__init__(self)
	self.set_title('Classification Info')
	self.nBands = nBands
	self.create_gui()
	self.stop_flag = FALSE
	GtkWindow.show_all(self)

    def close(self,*args):
	self.destroy()
	return TRUE
	
    def create_gui(self):
	box1 = GtkVBox(spacing=5)     	
        self.add(box1)
        box1.show()

	self.line_label = GtkLabel()
	box1.pack_start(self.line_label)

	self.it_label = GtkLabel()
	box1.pack_start(self.it_label)
	
	self.data_list = GtkCList(cols=self.nBands+1)
	self.data_list.set_selection_mode(SELECTION_SINGLE)
	self.data_list.set_column_width(0,20)
	for i in range(self.nBands):
	    self.data_list.set_column_width(i+1,60)
	box1.pack_start(self.data_list)
	self.data_list.show()

	self.progress_bar = GtkProgressBar()
	box1.pack_start(self.progress_bar)
	
	self.stop_button = GtkButton("Stop process")
	self.stop_button.connect("clicked",self.stop_cb)
	box1.pack_start(self.stop_button)

    def set_data(self,centres,n_iter):
	self.it_label.set_text("Classes after "+str(n_iter+1)+" iterations") 
	self.data_list.freeze()
	self.data_list.clear()
	for i in range(len(centres)):
	    cur_list = [str(i)]
	    for j in range(self.nBands):
	        #c = str(centres[i][j])
		c = "%7.2f"%centres[i][j]
		cur_list.append(c)
	    self.data_list.append(cur_list)
	
	self.data_list.thaw()

    def stop_cb(self,*args):
	self.stop_flag = TRUE
	self.progress_bar.hide()
	self.stop_button.hide()
	    
    def stop_pressed(self,*args):
	return self.stop_flag
	
    def show_progress(self,percents,line):
	self.line_label.set_text("Current Line Number "+str(line)) 
	self.progress_bar.set_percentage(percents/100.)
	while events_pending():
	    mainiteration(FALSE)

    def finish(self):
	self.line_label.hide()
	self.it_label.set_text("Classification Complete") 
############################################################################
class ISODATADialog(GtkWindow):

    def __init__(self,app=None):
	GtkWindow.__init__(self)
	self.set_title('ISODATA Classification')
	self.set_policy(FALSE, TRUE, TRUE)
	self.text_pos = 0
	self.tooltips = GtkTooltips()
	
        try:
    	    gdal_dataset = gview.app.sel_manager.get_active_layer().get_data().get_dataset()
        except:
	    gvutils.error("Active Layer is not a raster layer")
    	    return None 
	    		
	self.band_list_to_classify = []    		
		   	
	gui_OK = self.create_gui()
	if gui_OK is FALSE:
	    return None
	else:
	    GtkWindow.show_all(self)
	
    def close(self,*args):
	self.destroy()
	return TRUE

######################################################################
    def create_gui(self):

	self.dict_of_bands = get_list_of_bands_as_dict()
	self.list_of_bands = self.dict_of_bands.keys()
	self.list_of_bands.sort()
	
	title_width = 120
	self.metric_num = 0

	box1 = GtkVBox(spacing=5)     	
        self.add(box1)
        box1.show()

	rastersbox = GtkVBox(spacing=5)
	box1.pack_start(rastersbox)
	rastersbox.show()
	
### source list #############################################################	
	frame1 = GtkFrame("Raster Specifications")
	frame1.show()
        rastersbox.pack_start(frame1, expand=FALSE)
	
	box2r = GtkHBox(spacing=10)
        box2r.set_border_width(10)
	frame1.add(box2r)
	box2r.show()
			
	box2r1 = GtkVBox(spacing=5)
	box2r.add(box2r1)
	box2r1.show()
	
	self.src_list = GtkCList(cols=1)
	self.src_list.set_selection_mode(SELECTION_SINGLE)
	self.src_list.set_column_width(0,120)
	self.src_list.connect('button-press-event',self.src_band_selected_cb)
	self.src_list.freeze()
	self.src_list.clear()
	
	for name in self.list_of_bands:
	    self.src_list.append([name])
	self.src_list.thaw()
	box2r1.pack_start(self.src_list)
	self.src_list.show()

	box2r2 = GtkVBox(spacing=5)
	box2r.add(box2r2)
	box2r2.show()

	button_copy = GtkButton(">>")
	box2r2.pack_start(button_copy)
	button_copy.connect("clicked",self.copy_band_cb)
	button_remove = GtkButton("<<")
	box2r2.pack_start(button_remove)
	button_remove.connect("clicked",self.remove_band_cb)

	box2r3 = GtkVBox(spacing=5)
	box2r.add(box2r3)
	box2r3.show()
	
	self.sel_list = GtkCList(cols=1)
	self.sel_list.set_selection_mode(SELECTION_SINGLE)
	self.sel_list.connect('button-press-event',self.sel_band_selected_cb)
	self.sel_list.set_column_width(0,120)
	box2r3.pack_start(self.sel_list)
	self.sel_list.show()

	self.src_row_to_copy   = -1
	self.sel_row_to_delete = -1
	
#### Entries ###########################################################
	entries_table = GtkTable(3,4)
	entries_table.set_border_width(5) 
	box1.pack_start(entries_table)
        
	label = GtkLabel("Desirable Number of Clusters")
	entries_table.attach(label,0,2,0,1)
	self.clusters = GtkEntry()
	self.clusters.set_text("8")
	entries_table.attach(self.clusters,2,3,0,1)
	
	
	label = GtkLabel("Maximal Number of Iterations")
	entries_table.attach(label,0,2,1,2)
	self.maxiter = GtkEntry()
	self.maxiter.set_text("20")
	entries_table.attach(self.maxiter,2,3,1,2)
	
	label = GtkLabel("Minimal Cluster Volume")
	entries_table.attach(label,0,2,2,3)
	self.min_volume = GtkEntry()
	self.min_volume.set_text("1000")
	entries_table.attach(self.min_volume,2,3,2,3)

	label = GtkLabel("Movement Classes Treshold")
	entries_table.attach(label,0,2,3,4)
	self.mov_treshold = GtkEntry()
	self.mov_treshold.set_text("0.1")
	entries_table.attach(self.mov_treshold,2,3,3,4)
#######################################################################
	metric_box = GtkHBox(spacing=10)
	box1.pack_start(metric_box)
	
	metric_list = ["Manhattan Metric","Euclidian Metric","Chebyshev Metric"]
	self.metric_menu = gvutils.GvOptionMenu(metric_list,self.metrics_selected_cb)
	metric_box.pack_start(self.metric_menu)
#### Buttons ###########################################################
	button_box = GtkHBox(spacing = 10)
        button_box.set_border_width(10)
	box1.pack_start(button_box)

	button_ok = GtkButton("Classify")
	button_ok.connect("clicked",self.classify_cb)
	button_box.pack_start(button_ok)
	
	button_cancel = GtkButton("Cancel")
	button_cancel.connect("clicked",self.close)
	button_box.pack_start(button_cancel)
	
        return TRUE
########################################################################
    def metrics_selected_cb(self,*args):
	self.metric_num = self.metric_menu.get_history()
########################################################################
    def src_band_selected_cb(self,widget,event,*args):
	try:
	    row,col = widget.get_selection_info(int(event.x),int(event.y))
	except:
	    return
	self.src_row_to_copy = row
########################################################################
    def sel_band_selected_cb(self,widget,event,*args):
	try:
	    row,col = widget.get_selection_info(int(event.x),int(event.y))
	except:
	    return
	self.sel_row_to_delete = row 
########################################################################	    
    def copy_band_cb(self,*args):
	if self.src_row_to_copy > -1:
	    text = self.src_list.get_text(self.src_row_to_copy,0)	   
    	    self.sel_list.freeze()
	    self.sel_list.append([text])
	    self.sel_list.thaw()
	    self.src_list.remove(self.src_row_to_copy)
	    self.src_row_to_copy = -1
	    self.band_list_to_classify.append(self.get_band(text)) 
########################################################################	
    def remove_band_cb(self,*args):
	if self.sel_row_to_delete > -1:
    	    self.sel_list.freeze()
	    text = self.sel_list.get_text(self.sel_row_to_delete,0)	   
	    self.sel_list.remove(self.sel_row_to_delete)
	    self.sel_list.thaw()	
	    self.src_list.append([text])	   
	    self.sel_row_to_delete = -1
	    self.band_list_to_classify.delete(self.get_band(text))
#########################################################################
    def update_gui(self,*args):
	pass
#########################################################################	
    def get_band(self,name):
	layer = self.dict_of_bands[name][1]
	b_num = self.dict_of_bands[name][2]
	band = layer.get_parent().get_dataset().GetRasterBand(b_num+1)
	return band	    
#########################################################################	
    def classify_cb(self,*args):
	if len(self.band_list_to_classify) < 2:
	    return
	if self.metric_num == 0:
	    distance = L1
	elif self.metric_num == 2:
	    distance = L3
	else: 
	    distance = L2
	nClusters = int(self.clusters.get_text())
	minvol = int(self.min_volume.get_text())
	maxit = int(self.maxiter.get_text())
	movement_treshold = float(self.mov_treshold.get_text())
	nBands = len(self.band_list_to_classify)
	cl_table = ClassesTable(nBands)
	self.hide()

	gview.app.new_view()

	b1_name = self.sel_list.get_text(0,0)
	band_list = self.band_list_to_classify
	b1 = self.get_band(b1_name)
	proto_ds = self.dict_of_bands[b1_name][1].get_parent().get_dataset()
	self.out_buf = zeros((b1.YSize, b1.XSize),UnsignedInt8)


	sb = range(len(band_list))
	cp = zeros(nBands)
	d_means = zeros(nClusters,Float)
	volumes = range(nClusters)
	
	centres = []
	disp = []
	maxVal = 256.
	ymax = b1.YSize / 20
	ys = 20
	max_percent_val = 11 * maxit * b1.YSize / 40
	cur_percent_val = 0
	for i in range(nClusters):
	    centres.append(((ones(nBands,Float)*i)*maxVal)/nClusters)
	    disp.append(zeros(nBands,Float))
	for kit in range(maxit):
	    centres_s = []
	    for i in range(len(centres)):
		volumes[i] = 0
		centres_s.append(zeros(nBands,Float))
	    flag = 0
	    nc = len(centres)
	    if kit >= maxit/2:
	        ymax = b1.YSize
		ys = 1
	    for yc in range(ymax):
		y = yc * ys
		for i in range(nBands):
		    sb[i] = gdalnumeric.BandReadAsArray(band_list[i],0,y,b1.XSize,1)[0]

		rb = self.out_buf[y,0:]
		for x in range(b1.XSize):
		    for i in range(nBands):
			cp[i] = sb[i][x]
		    mind = 1e29
		    for i in range(nc):
			d = distance(centres[i],cp)
			if d < mind:
			    mind = d
			    ic = i
		    if rb[x] != ic:
			rb[x] = ic
			flag = 1
		    centres_s[ic] += cp
		    disp[ic] += cp * cp 
		    volumes[ic] += 1
		    if (distance == L2):
			d_means[ic] += sqrt(mind)
		    else:
			d_means[ic] += mind
		self.out_buf[y, 0:] = rb
		if y%2 == 0:
		    cur_percent_val += 1
		    cl_table.show_progress(100.*cur_percent_val/max_percent_val,y)
	    ##########################################################
	    new_centres = []
	    d_tresh = sum(d_means)/sum(volumes)
	    for i in range(len(centres)):
	        cur_vol = volumes[i]
		if cur_vol > minvol/ys:
		    cur_centre = centres_s[i]/cur_vol
		    disp[i]  = disp[i] / cur_vol - cur_centre * cur_centre
		    disp[i] = sqrt(disp[i])
		    d_means[i] /= cur_vol
		    if len(centres) < nClusters and cur_vol > 2 * minvol/ys and d_means[i] > d_tresh:
			new_centres.append(cur_centre-disp[i])
			new_centres.append(cur_centre+disp[i])
		    else:			    
		    	new_centres.append(cur_centre)
		    
	    ncl = len(new_centres)
	    if ncl > nClusters:
		mind = 1e29
		for i in range(ncl):
		    for j in range(i):
		        d = distance(new_centres[i],new_centres[j])
			if d < mind:
			    mind = d
			    i1 = i
			    i2 = j
		new_centres[i1] += new_centres[i2]
		new_centres[i1] /= 2
		new_centres.remove(new_centres[i2])
				
	    cl_table.set_data(new_centres,kit)
	    
	    if cl_table.stop_pressed():
		if ys > 1:
	    	    ymax = b1.YSize
		    ys = 1
		else:
		    break       #stop_pressed
		
	    if len(centres) == len(new_centres):
		movement_flag = 0
		for i in range(len(centres)):
		    d = distance(centres[i],new_centres[i])
		    d /= d_tresh
		    if d > movement_treshold:
			movement_flag = 1	

		if movement_flag == 0:
		    if ys > 1:
	    		ymax = b1.YSize
			ys = 1
		    else:
			break		# centres movement less then treshold
		
	    centres = new_centres
	    disp = []
	    for i in range(len(centres)):
		disp.append(zeros(nBands,Float))
	    volumes = zeros(len(centres))	
	    d_means = zeros(len(centres))
	    
	    
	    if flag == 0:
		if ys > 1:
	    	    ymax = b1.YSize
		    ys = 1
		else:
		    break       #no changed points

	cl_table.finish()
	res_ds = gdalnumeric.OpenArray(self.out_buf,proto_ds)
	gview.app.open_gdal_dataset(res_ds)
	self.close()
	
TOOL_LIST = ['IsodataTool']

