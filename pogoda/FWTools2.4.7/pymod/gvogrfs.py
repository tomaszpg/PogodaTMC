#!/usr/bin/env python
###############################################################################
# $Id: gvogrfs.py,v 1.7 2003/05/08 16:19:39 pgs Exp $
#
# Project:  OpenEV
# Purpose:  Classes for building, and parsing OGR Feature Style Specifications
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
# Copyright (c) 2001, Frank Warmerdam <warmerdam@pobox.com>
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
#  $Log: gvogrfs.py,v $
#  Revision 1.7  2003/05/08 16:19:39  pgs
#  made params safe if value missing
#
#  Revision 1.6  2001/04/29 16:27:33  pgs
#  added has_part() to OGRFeatureStyle class
#
#  Revision 1.5  2001/04/23 21:21:28  warmerda
#  added OGRFeatureStyleParam.set() and OGRFeatureStyleParm.set_parm
#
#  Revision 1.4  2001/04/19 22:07:53  warmerda
#  avoid use of +=
#
#  Revision 1.3  2001/04/16 13:50:35  warmerda
#  Paul added OGRFeatureStyle class
#
#  Revision 1.2  2001/04/09 18:37:46  warmerda
#  improved color handling
#
#  Revision 1.1  2001/03/21 22:40:33  warmerda
#  New
#
#

import gview
import string

def gv_to_ogr_color( rgba ):
    if len(rgba) == 3:
        rgba = (rgba[0], rgba[1], rgba[2], 1.0)

    red = min(255,max(0,int(rgba[0] * 255 + 0.5)))
    green = min(255,max(0,int(rgba[1] * 255 + 0.5)))
    blue = min(255,max(0,int(rgba[2] * 255 + 0.5)))
    alpha = min(255,max(0,int(rgba[3] * 255 + 0.5)))

    color = '#%02X%02X%02X' % (red, green, blue)
    if alpha != 255:
        color = color + '%02X' % alpha

    return color

def ogr_to_gv_color( ogr_color ):
    if len(ogr_color) == 9:
        return (int(ogr_color[1:3],16) / 255.0,
                int(ogr_color[3:5],16) / 255.0,
                int(ogr_color[5:7],16) / 255.0,
                int(ogr_color[7:9],16) / 255.0)
    elif len(ogr_color) == 7:
        return (int(ogr_color[1:3],16) / 255.0,
                int(ogr_color[3:5],16) / 255.0,
                int(ogr_color[5:7],16) / 255.0,
                1.0)
    else:
        return (0,0,0,1.0)

class OGRFeatureStyleParam:

    def __init__(self, parm=None):
        if parm is not None:
            self.parse(parm)

    def set(self, name, value, role='string_value', units=''):
        self.param_name = name
        self.units = units
        self.value = value
        self.role = role

    def parse(self, parm):
        (key,value) = string.split(parm,':',1)
        self.param_name = key
        
        #trap params that have no value
        if len(value) == 0:
            self.role='numeric_value'
            self.value = ''
            self.units = ''
            return

        # Handle units
        self.units = ''
        if value[-2:] in ['px','pt','mm','cm','in']:
            self.units = value[-2:]
            value = value[:-2]
        elif value[-1:] == 'g':
            self.units = value[-1:]
            value = value[:-1]

        if value[0] == '"':
            if value[-1:] != '"':
                raise ValueError, 'unterminated literal - ' + parm

            self.role = 'string_value'
            self.value = value[1:-1]

        elif value[0] == '{':
            if value[-1:] != '}':
                raise ValueError, 'unterminated fieldname - ' + parm

            self.role = 'field_name'
            self.value = value[1:-1]

        else:
            self.role = 'numeric_value'
            self.value = value

    def unparse(self):
        result = self.param_name + ':'
        if self.role == 'numeric_value':
            result = result + self.value
        elif self.role == 'field_name':
            result = result + '{'+self.value+'}'
        else:
            result = result + '"'+self.value+'"'

        result = result + self.units

        return result

    def __str__(self):
        result = '  parm=%s  role=%12s  value=%-20s' \
                 % (self.param_name, self.role, self.value)
        if len(self.units) > 0:
            result = result + ' units:'+self.units

        return result

class OGRFeatureStylePart:
    def __init__(self):
        pass

    def parse(self, style_part):

        style_part = string.strip(style_part)
        i = string.find(style_part, '(')
        if i == -1:
            raise ValueError, 'no args to tool name - ' + style_part

        self.tool_name = string.upper(style_part[:i])
        if self.tool_name not in [ 'PEN', 'BRUSH', 'SYMBOL', 'LABEL' ]:
            raise ValueError, 'unrecognised tool name - ' + style_part

        if style_part[-1:] != ')':
            raise ValueError, 'missing end bracket - ' + style_part

        tool_parms = style_part[i+1:-1]

        parms_list = []
        i = 0
        last_i = 0
        in_literal = 0
        while i < len(tool_parms):

            if tool_parms[i] == '"':
                if not in_literal or i == 0 or tool_parms[i-1] != '\\':
                    in_literal = not in_literal

            if not in_literal and tool_parms[i] == ',':
                parms_list.append( string.strip(tool_parms[last_i:i]) )
                i = i + 1
                last_i = i

            i = i + 1

        if in_literal:
            raise ValueError, 'unterminated string literal - ' + style_part

        parms_list.append(string.strip(tool_parms[last_i:]))
        self.parms = {}
        for parm_literal in parms_list:
            parm = OGRFeatureStyleParam(parm_literal)
            self.parms[parm.param_name] = parm

    def unparse(self):
        result = self.tool_name + '('
        first = 1
        for key in self.parms.keys():
            if first:
                first = 0
            else:
                result = result + ','

            result = result + self.parms[key].unparse()
        result = result + ')'

        return result

    def set_parm(self, parm_obj ):
        self.parms[parm_obj.param_name] = parm_obj

    def get_parm(self, parm_name, default_value=None):
        if self.parms.has_key(parm_name):
            return self.parms[parm_name].value
        else:
            return default_value

    def get_color(self, default_value=None):
        color = self.get_parm('c', None)
        if color is None or color[0] != '#':
            return default_value
        else:
            return ogr_to_gv_color( color )

    def __str__(self):
        result = 'Tool:%s\n' % self.tool_name
        for key in self.parms.keys():
            parm = self.parms[key]
            result = result + '  %s\n' % str(parm)

        return result

class OGRFeatureStyle:
    """
    Encapulation of an OGR Feature Style

    This object keeps one tool of each type in a dictionary and allows parsing
    and unparsing of the ogrfs property that would be stored on a vector
    layer.  The semi-colon separator is used for parts. 
    """
    def __init__(self, style=None):
        self.parts = {}

        if style is not None:
            self.parse(style)

    def parse(self, style):
        """
        parse a style into style parts by breaking it apart at any
        ';' not within '"'
        """
        #TODO: check to see if it is of type string 
        #      or can be turned into a string as well
        if style is None:
            return
            
        style = string.strip(style)
        if style == '':
            print 'empty style'
            return
        in_quote = 0
        part_start = 0
        for i in range(len(style)):
            char = style[i:i+1]
            if char == chr(34):
                in_quote = not in_quote
            if not in_quote and char == ";":
                part = style[part_start:i]
                self.parse_part(part)
                part_start = i + 1
        #check for the last one ...
        if part_start != 0 or len(self.parts) == 0:
            part = style[part_start:]
            self.parse_part(part)

    def parse_part(self, part):
        """
        parse a single part
        """
        ogr_part = OGRFeatureStylePart()
        try:
            ogr_part.parse(part)
            self.add_part(ogr_part)
        except:
            print 'Invalid part in feature sytle definition'

    def unparse(self):
        """
        compose the feature style into a string
        """
        result = ''
        sep = ''
        for key in self.parts.keys():
            part = self.parts[key]
            result = result + sep + part.unparse()
            sep = ";"
        return result

    def add_part(self, ogr_part):
        """
        add an OGRFeatureStylePart
        """
        if issubclass(ogr_part.__class__, OGRFeatureStylePart):
            self.parts[ogr_part.tool_name] = ogr_part
        else:
            raise TypeError, 'ogr_part must be an OGRFeatureStylePart'

    def get_part(self, part_name, default = None):
        if self.parts.has_key(part_name):
            return self.parts[part_name]
        else:
            return default

    def remove_part(self, part_name):
        if self.parts.has_key(part_name):
            del self.parts[part_name]
            
    def has_part(self, part_name):
        return self.parts.has_key(part_name)

    def __str__(self):
        result = 'Feature Style Definition:\n'
        for key in self.parts.keys():
            part = self.parts[key]
            result = result + '  %s\n' % str(part)

        return result


if __name__ == '__main__':

    fsp = OGRFeatureStylePart()

    while 1:
        line = raw_input('OGR FS:')
        if len(line) == 0:
            sys.exit(0)

        fsp.parse( line )
        print fsp
        print fsp.unparse()


