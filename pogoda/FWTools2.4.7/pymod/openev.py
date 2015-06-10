#!/usr/bin/env python
###############################################################################
# $Id: openev.py,v 1.46 2005/01/14 17:17:18 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  OpenEV Application Mainline
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
#  $Log: openev.py,v $
#  Revision 1.46  2005/01/14 17:17:18  warmerda
#  pass base config file names, not full path, to new_view()
#
#  Revision 1.45  2003/10/29 14:58:00  gmwalter
#  Force floating point to use "." instead of "," to avoid problems on
#  foreign language windows.
#
#  Revision 1.44  2003/09/09 15:18:46  gmwalter
#  Update openev.py so that if default xml files are not present in xmlconfig
#  directory, old configuration is used.  Get rid of deprecation warnings
#  for python 2.3 by updating clist get_selection_info calls and colour
#  allocation (alloc) calls to use integers instead of floats.
#
#  Revision 1.43  2003/07/28 19:42:34  gmwalter
#  Checked in Diana's xml changes (modified to include tools), added
#  python shell xml configuration.
#
#  Revision 1.42  2002/02/28 18:52:22  gmwalter
#  Added a point-of-interest tool similar to the region-of-interest
#  tool (allows a user to select a temporary point without having to add a
#  new layer).  Added a mechanism to allow some customization of openev
#  via a textfile defining external modules.
#
#  Revision 1.41  2001/11/12 18:42:56  warmerda
#  GViewApp moved to gviewapp.py
#
#  Revision 1.40  2001/10/25 20:30:46  warmerda
#  added interp_mode preference to control default subpixel interp
#
#  Revision 1.39  2001/10/19 16:08:57  warmerda
#  dont put NUMPY:: files in RFL list
#
#  Revision 1.38  2001/10/16 18:52:40  warmerda
#  added active_layer
#
#  Revision 1.37  2001/08/15 13:05:57  warmerda
#  modified default autoscale std_dev to 2.5
#
#  Revision 1.36  2001/08/14 17:03:24  warmerda
#  added standard deviation autoscaling support
#
#  Revision 1.35  2001/06/27 14:32:56  warmerda
#  added subdataset selection support
#
#  Revision 1.34  2001/04/24 14:23:33  warmerda
#  added label tool
#
#  Revision 1.33  2001/04/09 18:33:24  warmerda
#  instantiate a GvSelectionManager
#

import gviewapp
import gview
import gtk
import sys
import os
import getopt

# Force standard c settings for floating point (. rather than ,)
import locale
locale.setlocale(locale.LC_NUMERIC,'C')


if __name__ == '__main__':

    # get command line options and args
    # openev -m menufile -i iconfile -t toolfile image1 image2 ......
    (options, ifiles) = getopt.getopt(sys.argv[1:], 'm:i:t:p:')

    if os.path.isdir(os.path.join(gview.home_dir, 'xmlconfig')):
        mfile = 'DefaultMenuFile.xml'
        if not os.path.isfile(os.path.join(gview.home_dir, 'xmlconfig',mfile)):
            mfile = None

        ifile = 'DefaultIconFile.xml'
        if not os.path.isfile(os.path.join(gview.home_dir, 'xmlconfig',ifile)):
            ifile = None

        pfile = 'DefaultPyshellFile.xml'
        if not os.path.isfile(os.path.join(gview.home_dir, 'xmlconfig',pfile)):
            pfile = None

    else:
        mfile=None
        ifile=None
        pfile=None
        
    tfile = None

    for opt in options[0:]:
        if opt[0] == '-m':
            mfile=opt[1]
        elif opt[0] == '-i':
            ifile=opt[1]
        elif opt[0] == '-p':
            pfile=opt[1]
        elif opt[0] == '-t':
            tfile=opt[1]

    app = gviewapp.GViewApp(toolfile=tfile,menufile=mfile,iconfile=ifile,pyshellfile=pfile)
    gview.app = app
    app.subscribe('quit',gtk.mainquit)
    app.show_layerdlg()
    app.new_view(title=None)
    app.do_auto_imports()

    for item in ifiles:
        app.file_open_by_name(item)

    gtk.mainloop()
