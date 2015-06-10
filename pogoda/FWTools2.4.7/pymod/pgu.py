###############################################################################
# $Id: pgu.py,v 1.1 2000/06/14 15:12:39 warmerda Exp $
#
# Project:  Python Gtk Utility Widgets
# Purpose:  Core PGU stuff, such as registering new PyGtk classes.
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
#  $Log: pgu.py,v $
#  Revision 1.1  2000/06/14 15:12:39  warmerda
#  New
#
#

import gtk; _gtk = gtk; del gtk
from string import *

def gtk_register(name,class_obj):
    _gtk._name2cls[name] = class_obj
    
