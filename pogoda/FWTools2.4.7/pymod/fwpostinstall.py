###############################################################################
#
# Project:  FWTools
# Purpose:  FWTools Postinstall actions.
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
# Copyright (c) 2005, Frank Warmerdam, warmerdam@pobox.com
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
#  $Log: gvalg.py,v $
#

import sys
import os
import string

# ============================================================================
# FileSubstitute()
# ============================================================================
def FileSubstitute( filename, src_pattern, dst_pattern ):
	fulltext = open( filename ).read()
	fulltext = string.replace( fulltext, src_pattern, dst_pattern )
	open( filename, 'w').write( fulltext )


# ============================================================================
# Mainline 
# ============================================================================

if len(sys.argv) < 2:
	FWTOOLS_DIR = os.environ['FWTOOLS_DIR']
else:
	FWTOOLS_DIR = sys.argv[1]

# ----------------------------------------------------------------------------
# Replace location of GDAL DLL in GDALCore.base
# ----------------------------------------------------------------------------
gdalcore = FWTOOLS_DIR + r'\vb6\GDALCore.bas'
gdaldll = FWTOOLS_DIR + r'\bin\gdal_fw.dll'

FileSubstitute( gdalcore, 'gdal12.dll', gdaldll )

