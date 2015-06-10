###############################################################################
# $Id: gvconst.py,v 1.12 2003/08/06 17:09:14 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  Declaration of OpenEV constants
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
#  $Log: gvconst.py,v $
#  Revision 1.12  2003/08/06 17:09:14  warmerda
#  Added GLRA values
#
#  Revision 1.11  2002/07/24 14:50:41  warmerda
#  added GVSHAPE_COLLECTION
#
#  Revision 1.10  2001/08/14 17:03:24  warmerda
#  added standard deviation autoscaling support
#
#  Revision 1.9  2000/07/31 21:17:23  srawlin
#  added change_info type constants for GvShapes and GvRaster
#
#  Revision 1.8  2000/07/07 14:56:06  srawlin
#  added default LUT
#
#  Revision 1.7  2000/06/23 12:58:36  warmerda
#  added GvRasterLayer modes
#
#  Revision 1.6  2000/06/14 22:11:35  warmerda
#  Added real/imaginary support to color wheel
#
#  Revision 1.5  2000/06/14 13:17:51  warmerda
#  added RL_LUT_ codes
#
#  Revision 1.4  2000/06/13 22:19:49  srawlin
#  added 3D python bindings
#
#  Revision 1.3  2000/06/09 01:04:14  warmerda
#  added standard headers
#

"""
Constants for use in the GvRasterLayer functions

Constants for texture_mode_set
"""

RL_TEXTURE_REPLACE  = 0
RL_TEXTURE_MODULATE  = 1

"""
Constants for zoom_set

Magnification / Minification
"""

RL_FILTER_BILINEAR  = 0
RL_FILTER_NEAREST   = 1

"""
Minification only -- if we ever use mipmaps this is useful
"""

RL_FILTER_TRILINEAR = 2


"""
Preset modes for blend_mode_set
"""

RL_BLEND_OFF      = 0
RL_BLEND_FILTER   = 1
RL_BLEND_MULTIPLY = 2
RL_BLEND_ADD      = 3
RL_BLEND_CUSTOM   = 4

"""
Constants for custom blend modes
These can go in both the source and destination modes
"""

RL_BLEND_FACT_ZERO          = 0
RL_BLEND_FACT_ONE           = 1
RL_BLEND_FACT_DST_COLOR     = 2
RL_BLEND_FACT_MIN_DST_COLOR = 3
RL_BLEND_FACT_MIN_SRC_COLOR = 4
RL_BLEND_FACT_SRC_ALPHA     = 5
RL_BLEND_FACT_MIN_SRC_ALPHA = 6

"""
Constants for alpha_mode_set
"""

RL_ALPHA_OFF     = 0
RL_ALPHA_NEVER   = 1
RL_ALPHA_ALWAYS  = 2
RL_ALPHA_LESSER  = 3
RL_ALPHA_LEQUAL  = 4
RL_ALPHA_EQUAL   = 5
RL_ALPHA_GEQUAL  = 6
RL_ALPHA_GREATER = 7
RL_ALPHA_NEQUAL  = 8

"""
Constants to set texture wrapping/clamping
"""

RL_TEXCOORD_CLAMP  = 0
RL_TEXCOORD_REPEAT = 1

"""
Constants to describe type of LUT attached to the RasterLayer
"""

RL_LUT_NONE = 0
RL_LUT_1D   = 1
RL_LUT_2D   = 2

"""
Constants for GvRasterLayer.lut_color_wheel_new() mode arguments.
"""

RL_LUT_MAGNITUDE = 0
RL_LUT_PHASE_ANGLE = 1
RL_LUT_SCALAR = 2
RL_LUT_REAL = 3
RL_LUT_IMAGINARY = 4

"""
GvRasterLayer modes
"""

RLM_AUTO = 0
RLM_SINGLE = 1
RLM_RGBA = 2
RLM_COMPLEX = 3


"""
GvShape types.
"""

GVSHAPE_POINT = 1
GVSHAPE_LINE  = 2
GVSHAPE_AREA  = 3
GVSHAPE_COLLECTION = 4


"""
GvRaster and GvShapes change_info types, from gvtypes.h
"""
GV_CHANGE_ADD      = 0x001
GV_CHANGE_REPLACE  = 0x002
GV_CHANGE_DELETE   = 0x003

"""
GvView   2D = Orthonormal Projection
         3D = Perspective
"""
MODE_2D = 0
MODE_3D = 1


"""
Default Rainbow Look Up Table, colour order (red, orange, yellow, green, cyan, blue, purple, red)
"""
STD_LUT = '\377\000\000\377\377\006\000\377\377\014\000\377\377\022\000\377\377\030\000\377\377\036\000\377\377$\000\377\377*\000\377\3770\000\377\3776\000\377\377<\000\377\377B\000\377\377H\000\377\377N\000\377\377T\000\377\377Z\000\377\377`\000\377\377f\000\377\377l\000\377\377r\000\377\377x\000\377\377~\000\377\377\204\000\377\377\212\000\377\377\220\000\377\377\226\000\377\377\234\000\377\377\242\000\377\377\250\000\377\377\256\000\377\377\264\000\377\377\272\000\377\377\300\000\377\377\306\000\377\377\314\000\377\377\322\000\377\377\330\000\377\377\336\000\377\377\344\000\377\377\352\000\377\377\360\000\377\377\366\000\377\377\374\000\377\373\377\000\377\365\377\000\377\357\377\000\377\351\377\000\377\343\377\000\377\335\377\000\377\327\377\000\377\321\377\000\377\313\377\000\377\305\377\000\377\277\377\000\377\271\377\000\377\263\377\000\377\255\377\000\377\247\377\000\377\241\377\000\377\233\377\000\377\225\377\000\377\217\377\000\377\211\377\000\377\203\377\000\377}\377\000\377w\377\000\377q\377\000\377k\377\000\377e\377\000\377_\377\000\377Y\377\000\377S\377\000\377M\377\000\377G\377\000\377A\377\000\377;\377\000\3775\377\000\377/\377\000\377)\377\000\377#\377\000\377\035\377\000\377\027\377\000\377\021\377\000\377\013\377\000\377\005\377\000\377\000\377\000\377\000\377\006\377\000\377\014\377\000\377\022\377\000\377\030\377\000\377\036\377\000\377$\377\000\377*\377\000\3770\377\000\3776\377\000\377<\377\000\377B\377\000\377H\377\000\377N\377\000\377T\377\000\377Z\377\000\377`\377\000\377f\377\000\377l\377\000\377r\377\000\377x\377\000\377~\377\000\377\204\377\000\377\212\377\000\377\220\377\000\377\226\377\000\377\234\377\000\377\242\377\000\377\250\377\000\377\256\377\000\377\264\377\000\377\272\377\000\377\300\377\000\377\306\377\000\377\314\377\000\377\322\377\000\377\330\377\000\377\336\377\000\377\344\377\000\377\352\377\000\377\360\377\000\377\366\377\000\377\374\377\000\373\377\377\000\365\377\377\000\357\377\377\000\351\377\377\000\343\377\377\000\335\377\377\000\327\377\377\000\321\377\377\000\313\377\377\000\305\377\377\000\277\377\377\000\271\377\377\000\263\377\377\000\255\377\377\000\247\377\377\000\241\377\377\000\233\377\377\000\225\377\377\000\217\377\377\000\211\377\377\000\203\377\377\000}\377\377\000w\377\377\000q\377\377\000k\377\377\000e\377\377\000_\377\377\000Y\377\377\000S\377\377\000M\377\377\000G\377\377\000A\377\377\000;\377\377\0005\377\377\000/\377\377\000)\377\377\000#\377\377\000\035\377\377\000\027\377\377\000\021\377\377\000\013\377\377\000\005\377\377\000\000\377\377\006\000\377\377\014\000\377\377\022\000\377\377\030\000\377\377\036\000\377\377$\000\377\377*\000\377\3770\000\377\3776\000\377\377<\000\377\377B\000\377\377H\000\377\377N\000\377\377T\000\377\377Z\000\377\377`\000\377\377f\000\377\377l\000\377\377r\000\377\377x\000\377\377~\000\377\377\204\000\377\377\212\000\377\377\220\000\377\377\226\000\377\377\234\000\377\377\242\000\377\377\250\000\377\377\256\000\377\377\264\000\377\377\272\000\377\377\300\000\377\377\306\000\377\377\314\000\377\377\322\000\377\377\330\000\377\377\336\000\377\377\344\000\377\377\352\000\377\377\360\000\377\377\366\000\377\377\374\000\377\377\377\000\373\377\377\000\365\377\377\000\357\377\377\000\351\377\377\000\343\377\377\000\335\377\377\000\327\377\377\000\321\377\377\000\313\377\377\000\305\377\377\000\277\377\377\000\271\377\377\000\263\377\377\000\255\377\377\000\247\377\377\000\241\377\377\000\233\377\377\000\225\377\377\000\217\377\377\000\211\377\377\000\203\377\377\000}\377\377\000w\377\377\000q\377\377\000k\377\377\000e\377\377\000_\377\377\000Y\377\377\000S\377\377\000M\377\377\000G\377\377\000A\377\377\000;\377\377\0005\377\377\000/\377\377\000)\377\377\000#\377\377\000\035\377\377\000\027\377\377\000\021\377\377\000\013\377\377\000\005\377\377\000\000\377'

"""
GvRaster autoscaling algorithms.
"""

ASAAutomatic = 0
ASAPercentTailTrim = 1
ASAStdDeviation = 2

"""
OGR Feature Style Anchor points for LABELs.
"""

GLRA_LOWER_LEFT               = 1
GLRA_LOWER_CENTER             = 2
GLRA_LOWER_RIGHT              = 3
GLRA_CENTER_LEFT              = 4
GLRA_CENTER_CENTER            = 5
GLRA_CENTER_RIGHT             = 6
GLRA_UPPER_LEFT               = 7
GLRA_UPPER_CENTER             = 8
GLRA_UPPER_RIGHT              = 9
