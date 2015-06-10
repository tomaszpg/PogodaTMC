###############################################################################
# $Id: pgushapesgrid.py,v 1.10 2003/07/27 04:58:44 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  Scrollable text area widget for displaying GvShapes data
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
#  $Log: pgushapesgrid.py,v $
#  Revision 1.10  2003/07/27 04:58:44  warmerda
#  dos2unix
#
#  Revision 1.9  2003/04/14 18:49:39  gmwalter
#  Fix typo.
#
#  Revision 1.8  2003/04/14 18:37:54  gmwalter
#  Updated to include sorting/indexing functions.
#
#  Revision 1.7  2002/09/14 16:17:13  pgs
#  added support for selecting a cell
#
#  Revision 1.6  2002/08/27 19:12:29  pgs
#  added notion of 'selected' shapes
#
#  Revision 1.5  2002/08/19 17:13:13  pgs
#  small fix for NULL values
#
#  Revision 1.4  2002/08/15 18:17:23  pgs
#  fixed  bug in expose when a property is None.
#
#  Revision 1.3  2002/08/13 17:42:32  pgs
#  added a nice frame ;)
#
#  Revision 1.2  2002/08/13 16:08:52  pgs
#  several changes to rendering logic to allow for resetting the adjustments
#  if the column widths change, plus easier calculations of cell spacings for
#  consistency
#
#

"""

"""

import gtk,GDK
import gview
import Numeric
import gvsignaler

class pguShapesGrid( gtk.GtkTable, gvsignaler.Signaler ):
    
    def __init__(self,editable=1):
        
        self._editable=editable
        if self._editable == 1:
            gtk.GtkTable.__init__( self, rows=3, cols=2 )
        else:
            gtk.GtkTable.__init__( self, rows=2, cols=2 )
            
        self.hadj = gtk.GtkAdjustment()
        self.vadj = gtk.GtkAdjustment()
        
        self._hscroll = gtk.GtkHScrollbar( adj = self.hadj )
        self._vscroll = gtk.GtkVScrollbar( adj = self.vadj )
        self._area = gtk.GtkDrawingArea()
        self._pixmap = None
        #this mask also seems to enable scrolling???
        evt_mask = gtk.GDK.BUTTON_PRESS_MASK | gtk.GDK.BUTTON_RELEASE_MASK | \
                   gtk.GDK.KEY_PRESS_MASK | gtk.GDK.KEY_RELEASE_MASK
        self._area.set_events( evt_mask )


        if self._editable == 1:
            self._entry = gtk.GtkEntry()
            self._entry.set_sensitive( gtk.FALSE )
            self._entry.connect( 'changed', self.entry_changed )
        
        #the data source
        self.source = None
        self.source_changed_id = None
        self.subset = []

        # indices/info for sorting (indices maps source index to nRow; inv_indices
        # maps nRow to source index, and similar for subindices).
        self.indices = None
        self.inv_indices = None
        self.subindices = None
        self.inv_subindices = None
        self.sort_reverse=0
        
        #string values to use as titles
        self.titles = [ ]
        
        #fonts for drawing titles and cells put here
        self.title_font = None
        self.cell_font = None
        
        #the overall size of the data set
        self.n_rows = 0
        self.n_cols = 0
        
        #the height of a single row and title row
        self.row_height = 0
        self.title_height = 0
        
        #the row/col to put in the top left corner
        self.start_row = 0
        self.start_col = 0
        
        #the current row/col selected (when we support clicking :)
        self.current_row = 0      # current row in display widget coordinates
        self.current_row_src = -1 # current row in source coordinates (source index)
        self.current_col = 0
        
        self.col_widths = []
               
        #the number of pixels around each cell
        self.cell_half = 4
        self.cell_full = (self.cell_half) * 2 + 1
        
        self.max_width = 0
        self.max_height = 0
        
        #flag to recalculate the adjustments
        self.bCalcAdjustments = gtk.TRUE

        # list of indices of currently selected shapes (NOT the same as the
        # currently editable cell)
        self.selected_shapes=None
        
        #set to true if changing some value that would end up causing multiple
        #expose events or an endless loop even.
        self.updating = gtk.FALSE
        
        frm = gtk.GtkFrame()
        frm.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        frm.add(self._area)

        if self._editable == 1:
            self.attach( self._entry, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.SHRINK )
            self.attach( frm, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL )
            self.attach( self._vscroll, 1, 2, 1, 2, xoptions=gtk.SHRINK)
            self.attach( self._hscroll, 0, 1, 2, 3, yoptions=gtk.SHRINK )
        else:
            self.attach( frm, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL )
            self.attach( self._vscroll, 1, 2, 0, 1, xoptions=gtk.SHRINK)
            self.attach( self._hscroll, 0, 1, 1, 2, yoptions=gtk.SHRINK )
            
        self.show_all()

        # signals: Note that the right-click (button 3) event
        # is a special case used internally to select cells for
        # editing.
        self.publish('clicked-selected-row')
        self.publish('clicked-unselected-row')
        self.publish('title-clicked')
        
        self._area.connect( 'expose-event', self.expose )
        self._area.connect( 'configure-event', self.configure )
        self._area.connect( 'button-press-event', self.click )
        self.hadj.connect( 'value-changed', self.changed )
        self.vadj.connect( 'value-changed', self.changed )
        self.connect( 'style-set', self.expose )
        
    def entry_changed( self, widget ):
        """called when the user has changed the text in an entry
        """
        if self.current_row is not None and self.current_col is not None:
            if self.current_row > 0:
                self.source[self.current_row_src].set_property( \
                    self.titledict[self.titles[self.current_col]], self._entry.get_text() )
                    
        self.expose()
        
    def click( self, widget, event ):
        """the user clicked the widget, select a cell?
        """
        
        # If left button clicked, select/delect a row; if right button
        # clicked, select a column.
        if len(self.col_widths) < 1:
            return
        
        #
        # determine the column that the user clicked in by first offsetting
        # for the current start column (accounts for columns scrolled off the
        # left edge)
        #
        current = 0
        for i in range(self.start_col):
            current = current + self.col_widths[i] + self.cell_full
        
        #
        # now actually look for the right column.  If nCol is None at the end
        # then the user clicked off the right edge.
        #
        nCol = None
        current_temp = 0
        for i in range(self.start_col, len(self.col_widths)):
            current_temp = current_temp + self.col_widths[i] + self.cell_full
            if event.x < current_temp:
                nCol = i
                break
            
        current = current + current_temp
        
        #
        # now determine the row.  If its 0 then they clicked a 'title'.  If it
        # is None then they clicked off the bottom edge.
        # Use the same trick as for the columns to account for ones scrolled
        # off the top, but its trickier because the first row is always the
        # titles.  And its easier because all rows are the same height :)
        #
        nRow = None
        if event.y < (self.row_height + self.cell_full):
            nRow = 0
        else:
            # NOTE: the max(self.start_row-1,0) below is a kludge to
            # avoid an offset problem after scrolling (first scroll
            # click doesn't seem to actually cause the window to scroll,
            # even though vadj updates)
            row = max(self.start_row-1,0) + int(event.y / (self.row_height + self.cell_full))
            if row <= self.n_rows:
                nRow = row
        
        if nRow == 0 and nCol is not None:
            cprop=self.titledict[self.titles[nCol]]
            self.notify('title-clicked',nCol,cprop)

        if (event.button != 3):
            # Notify that a selected or unselected row was clicked,
            # and send event.
            if nRow is not None and nRow > 0:            
                if self.selected_shapes[self.grid2src(nRow)] == 1:
                    self.notify('clicked-selected-row',self.grid2src(nRow),0,event)
                else:
                    self.notify('clicked-unselected-row',self.grid2src(nRow),0,event)
        elif (event.state & GDK.SHIFT_MASK):
            # stop editing
            self.current_row = 0
            self.current_row_src = -1
            self.current_col = 0
            if self._editable == 1:
                self._entry.set_sensitive( gtk.FALSE )
            self.expose()
         
        else:
            self.current_row = nRow
            self.current_row_src = self.grid2src(nRow)
            self.current_col = nCol

            if self._editable == 1:
                if nRow is not None and nCol is not None and nRow > 0:
                    self._entry.set_sensitive( gtk.TRUE )
                    val = self.source[self.grid2src(nRow)].get_property(self.titledict[self.titles[nCol]])
                    self._entry.set_text( val )
                    self._entry.grab_focus()
                else:
                    self._entry.set_text( '' )
                    self._entry.set_sensitive( gtk.FALSE )

            self.expose()           
        
            
    def changed( self, widget ):
        """Track changes to the scrollbars and record the 
        """
        
        self.start_row = int(self.vadj.value)
        self.start_col = int(self.hadj.value)
        self.expose()
        
    def set_subset( self, subset = []):
        """Sets an array of shape indexes that constitute a displayable
        subset of the shapes
        
        subset - list of integer values
        
        If selected is None or an empty list, then all records will be
        displayed.
        """
        if subset is None:
            subset = []
            
        self.subset = subset
        
        self.start_row = 0
        self.start_col = 0
        if len(self.subset) > 0:
            self.n_rows = len(self.subset)
        
        self.bCalcAdjustments = gtk.TRUE
        self.source_sort()
        self.expose()

    def set_source( self, source, titledict=None, hidden=None ):
        """Set the data source
        
        shapes - a GvShapes instance

        titledict - dictionary of titles for properties (optional)

        hidden - properties to hide
        
        reset all the internal parameters
        """       
        self.clear()
        #trap setting to None or an invalid shapes object       
        if source == None or source._o == None or len(source) == 0:
            return

        self.source = source
        self.source_changed_id = self.source.connect( 'changed', self.source_changed_cb )
        self.subset = []

        schema = source.get_schema()
        self.n_cols = len(schema)
        self.n_rows = len(source)

        # no shapes initially selected.
        # Shapes are selected by source index.
        self.selected_shapes=Numeric.zeros([len(source),1])
        # Sorted position of shape- initially in order of location in source.
        # Used to map nRow->source index and vice versa.
        self.indices=Numeric.array(range(len(source)))+1
        self.inv_indices=Numeric.argsort(self.indices)
        self.sort_reverse=0
        self.subindices=None
        self.inv_subindices=None
        
        self.sort_property=None
        
        self.titledict={}
        if titledict is None:
            titledict={}

        self._hidden_titles=[]    
        if hidden is not None:
            for item in hidden:
                self._hidden_titles.append(item)

        for i in range(len(schema)):
            title = schema[i][0]

            if title not in self._hidden_titles:
                if titledict.has_key(title):
                    self.titles.append(titledict[title])
                    self.titledict[titledict[title]]=title
                else:
                    self.titles.append(title)
                    self.titledict[title]=title
                
        #update the scrollbars
        self.bCalcAdjustments = gtk.TRUE
        self.expose()

    def ssrc2grid( self, ss_index ):
        # Convert from source index (0...Nsrc-1 or 0...Nsubset-1)
        # to grid row # (1...Nsrc or 1...Nsubset)
        if ((self.source is None) or (ss_index > len(self.source)-1) or (ss_index < 0)):
            return 0
        
        if len(self.subset) > 0:
            if ss_index > len(self.subset)-1:
                return 0
            grid_row = self.subindices[ss_index] 
        else:
            grid_row = self.indices[ss_index]

        return grid_row

    def src2grid( self, s_index ):
        # Convert from source index
        # to grid row # (1...Nsrc or 1...Nsubset)
        if ((self.source is None) or (s_index > len(self.source)-1) or (s_index < 0)):
            return 0
        
        if len(self.subset) > 0:
            ss_index=None
            for ind in range(len(self.subset)):
                if self.subset[ind] == s_index:
                    ss_index=ind
            if ss_index is None:
                return 0
            
            grid_row = self.subindices[ss_index] 
        else:
            grid_row = self.indices[s_index]

        return grid_row

    def grid2ssrc( self, grid_row ):
        # Convert from grid row (0...Nsrc or 0...Nsubset)
        # to source or subset index # (1...Nsrc-1 or 1...Nsubset-1)
        if ((self.source is None) or (grid_row > len(self.source)) or (grid_row < 1)):
            return -1
        
        if len(self.subset) > 0:
            if grid_row > len(self.subset):
                return -1
            ss_index = self.inv_subindices[grid_row-1] 
        else:
            ss_index = self.inv_indices[grid_row-1]

        return ss_index

    def grid2src( self, grid_row ):
        # Convert from grid row (0...Nsrc or 0...Nsubset)
        # to source index # (1...Nsrc-1)
        if ((self.source is None) or (grid_row > len(self.source)) or (grid_row < 1)):
            return -1
        
        if len(self.subset) > 0:
            if grid_row > len(self.subset):
                return -1
            src_index = self.subset[self.inv_subindices[grid_row-1]] 
        else:
            src_index = self.inv_indices[grid_row-1]

        return src_index

            
    def source_sort( self, sort_property=None,reverse=None ):
        # Need to call expose event after sorting to display
        # inv_indices/inv_subindices map (nRow-1)->source/subset
        # index; indices/subindices map source/subset index->nRow
        if ((self.source is None) or (len(self.source) < 1)):
            return

        # clear editing cell selections
        self.current_row = 0
        self.current_row_src = -1
        
        if sort_property is None:
            # default to last one if sort property not specified
            sort_property=self.sort_property
            
        if reverse is None:
            reverse=self.sort_reverse
          
        if (len(self.subset) == 0):
            self.subindices=None
            self.inv_subindices=None
            if sort_property is None:
                self.sort_property=sort_property
                self.sort_reverse=reverse
                if self.sort_reverse == 0:
                    self.inv_indices=Numeric.array(range(len(self.source)))
                else:
                    self.inv_indices=Numeric.array(range(len(self.source)-1,-1,-1))
                # Grid rows are from 1...N (titles are 0)                    
                self.indices=Numeric.argsort(self.inv_indices)+1
                return
        else:
            # If a subset is defined, the main set shouldn't be
            # used at all in expose.  Don't bother sorting it.
            self.indices=None
            self.inv_indices=None
            if sort_property is None:
                self.sort_property=sort_property
                self.sort_reverse=reverse                
                if self.sort_reverse == 0:
                    self.inv_subindices=Numeric.array(range(len(self.subset)))
                else:
                    self.inv_subindices=Numeric.array(range(len(self.subset)-1,-1,-1))
                self.subindices=Numeric.argsort(self.inv_subindices)+1
                return
            
            
        # Check that requested sort property exists
        have_prop=0
        prop_type='string'
        for cprop in self.source.get_schema():
            if cprop[0] == sort_property:
                have_prop=1
                prop_type=cprop[1]
                
        if have_prop == 1:
            self.sort_property=sort_property
            self.sort_reverse=reverse             
            if (len(self.subset) == 0):
                ind_list=[]
                count=0
                if ((prop_type == 'float') or (prop_type == 'integer')):
                    for cshape in self.source:
                        # convert to float so sorting is numeric
                        ind_list.append((float(cshape.get_property(sort_property)),count))
                        count=count+1
                else:
                    # sort as a string
                    for cshape in self.source:
                        ind_list.append((cshape.get_property(sort_property),count))
                        count=count+1
                        
                ind_list.sort()
                if self.sort_reverse == 1:
                    ind_list.reverse()
                self.inv_indices=Numeric.zeros((count,))
                for c_ind in range(count):
                    self.inv_indices[c_ind]=ind_list[c_ind][1]
                self.indices=Numeric.argsort(self.inv_indices)+1
            else:
                ind_list=[]
                if ((prop_type == 'float') or (prop_type == 'integer')):
                    count = 0
                    for cindex in self.subset:
                        ind_list.append((float(self.source[cindex].get_property(sort_property)),count))
                        count=count+1
                else:
                    count=0
                    for cindex in self.subset:
                        ind_list.append((self.source[cindex].get_property(sort_property),count))
                        count=count+1
                        
                ind_list.sort()
                if self.sort_reverse == 1:
                    ind_list.reverse()                
                self.inv_subindices=Numeric.zeros((len(self.subset),))
                for c_ind in range(len(self.subset)):
                    self.inv_subindices[c_ind]=ind_list[c_ind][1]
                self.subindices=Numeric.argsort(self.inv_subindices)+1
        else:
            print 'Invalid sort property.'
            
    def source_changed_cb( self, *args ):
        # If shapes have been added/deleted, update relevant info:
        if len(self.source) > self.n_rows:
            temp=self.selected_shapes
            self.selected_shapes=Numeric.zeros([len(self.source),1])
            self.selected_shapes[:self.n_rows]=temp
            self.n_rows=len(self.source)
        elif len(self.source) < self.n_rows:
            temp=self.selected_shapes
            self.selected_shapes=Numeric.zeros([len(self.source),1])
            self.selected_shapes[:len(self.source)]=temp
            self.n_rows=len(self.source)
            # Remove deleted shapes from subset:
            if len(self.subset) > 0:
                new_subset=[]
                for item in self.subset:
                    if item < self.n_rows:
                        new_subset.append(item)
                self.subset=new_subset

        # Update schema, if necessary
        new_schema=self.source.get_schema()
        if len(new_schema) != self.n_cols:
            self.n_cols=len(new_schema)
            for i in range(len(new_schema)):
                if new_schema[i][0] not in self._hidden_titles:
                    if not (titledict.has_key(new_schema[i][0])):
                        self.titledict[new_schema[i][0]]=new_schema[i][0]
                        self.titles.append(new_schema[i][0])
            self.schema=new_schema
            
        self.source_sort()
        self.bCalcAdjustments = gtk.TRUE
        self.expose()

    def calc_adjustments( self ):
        """Recalculate the adjustment settings
        """
        if not (self.flags() & gtk.REALIZED) or len(self.col_widths) == 0:
            self.bCalcAdjustments = gtk.TRUE
            return

        self.updating = gtk.TRUE
        #horizontal min/max are 0 and max line length - page size
        hpos = self.hadj.value
        h_min = 0
        win_width = self._area.get_window().width - self.cell_full
        for i in range( len(self.col_widths) - 1, -1, -1):
            win_width = win_width - self.col_widths[i] - self.cell_full
            if win_width < 0:
                break;
                
        if i == 0 and win_width >= 0:
            h_max = 0
        elif i == 0:
            h_max = 1
        else:
            h_max = i + 2
        
        self.hadj.set_all( hpos, h_min, h_max, 1, 1, 1 )
        self.hadj.changed()

        vpos = self.vadj.value
        v_min = 0
        cells_height = self._area.get_window().height - \
                       self.row_height - self.cell_full
        row_height = self.row_height + self.cell_full
        rows = cells_height / row_height
        
        if len(self.subset) == 0:
            v_max = len(self.source)
        else:
            v_max = len(self.subset)
        #v_max = max( 0, v_max - rows ) + 1
        v_max = max( 0, v_max - rows ) + 2 
        
        self.vadj.set_all( vpos, v_min, v_max, 1, 1, 1)
        self.vadj.changed()
        self.bCalcAdjustments = gtk.FALSE
        self.updating = gtk.FALSE

    def select_row(self,row,col=0,expose=1):
        # Row should be in SOURCE INDEX coordinates, NOT
        # grid or subset coordinates.
        # Note: col argument is only there to be consistent with
        # gtk clist- I don't really see why it is needed, since
        # row number should be enough to select a given row.

        if self.selected_shapes is None:
            print 'No shapes to select...'
            return 0
        elif (len(self.selected_shapes) <= row):
            print 'Selected shape index out of range...'
            return 0
        else:
            self.selected_shapes[row]=1
            if expose == 1:
                self.expose()  
            return 1

    def unselect_row(self,row,col=0,expose=1):
        # Row should be in SOURCE INDEX coordinates, NOT
        # grid or subset coordinates.        
        # Note: col argument is only there to be consistent with
        # gtk clist- I don't really see why it is needed, since
        # row number should be enough to select a given row.

        if self.selected_shapes is None:
            print 'No shapes to unselect...'
            return 0
        elif (len(self.selected_shapes) <= row):
            print 'Selected shape index out of range...'
            return 0
        else:        
            self.selected_shapes[row]=0
            if expose == 1:
                self.expose()                  
            return 1
        
    def select_all(self,expose=1):
        if self.selected_shapes is not None:
            self.selected_shapes[:]=1
            if expose == 1:
                self.expose()   
            return 1
        else:
            print 'No shapes to select...'
            return 0
        
    def unselect_all(self,expose=1):
        if self.selected_shapes is not None:
            self.selected_shapes[:]=0
            if expose == 1:
                self.expose()
            return 1
        else:
            print 'No shapes to unselect...'
            return 0

    def get_shape_coords(self,row):
        if ((self.source is not None) and (len(self.source) > row)):
            return self.source[row].get_node()
        else:
            return None
        
    def expose( self, *args ):
        """Draw the widget
        """
        if not (self.flags() & gtk.REALIZED):
            return

        if len(self.col_widths) != len(self.titles):
            self.max_width = self.cell_full
            self.col_widths=[]
            for title in self.titles:
                col_width = self.title_font.width( title )

                self.col_widths.append( col_width )

                self.max_width = self.max_width + col_width + self.cell_full

            self. max_length = self.cell_full + \
                               ( len(self.titles) * ( self.row_height + self.cell_full ) )

        
        #
        # pre-calculate half a cell spacing because we use it a lot
        #
        cell_half = self.cell_half
        cell_full = self.cell_full

        #
        # create a memory pixmap to render into
        #
        win = self._area.get_window()
        width = win.width
        height = win.height
        pix = self._pixmap
        
        #
        # prefetch the style
        #
        style = self.get_style()
        
        #
        # clear the pixmap
        #
        gtk.draw_rectangle( pix, style.white_gc, gtk.TRUE, 
                            0, 0, width, height )
                            
        if self.source == None or self.source._o == None or len(self.source) == 0:
            msg = "NO DATA TO DISPLAY"
            msg_width = self.title_font.width( msg )
            msg_height = self.title_font.height( msg )
            msg_x = (width / 2) - (msg_width / 2)
            msg_y = (height / 2) + (msg_height / 2 )
            gtk.draw_text( pix, self.title_font, 
                           style.fg_gc[gtk.STATE_INSENSITIVE], 
                           msg_x, msg_y, msg )
            self._area.draw_pixmap(style.white_gc, self._pixmap, 
                                   0, 0, 0, 0, 
                                   width, height )
            
            return gtk.FALSE
            
        
        #
        # track changes in column width because of wide columns
        #
        bResetAdj = gtk.FALSE
        
        #
        # calculate the number of rows to draw
        #
        base_height = height
        title_height = self.title_height
        data_height = base_height - title_height
        disp_rows = int(data_height / ( self.row_height + 3 ))
        
        #
        # starting x for the the first column
        #
        x = cell_half 
        
        first_row = self.start_row
        last_row = first_row + disp_rows
        first_col = self.start_col
        last_col = len(self.titles)
        
        #
        # loop through a column at a time
        #
        for i in range( first_col, last_col ):
            #
            # don't bother drawing if we're going to start past the right edge
            #
            if x > width:
                continue
            
            #
            # pre-calculate the column width for this draw
            # and remember the text values to draw
            #
            cells = []
            
            # Info on whether or not shapes are selected (1 if selected)
            cell_is_selected = []

            for j in range( first_row, last_row ):
                idx = self.grid2src(j)
                if idx == -1:
                    continue
                
                txt = self.source[idx].get_property( self.titledict[self.titles[i]] )
                if txt is None:
                    txt = ""

                cell_width = self.cell_font.width( txt )
                cells.append( (txt, cell_width) )
                cell_is_selected.append(self.selected_shapes[idx])
                if cell_width > self.col_widths[i]:
                    bResetAdj = gtk.TRUE
                    self.col_widths[i] = cell_width

            #
            # figure out the size and placement of the title text
            #
            y = self.title_height + cell_half
            title_width = self.title_font.width( self.titles[i] )
            self.col_widths[i] = max( self.col_widths[i], title_width )
            
            #
            # draw the 'button'
            #
            bx = x - cell_half + 1
            by = y - self.title_height - cell_half
            bw = self.col_widths[i] + cell_full - 1
            bh = self.title_height + cell_full
            gtk.draw_rectangle( pix, style.bg_gc[gtk.STATE_NORMAL], 
                                gtk.TRUE, bx, by, bw, bh)
            
            gtk.draw_line( pix, style.bg_gc[gtk.STATE_PRELIGHT],
                           bx, by, bx, by + bh - 1 )
            gtk.draw_line( pix, style.bg_gc[gtk.STATE_PRELIGHT],
                           bx, by, bx + bw, by )
            #
            # draw the title
            #
            tx = x + ( ( self.col_widths[i] - title_width ) / 2 )
            gtk.draw_text( pix, self.title_font, 
                           style.fg_gc[gtk.STATE_NORMAL], 
                           tx, y, self.titles[i] )
            
            #
            # draw the horizontal line below the title
            #            
            ly = y + cell_half + 1
            lx = x + self.col_widths[i] + cell_half - 1
            gtk.draw_line( pix, style.fg_gc[gtk.STATE_INSENSITIVE], 
                           0, ly - 1, lx, ly - 1 ) 

            # Calculate total width of all cells
            sum_col_widths=0.0
            for cwidth in self.col_widths:
                sum_col_widths = sum_col_widths + cwidth + self.cell_full

            #
            # draw the contents of the cells
            #
            for j in range( len(cells) ):                    
                if cell_is_selected[j] == 1 and i == first_col:
                    gtk.draw_rectangle( pix, style.bg_gc[gtk.STATE_PRELIGHT],
                                       gtk.TRUE, 
                                       0, 
                                       y + cell_half, 
                                       sum_col_widths,
                                       self.row_height + cell_full )                    
                elif self.current_row is not None and \
                   self.current_col is not None and \
                   self.current_row != 0 and \
                   self.current_col == i and \
                   j + max(self.start_row-1,0) == self.current_row - 1:  
                   gtk.draw_rectangle( pix, style.bg_gc[gtk.STATE_PRELIGHT],
                                       gtk.TRUE, 
                                       x - cell_half, 
                                       y + cell_half, 
                                       self.col_widths[i] + cell_full,
                                       self.row_height + cell_full )
                y = y + self.row_height + cell_full
                cx = x + self.col_widths[i] - cells[j][1]
                gtk.draw_text(pix, self.cell_font, 
                              style.fg_gc[gtk.STATE_NORMAL], 
                              cx, y, cells[j][0])
                #
                # only draw the line under each row once, when we are drawing
                # the last column
                #
                if x + self.col_widths[i] + cell_full > width or \
                   i == last_col - 1:
                    ly = y + cell_half + 1
                    lx = x + self.col_widths[i] + cell_half - 1
                    gtk.draw_line( pix, style.fg_gc[gtk.STATE_INSENSITIVE], 
                                   0, ly - 1, lx, ly - 1) 
                              
            #
            # where does the line go
            #
            ly = y + cell_half + 1
            lx = x + self.col_widths[i] + cell_half
            
            #
            # special case for first column, start under the title row
            #
            if i == 0:
                gtk.draw_line( pix, style.fg_gc[gtk.STATE_INSENSITIVE], 
                               0, bh , 0, ly - 1 )

            #
            # draw the vertical lines to the right of each column
            #
            gtk.draw_line( pix, style.fg_gc[gtk.STATE_INSENSITIVE], 
                           lx, 1, lx , y + cell_half )
            
            #
            #advance to next column
            #
            x = x + self.col_widths[i] + cell_full
            
        #draw the backing pixmap onto the screen
        self._area.draw_pixmap(style.white_gc, self._pixmap, 0, 0, 0, 0, 
                               width, height )

        if bResetAdj or self.bCalcAdjustments:
            self.calc_adjustments()

        return gtk.FALSE
           
    def configure( self, widget, event, *args ):
        """Track changes in width, height
        """
        #only do this if we have been realized
        if not self.flags() & gtk.REALIZED:
            return
            
        # create a memory pixmap to render into
        a_win = self._area.get_window()
        self._pixmap = gtk.create_pixmap( a_win, event.width, event.height )    
        
        style = self.get_style()

        if self.title_font is None:
            try:
                self.title_font = gtk.load_font( self.title_font_spec )
            except:
                self.title_font = style.font
            self.title_height = self.title_font.ascent

        if self.cell_font is None:
            try:
                self.cell_font = gtk.load_font( self.cell_font_spec )
            except:
                self.cell_font = style.font
            self.row_height = self.cell_font.ascent

        self.bCalcAdjustments=gtk.TRUE
        
    def clear( self, *args ):
        if self.source_changed_id is not None and self.source is not None:
            self.source.disconnect( self.source_changed_id )
        self.source = None
        self.source_changed_id = None
        self.titles = []
        self.titledict={}
        self._hidden_titles=[]
        self.col_widths = []
        self.n_rows = 0
        self.n_cols = 0
        self.start_row = 0
        self.start_col = 0
        self.current_row = 0
        self.current_row_src = -1
        self.current_col = 0
        
        # indices/info for sorting (indices maps source index to nRow; inv_indices
        # maps nRow to source index, and similar for subindices).
        self.indices = None
        self.inv_indices = None
        self.subindices = None
        self.inv_subindices = None
        self.sort_reverse=0
        self.expose()

    def reset_startrow(self, c_row):
        # Check if c_row is visible.  If not,
        # reset start row to c_row in widget
        win = self._area.get_window()
        width = win.width
        height = win.height

        base_height = height
        title_height = self.title_height
        data_height = base_height - title_height
        # The 3 is there to make sure that we don't scroll
        # 1 or 2 off the bottom of the widget: it may make 
        # the jump to the top occur sooner than it has to.
        disp_rows = int(data_height / ( self.row_height + self.cell_full + 3 ))
        first_row = self.start_row
        last_row = first_row + disp_rows

        if ((c_row >= self.start_row) and (c_row <= last_row)):
            return

        # If c_row isn't in current window, scroll
        # so it is the new start row.
        vmax = self.vadj.__getattr__('upper')
        if c_row >= vmax:
            self.vadj.set_value(vmax)
        elif c_row < 1:
            self.vadj.set_value(1)
        else:
            self.vadj.set_value(c_row)

        self.vadj.value_changed()
        
        
class TestGrid( gtk.GtkWindow ):

    def __init__(self):
        gtk.GtkWindow.__init__( self )
        self.set_title("Test ShapesGrid")
        
        vbox = gtk.GtkVBox()
        self.grid = pguShapesGrid()
        self.grid.set_usize( 300, 300 )
        self.entry = gtk.GtkEntry()
        self.button = gtk.GtkButton( "set shapes file" )
        self.button.connect( "clicked", self.set_shapes )
        
        vbox.pack_start( self.grid )
        vbox.pack_start( self.entry, expand=gtk.FALSE )
        vbox.pack_start( self.button, expand=gtk.FALSE )
        self.add(vbox)
        self.show_all()
        
    def set_shapes( self, widget=None, src = None ):
        if src is None:
            src = self.entry.get_text()
        else:
            self.entry.set_text( src )
            
            
        shapes = gview.GvShapes( shapefilename = src )
        if shapes is not None and shapes._o is not None:
            self.grid.set_source( shapes )
        
        
if __name__ == "__main__":
    win = TestGrid()
    win.set_shapes( src = "c:\\projects\\dmsolutions\\ciet\\ciet_data\\wcsite.shp" )
    win.connect( 'delete-event', gtk.mainquit )
    gtk.mainloop()
    
