#!/usr/bin/env python
###############################################################################
# $Id: oe_about.py,v 1.1 2005/08/07 18:22:57 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  Subscript for OpenEV About Box
# Author:   Frank Warmerdam <warmerdam@pobox.com>
#           Gillian Walter <gillian.walter@vexcel.com>
#
###############################################################################
# Copyright (c) 2005, Vexcel Canada Inc. (www.vexcel.com)
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
#  $Log: oe_about.py,v $
#  Revision 1.1  2005/08/07 18:22:57  warmerda
#  New
#
#

import gtk
from gtk import FALSE, TRUE
from GDK import *
import sys
import os
import gview
import gvconst

def ShowAboutBox( viewwindow ):

    window = gtk.GtkWindow()
    window.set_title('About FWTools and OpenEV')
    vbox = gtk.GtkVBox(homogeneous=FALSE,spacing=15)
    window.add(vbox)

    vbox.pack_start(gtk.GtkPixmap(viewwindow,
                                  os.path.join(gview.home_dir,'pics',
                                               'openev.xpm')))
    
    # Contributors
    contrib = gtk.GtkVBox(homogeneous=FALSE,spacing=3)
    contrib.pack_start(gtk.GtkLabel('Contributors:'))
    contrib.pack_start(gtk.GtkLabel('Frank Warmerdam (warmerdam@pobox.com),'))
    contrib.pack_start(gtk.GtkLabel('Gillian Walter (gillian.walter@vexcel.com),'))
    contrib.pack_start(gtk.GtkLabel('Peter Farris-Manning (peter.farris-manning@vexcel.com),'))
    contrib.pack_start(gtk.GtkLabel('Paul Spencer (pagemeba@magma.ca),'))
    contrib.pack_start(gtk.GtkLabel('Steve Rawlinson,'))
    contrib.pack_start(gtk.GtkLabel('Steve Taylor,'))
    contrib.pack_start(gtk.GtkLabel('Paul Lahaie,'))
    contrib.pack_start(gtk.GtkLabel('and others'))
    vbox.pack_start(contrib)

    # Funded By
    funding = gtk.GtkVBox(homogeneous=FALSE,spacing=3)
    funding.pack_start(gtk.GtkLabel('Funding provided by:'))
    funding.pack_start(gtk.GtkPixmap(viewwindow,
                                     os.path.join(gview.home_dir, 'pics', 'vexcel_logo.xpm')))
    funding.pack_start(gtk.GtkLabel('Vexcel Canada Inc.'))
    funding.pack_start(gtk.GtkPixmap(viewwindow,
                                     os.path.join(gview.home_dir,'pics','geo_innovation.xpm')))
    funding.pack_start(gtk.GtkLabel('GeoInnovations'))
    vbox.pack_start(funding)

    # Other Info
    other = gtk.GtkVBox(homogeneous=FALSE,spacing=3)

    FWTOOLS_VERSION = "2.4.7"
    other.pack_start(gtk.GtkLabel('FWTools ' + FWTOOLS_VERSION ))
    other.pack_start(gtk.GtkLabel('http://FWTools.MapTools.org'))
    
    other.pack_start(gtk.GtkLabel('    '))
    
    other.pack_start(gtk.GtkLabel('OpenEV 1.8'))
    other.pack_start(gtk.GtkLabel('http://OpenEV.sourceforge.net'))
    other.pack_start(gtk.GtkLabel('(C) Copyright 2000 Vexcel Canada Inc.  www.vexcel.com'))
    vbox.pack_start(other)
        
    window.show_all()

