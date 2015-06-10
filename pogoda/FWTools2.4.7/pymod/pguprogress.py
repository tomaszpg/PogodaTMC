###############################################################################
# $Id: pguprogress.py,v 1.1 2000/06/27 13:22:20 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  Simplified progress monitor dialog.
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
#  $Log: pguprogress.py,v $
#  Revision 1.1  2000/06/27 13:22:20  warmerda
#  New
#
#
#

from gtk import *

class PGUProgressDialog(GtkDialog):
    def __init__(self, title = 'Progress', cancel = FALSE ):
        GtkDialog.__init__(self)
        self.set_title( title )
        self.min = 0.0
        self.max = 1.0
        self.message = "complete"
        self.cancelled = FALSE

        vbox = GtkVBox(spacing=5)
        vbox.set_border_width(10)
        self.vbox.pack_start(vbox)
        
        label = GtkLabel(" 0% "+self.message)
        label.set_alignment(0, 0.5)
        vbox.pack_start(label, expand=TRUE)
        self.label = label
        
        pbar = GtkProgressBar()
        pbar.set_usize(200, 20)
        vbox.pack_start(pbar)

        if cancel:
            button = GtkButton("cancel")
            self.cancel = button
            button.connect( "clicked", self.CancelCB )
            self.action_area.pack_start(button)

        self.pbar = pbar
        self.show_all()

    def CancelCB( self, *args ):
        self.cancelled = TRUE

    def Reset(self):
        self.cancelled = FALSE

    def SetRange( self, min, max ):
        self.min = min
        self.max = max

    def SetDefaultMessage( self, message ):
        self.message = message
        
    def ProgressCB( self, complete, message, *args ):

        self.complete = self.min + (self.max-self.min) * complete
        if message == "":
            message = self.message
            
        message = str(int(complete*100)) + "% " + message
        self.label.set_text(message)
        
        self.pbar.update( complete )
        while events_pending():
            mainiteration(FALSE)

        if self.cancelled:
            return 0
        else:
            return 1
    

if __name__ == '__main__':
    pdialog = PGUProgressDialog( "Progress Test" )

    mainloop()
        
