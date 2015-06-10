###############################################################################
# $Id: vrtutils.py,v 1.17 2005/07/07 21:36:06 gmwalter Exp $
#
# Project:  OpenEV
# Purpose:  Utilities for creating vrt files.
# Author:   Gillian Walter, gwalter@atlsci.com
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
#  $Log: vrtutils.py,v $
#  Revision 1.17  2005/07/07 21:36:06  gmwalter
#  Use string to join lines- faster.
#
#  Revision 1.16  2005/01/12 20:00:13  gmwalter
#  Add option to serialize default geotransform.
#
#  Revision 1.15  2005/01/04 17:17:20  gmwalter
#  Add option to adjust geocoding for SrcRect != DstRect
#  added to serializeGCPs, serializeGeoTransform.
#
#  Revision 1.14  2004/11/25 20:53:18  gmwalter
#  Avoid core dump when default geotransform set.
#
#  Revision 1.13  2004/10/28 18:32:33  gmwalter
#  Add band descriptions, minor fixes.
#
#  Revision 1.12  2004/10/15 20:45:23  gmwalter
#  Fix typo.
#
#  Revision 1.11  2004/10/15 17:12:28  gmwalter
#  Added a function.
#
#  Revision 1.10  2004/08/20 15:57:17  gmwalter
#  Various fixes to export tool, added
#  raw band creation to vrt utilities.
#
#  Revision 1.9  2004/07/07 23:13:21  gmwalter
#  Update default geotransform->gcp grid to have
#  16 control points instead of 4.
#
#  Revision 1.8  2003/09/15 19:11:09  gmwalter
#  Bug fix.
#
#  Revision 1.7  2003/09/15 18:53:19  gmwalter
#  Added some functionality for combining bands from different files,
#  reprojecting geocoding information.
#
#  Revision 1.6  2003/04/09 14:46:13  gmwalter
#  Fixed typo in datatype setting.
#
#  Revision 1.5  2003/02/26 22:53:15  gmwalter
#  Add geocoding information preference.
#
#  Revision 1.4  2003/01/28 14:31:39  warmerda
#  added log
#
#
import gdal       
import Numeric
import osr
import os
import string

class VRTCreationOptions:
    def __init__(self,num_dstbands):
        # num_dstbands: number of bands in destination vrt
        self.band_opts={}
        self.geocode_preference=None
        self.reproj=None
        
        for cband in range(1,num_dstbands+1):
            self.band_opts[str(cband)]={}
            self.band_opts[str(cband)]['band']=str(cband)
            self.band_opts[str(cband)]['SourceBand']=str(cband)
            
    def set_geopref(self,geocode_pref=None):
        # Set the geocode preference
        # (None or 'geotransform' or 'gcps')
        if geocode_pref is None:
            self.geocode_preference=None            
        elif geocode_pref == 'geotransform':
            self.geocode_preference='geotransform'
        elif geocode_pref == 'gcps':
            self.geocode_preference = 'gcps'
        else:
            txt="Invalid geocoding preference- options are None,"
            txt=txt+"'geotransform',or 'gcp'.  Resetting to None." 
            print txt
            self.geocode_preference = None

    def get_geopref(self):
        return self.geocode_preference

    def set_reproj(self,proj):
        """ Reproject gcps or geotransform to projection proj (a WKT string)
            during serialization.
        """
        self.reproj=proj
        
    def set_src_window(self,src_tuple,band_list=None):
        if band_list is None:
            # Window all bands
            for ckey in self.band_opts.keys():
                self.band_opts[ckey]['SrcRect']=src_tuple
        else:
            for cband in band_list:
                self.band_opts[str(cband)]['SrcRect']=src_tuple
            
    def set_dst_window(self,dst_tuple,band_list=None):
        if band_list is None:
            # Window all bands
            for ckey in self.band_opts.keys():
                self.band_opts[ckey]['DstRect']=dst_tuple
        else:
            for cband in band_list:
                self.band_opts[str(cband)]['DstRect']=dst_tuple

    def set_datatype(self,data_type,band_list=None):
        if band_list is None:
            # Set datatype in all bands
            for ckey in self.band_opts.keys():
                self.band_opts[ckey]['DataType']=gdal.GetDataTypeName(data_type)
        else:
            for cband in band_list:
                self.band_opts[str(cband)]['DataType']=gdal.GetDataTypeName(data_type)

    def set_color_interp(self,color_interp,band_list=None):
        if band_list is None:
            # Window all bands
            for ckey in self.band_opts.keys():
                self.band_opts[ckey]['ColorInterp']=color_interp
        else:
            for cband in band_list:
                self.band_opts[str(cband)]['ColorInterp']=color_interp
        

    def set_scaling(self,scale_tuple,band_list=None):
        srcmin=scale_tuple[0]
        srcmax=scale_tuple[1]
        dstmin=scale_tuple[2]
        dstmax=scale_tuple[3]
        srcdiff=float(srcmax-srcmin)
        dstdiff=float(dstmax-dstmin)
        if abs(srcdiff) > 0.0:
            ratio=dstdiff/srcdiff
        else:
            print 'Warning- no dynamic range for source. Ratio defaulting to 1.'
            ratio=1.0

        offset=dstmin-(srcmin*ratio)    
        if band_list is None:
            # Window all bands
            for ckey in self.band_opts.keys():
                self.band_opts[ckey]['ScaleRatio']=ratio                
                self.band_opts[ckey]['ScaleOffset']=offset
        else:
            for cband in band_list:
                self.band_opts[str(cband)]['ScaleRatio']=ratio                
                self.band_opts[str(cband)]['ScaleOffset']=offset
        

    def get_opts(self):
        return self.band_opts

def serializeMetadata(indataset=None, dict=None):
    """ Serialize metadata.
    
        Inputs:
        
            indataset- gdal dataset to extract metadata from
                       (None if not using)
                       
            dict- dictionary to use for metadata (None
                  if not using)

        Values in dict will override values in indataset.
    """
    
    if indataset is not None:
        metadict=indataset.GetMetadata()
        if dict is not None:
            for item in dict.keys():
                metadict[item] = dict[item]
    else:
        metadict=dict
        
    if len (metadict) > 0:
        metabase=[gdal.CXT_Element,'Metadata']
        for ckey in metadict.keys():
            mdibase=[gdal.CXT_Element,'MDI']
            mdibase.append([gdal.CXT_Attribute,'key',[gdal.CXT_Text,ckey]])
            mdibase.append([gdal.CXT_Text,metadict[ckey]])
            metabase.append(mdibase)
    else:
        metabase=None
        
    return metabase


def serializeGCPs(indataset=None, vrt_options=None,with_Z=0,gcplist=None,
                  projection_attr_txt=None,reproj=None,srcrect=None,
                  dstrect=None):
    """ This function can be used to serialize gcps with or
        without an associated gdal dataset.

        Inputs:
            indataset- a gdal dataset
            vrt_options- a VRTCreationOptions object
            with_Z- flag to indicate whether Z values should be included
            gcplist- a gcplist or None.  If it is None, indataset
                     will be searched.
            projection_attr_text- projection of the gcps.  If it is
                      None, indataset will be searched.
            reproj- projection of output gcps.  Only used if vrt_options
                    is None (otherwise it looks in vrt_options for reproj).
            srcrect, dstrect- source and destination rectangles to use to
                              adjust gcps (optional- default to None).
                              Only used if vrt_options is None (otherwise
                              function looks at the vrt options for the first
                              band and checks that for SrcRect, DstRect).
                              GCPs are updated so that the new pixel and
                              line values of each gcp correspond to the
                              destination rectangle as opposed to the source
                              rectangle.

        Examples:
            serializeGCPs(dataset,vrtopts)
            serializeGCPs(gcplist=gcps,projection_attr_txt='GEOGCS...',
                          reproj='PROJCS...')
    """
            
    if gcplist is None:
        gcplist=indataset.GetGCPs()

    if projection_attr_txt is None:
        projection_attr_txt=indataset.GetGCPProjection()
        
    srtrans=None
    if vrt_options is not None:
        reproj=vrt_options.reproj
        if reproj == projection_attr_txt:
            reproj=None
        
    if (reproj is not None):
        sr1=osr.SpatialReference()
        sr2=osr.SpatialReference()
        try:
            sr1.ImportFromWkt(reproj)
            try:
                sr2.ImportFromWkt(projection_attr_txt)
                srtrans=osr.CoordinateTransformation(sr2,sr1)
            except:
                srtrans=None
                print 'Warning: unable to reproject gcps- invalid source projection string'
        except:
            srtrans=None
            print 'Warning: unable to reproject gcps- invalid destination projection string'
            
    if len(gcplist) > 0:
        gcpbase=[gdal.CXT_Element,'GCPList']
        if (srtrans is not None):
            gcpbase.append([gdal.CXT_Attribute,'Projection',
                            [gdal.CXT_Text,reproj]])
        else:
            gcpbase.append([gdal.CXT_Attribute,'Projection',
                            [gdal.CXT_Text,projection_attr_txt]])
        if (vrt_options is None) and ((srcrect is None) or (dstrect is None)):
            for gcp in gcplist:
                if srtrans is not None:
                    ngcp=srtrans.TransformPoint(gcp.GCPX,gcp.GCPY,gcp.GCPZ)
                    gcp.GCPX=ngcp[0]
                    gcp.GCPY=ngcp[1]
                    gcp.GCPZ=ngcp[2]
                gcpbase.append(gcp.serialize(with_Z))    
        else:
            if vrt_options is not None:
                bopts=vrt_options.get_opts()[vrt_options.get_opts().keys()[0]]
                if((bopts.has_key('SrcRect')) and
                   (bopts.has_key('DstRect'))):
                    srcrect = bopts['SrcRect']
                    dstrect = bopts['DstRect']
                else:
                    srcrect = None
                    dstrect = None
                    
            if (srcrect is None) or (dstrect is None):
                for gcp in gcplist:
                    if srtrans is not None:
                        ngcp=srtrans.TransformPoint(gcp.GCPX,gcp.GCPY,gcp.GCPZ)
                        gcp.GCPX=ngcp[0]
                        gcp.GCPY=ngcp[1]
                        gcp.GCPZ=ngcp[2]
                    gcpbase.append(gcp.serialize(with_Z))    
            else:
                (spix,sline,xsize,ysize)=srcrect
                (dpix,dline,dxsize,dysize)=dstrect
                for gcp in gcplist:
                    gcpbase2=[gdal.CXT_Element,'GCP']
                    if srtrans is not None:
                        ngcp=srtrans.TransformPoint(gcp.GCPX,gcp.GCPY,gcp.GCPZ)
                        gx=ngcp[0]
                        gy=ngcp[1]
                        gz=ngcp[2]
                    else:
                        gx=gcp.GCPX
                        gy=gcp.GCPY
                        gz=gcp.GCPZ
                    gp=(gcp.GCPPixel+dpix-spix)*dxsize/xsize
                    gl=(gcp.GCPLine+dline-sline)*dysize/ysize
                    gcpbase2.append([gdal.CXT_Attribute,'Id',
                                     [gdal.CXT_Text,gcp.Id]])
                    pixval = '%0.15E' % gp       
                    lineval = '%0.15E' % gl
                    xval = '%0.15E' % gx
                    yval = '%0.15E' % gy
                    zval = '%0.15E' % gz
                    gcpbase2.append([gdal.CXT_Attribute,'Pixel',
                                     [gdal.CXT_Text,pixval]])
                    gcpbase2.append([gdal.CXT_Attribute,'Line',
                                     [gdal.CXT_Text,lineval]])
                    gcpbase2.append([gdal.CXT_Attribute,'X',
                                     [gdal.CXT_Text,xval]])
                    gcpbase2.append([gdal.CXT_Attribute,'Y',
                                     [gdal.CXT_Text,yval]])
                    if with_Z:
                        gcpbase2.append([gdal.CXT_Attribute,'Z',
                                         [gdal.CXT_Text,yval]])
                    gcpbase.append(gcpbase2)
    else:
        gcpbase=None
        
    return gcpbase


def GeoTransformToGCPs(gt,num_pixels,num_lines,grid=2):
    """ Form a gcp list from a geotransform. If grid=0, just use 4
        corners.  If grid=1, split each dimension once.  If grid=2,
        split twice, etc:

        grid=0             grid=1                grid=2

        *           *      *     *     *         *   *   *   *
        
                                                 *   *   *   *    
                           *     *     *
                                                 *   *   *   *
                                               
        *           *      *     *     *         *   *   *   *

        This function is meant to be used to convert a geotransform
        to gcp's so that the geocoded information can be reprojected.

        Inputs: gt- geotransform to convert to gcps
                num_pixels- number of pixels in the dataset
                num_lines- number of lines in the dataset
                grid- see above.  Defaults to 2.
        
    """
    
    gcp_list=[]

    parr=Numeric.arange(0.0,num_pixels+1.0,num_pixels/(grid+1.0))
    larr=Numeric.arange(0.0,num_lines+1.0,num_lines/(grid+1.0))

    for idx in range(len(parr)*len(larr)):
        cgcp=gdal.GCP()
        pix=parr[idx % len(parr)]
        line=larr[idx/len(larr)]
        cgcp.Id=str(idx)
        cgcp.GCPX=gt[0]+(pix*gt[1])+(line*gt[2])
        cgcp.GCPY=gt[3]+(pix*gt[4])+(line*gt[5])
        cgcp.GCPZ=0.0
        cgcp.GCPPixel=pix
        cgcp.GCPLine=line
        
        gcp_list.append(cgcp)

    return gcp_list

def serializeGeoTransform(indataset=None,vrt_options=None,geotransform=None,
                          srcrect=None,dstrect=None,force_geo=0):
    """
        Returns a serialized geotransform, or None if the input
        geotransform is the default (0.0,1.0,0.0,0.0,0.0,1.0).

        Inputs:

        indataset- an input GDAL dataset to get the geotranform
                   from if the geotransform input isn't specified.
                   
        vrtoptions- options for indataset, specifying source and
                    destination rectangles (optional)
                    
        geotransform- a geotransform (6-valued tuple).  Overrides
                      the geotransform in indataset, if present.
    
        srcrect, dstrect-  arguments used to shift
        and scale the transform in case of cropping or resolution
        changes.  The srcrect and dstrect arguments must both be
        tuples of the form (xstart,ystart,xsize,ysize).  If only
        one is specified, it will be ignored. srcrect and dstrect
        are IGNORED if vrt_options is not None.

        force_geo- Set to 1 to force the geotransform to be serialized
                   even if the input geotransform is just the
                   default.  Is 0 (off) by default.
    """
    if geotransform is None:
        gt=indataset.GetGeoTransform()
    else:
        gt=geotransform
        
    default_geo=(0.0,1.0,0.0,0.0,0.0,1.0)
    # Don't add anything if the transform
    # is the default values, unless force_geo
    # is set to 1.
    usegeo=force_geo
    gbase=None

    for i in range(6):
        if gt[i] != default_geo[i]:
            usegeo=1

    if usegeo==1:
        if (vrt_options is None) and ((srcrect is None) or (dstrect is None)):
            geo_text='  %0.22E, %0.22E, %0.22E, %0.22E, %0.22E, %0.22E' % (gt[0], gt[1], gt[2], gt[3], gt[4], gt[5])
        else:
            if vrt_options is not None:
                bopts=vrt_options.get_opts()[vrt_options.get_opts().keys()[0]]
                if ((bopts.has_key('SrcRect')) and
                    (bopts.has_key('DstRect'))):
                    srcrect = bopts['SrcRect']
                    dstrect = bopts['DstRect']
                else:
                    srcrect=None
                    dstrect=None
            if (srcrect is None) or (dstrect is None):
                geo_text='  %0.22E, %0.22E, %0.22E, %0.22E, %0.22E, %0.22E' % (gt[0], gt[1], gt[2], gt[3], gt[4], gt[5])
            else:    
                # Geotransform should be updated to reflect the window
                # All the bands should have the same windowing/overview options,
                # so just look at first one
                
                (spix,sline,xsize,ysize)=srcrect
                (dpix,dline,dxsize,dysize)=dstrect
                gt0=gt[0]+gt[1]*(spix-dpix)+gt[2]*(sline-dline)
                gt3=gt[3]+gt[4]*(spix-dpix)+gt[5]*(sline-dline)
                # floor- if xsize/ysize/dxsize/dysize are non-integer,
                # gdal will truncate, so account for that here.
                gt1=float(gt[1])*Numeric.floor(xsize)/Numeric.floor(dxsize)
                gt2=float(gt[2])*Numeric.floor(ysize)/Numeric.floor(dysize)
                gt4=float(gt[4])*Numeric.floor(xsize)/Numeric.floor(dxsize)
                gt5=float(gt[5])*Numeric.floor(ysize)/Numeric.floor(dysize)
                geo_text='  %0.22E, %0.22E, %0.22E, %0.22E, %0.22E, %0.22E' % (gt0, gt1, gt2, gt3, gt4, gt5)
  
        gbase=[gdal.CXT_Element,'GeoTransform',[gdal.CXT_Text,geo_text]]
    else:
        gbase=None

    return gbase

def serializeCombinedDatasets(indatasetlist,vrt_options_list=None,
                              band_lists=None):
    """ Combines bands from several datasets into one.  Uses
        metadata and georeferencing from the FIRST one,
        and determines raster size from first one.
        indatasetlist- a list of gdal datasets
        vrt_options_list- a single vrt_options instance applicable
                          to all the datasets, or else a list
                          of vrt_options (same length as
                          indatasetlist).
        band_lists- list of lists of bands, or None (use all bands).
    """
    
    if vrt_options_list is None:
        band_opts=[]
        for ds in indatasetlist:
            band_opts.append({})
    else:
        band_opts=[]
        if type(vrt_options_list) == type(list):
            if len(vrt_options_list) != len(indatasetlist):
                raise 'VRT option list length does not match dataset list '+\
                      'length!'
            for opts in vrt_options_list:
                band_opts.append(opts.get_opts())
        else:
            for ds in indatasetlist:
                band_opts.append(vrt_options_list.get_opts())
        
    # band opts: A dictionary of band option dictionaries,
    # indexed by the str(band number)
    base=[gdal.CXT_Element,'VRTDataset']
    if vrt_options_list is None:
        base.append([gdal.CXT_Attribute,'rasterXSize',
                     [gdal.CXT_Text,str(indatasetlist[0].RasterXSize)]])
        base.append([gdal.CXT_Attribute,'rasterYSize',
                     [gdal.CXT_Text,str(indatasetlist[0].RasterYSize)]])
    else:
        bopts=band_opts[0]
        if bopts.has_key('DstRect'):
            # For now, get dataset size form first band
            (dpix,dline,dxsize,dysize)=bopts['DstRect']
            base.append([gdal.CXT_Attribute,'rasterXSize',
                         [gdal.CXT_Text,str(dxsize)]])
            base.append([gdal.CXT_Attribute,'rasterYSize',
                         [gdal.CXT_Text,str(dysize)]])
        else:
            base.append([gdal.CXT_Attribute,'rasterXSize',
                         [gdal.CXT_Text,str(indatasetlist[0].RasterXSize)]])
            base.append([gdal.CXT_Attribute,'rasterYSize',
                         [gdal.CXT_Text,str(indatasetlist[0].RasterYSize)]])

    mbase=serializeMetadata(indatasetlist[0])
    if mbase is not None:
        base.append(mbase)

    if vrt_options_list is None:
        geopref=None
        vrt_options=None
    elif type(vrt_options_list) == type([]):
        geopref=vrt_options_list[0].get_geopref()
        vrt_options=vrt_options_list[0]
    else:
        geopref=vrt_options_list.get_geopref()
        vrt_options=vrt_options_list
        
    if ((geopref == 'gcps') or (geopref is None)):
        # If preference is gcps or none, copy any available gcp information
        gcpbase=serializeGCPs(indatasetlist[0],vrt_options)
        if gcpbase is not None:
            base.append(gcpbase)

        if ((gcpbase is None) and (geopref == 'gcps')):
            print 'Warning- No gcp information to transfer.'
        
    if ((geopref == 'geotransform') or (geopref is None)):
        # If preference is geotransform or none, copy any available
        # geotransform information.  If geopref is None and
        # vrt indicates that the user wishes to reproject georeferencing,
        # convert to gcps and serialize them.

        srs_text=indatasetlist[0].GetProjection()
        if vrt_options is not None:
            reproj=vrt_options.reproj
            if reproj == srs_text:
                reproj=None
        else:
            reproj=None
            
        if ((reproj is not None) and (srs_text is not None) and
            (len(srs_text) > 0) and (gcpbase is None)):
            
            if geopref is None:
                gcps=GeoTransformToGCPs(indatasetlist[0].GetGeoTransform(),
                                        indatasetlist[0].RasterXSize,
                                        indatasetlist[0].RasterYSize)
                gcpbase=serializeGCPs(indatasetlist[0],vrt_options,
                         gcplist=gcps,projection_attr_txt=srs_text)
                
                if gcpbase is not None:
                    base.append(gcpbase)
            else:
                print 'Warning- reprojection of a geotransform to a '+\
                      '\n        new geotransform not supported.'
        elif (reproj is None):
            if ((srs_text is not None) and (len(srs_text) > 0)):
                prjbase=[gdal.CXT_Element,'SRS',[gdal.CXT_Text,srs_text]]      
                base.append(prjbase)
           
            gbase=serializeGeoTransform(indatasetlist[0],vrt_options)
            if gbase is not None:
                base.append(gbase)

            if ((gbase is None) and (geopref == 'geotransform')):
                print 'Warning- No geotransform information to transfer.'
        elif gcpbase is None:
            print 'Warning- No reprojectable geotransform information found.'
    
    for idx in range(len(indatasetlist)):
        indataset=indatasetlist[idx]
        if band_lists is None:
            band_list=None
        else:
            band_list=band_lists[idx]
            
        if band_list is None:
            for cband in range(1,indataset.RasterCount+1):
                if band_opts[idx].has_key(str(cband)):
                    bbase=serializeBand(indataset,
                                        opt_dict=band_opts[idx][str(cband)])
                    base.append(bbase)
                else:
                    opt_dict={}
                    opt_dict['band']=str(cband)
                    opt_dict['SourceBand']=str(cband)
                    bbase=serializeBand(indataset,opt_dict=opt_dict)
                    base.append(bbase)
        else:
            for cband in band_list:
                if band_opts.has_key(str(cband)):
                    bbase=serializeBand(indataset,
                                        opt_dict=band_opts[idx][str(cband)])
                    base.append(bbase)
                else:
                    opt_dict={}
                    opt_dict['band']=str(cband)
                    opt_dict['SourceBand']=str(cband)
                    bbase=serializeBand(indataset,opt_dict=opt_dict)
                    base.append(bbase)
        
    return base
                    
    
def serializeDataset(indataset,vrt_options=None,band_list=None):
    if vrt_options is None:
        band_opts={}
    else:
        band_opts=vrt_options.get_opts()
        
    # band opts: A dictionary of band option dictionaries,
    # indexed by the str(band number)
    base=[gdal.CXT_Element,'VRTDataset']
    if vrt_options is None:
        base.append([gdal.CXT_Attribute,'rasterXSize',
                     [gdal.CXT_Text,str(indataset.RasterXSize)]])
        base.append([gdal.CXT_Attribute,'rasterYSize',
                     [gdal.CXT_Text,str(indataset.RasterYSize)]])
    else:
        bopts=band_opts[band_opts.keys()[0]]
        if bopts.has_key('DstRect'):
            # For now, get dataset size form first band
            (dpix,dline,dxsize,dysize)=bopts['DstRect']
            base.append([gdal.CXT_Attribute,'rasterXSize',
                         [gdal.CXT_Text,str(dxsize)]])
            base.append([gdal.CXT_Attribute,'rasterYSize',
                         [gdal.CXT_Text,str(dysize)]])
        else:
            base.append([gdal.CXT_Attribute,'rasterXSize',
                         [gdal.CXT_Text,str(indataset.RasterXSize)]])
            base.append([gdal.CXT_Attribute,'rasterYSize',
                         [gdal.CXT_Text,str(indataset.RasterYSize)]])

    mbase=serializeMetadata(indataset)
    if mbase is not None:
        base.append(mbase)

    geopref=None
    if vrt_options is not None:
        geopref=vrt_options.get_geopref()

    gcpbase=None    
    if ((geopref == 'gcps') or (geopref is None)):
        # If preference is gcps or none, copy any available gcp information
        gcpbase=serializeGCPs(indataset,vrt_options)
        if gcpbase is not None:
            base.append(gcpbase)

        if ((gcpbase is None) and (geopref == 'gcps')):
            print 'Warning- No gcp information to transfer.'
        
    if ((geopref == 'geotransform') or (geopref is None)):
        # If preference is geotransform or none, copy any available
        # geotransform information.  If geopref is None and
        # vrt indicates that the user wishes to reproject georeferencing,
        # convert to gcps and serialize them.

        srs_text=indataset.GetProjection()
        if vrt_options is not None:
            reproj=vrt_options.reproj
            if reproj == srs_text:
                reproj=None
        else:
            reproj=None
            
        if ((reproj is not None) and (srs_text is not None) and
            (len(srs_text) > 0) and (gcpbase is None)):
            
            if geopref is None:
                gcps=GeoTransformToGCPs(indataset.GetGeoTransform(),
                                        indataset.RasterXSize,
                                        indataset.RasterYSize)
                gcpbase=serializeGCPs(indataset,vrt_options,gcplist=gcps,
                                      projection_attr_txt=srs_text)
                
                if gcpbase is not None:
                    base.append(gcpbase)
            else:
                print 'Warning- reprojection of a geotransform to a '+\
                      '\n        new geotransform not supported.'
        elif (reproj is None):
            if ((srs_text is not None) and (len(srs_text) > 0)):
                prjbase=[gdal.CXT_Element,'SRS',[gdal.CXT_Text,srs_text]]      
                base.append(prjbase)
           
            gbase=serializeGeoTransform(indataset,vrt_options)
            if gbase is not None:
                base.append(gbase)

            if ((gbase is None) and (geopref == 'geotransform')):
                print 'Warning- No geotransform information to transfer.'
        elif gcpbase is None:
            print 'Warning- No reprojectable geotransform information found.'
         

    if band_list is None:
        for cband in range(1,indataset.RasterCount+1):
            if band_opts.has_key(str(cband)):
                bbase=serializeBand(indataset,opt_dict=band_opts[str(cband)])
                base.append(bbase)
            else:
                opt_dict={}
                opt_dict['band']=str(cband)
                opt_dict['SourceBand']=str(cband)
                bbase=serializeBand(indataset,opt_dict=opt_dict)
                base.append(bbase)
    else:
        for cband in band_list:
            if band_opts.has_key(str(cband)):
                bbase=serializeBand(indataset,opt_dict=band_opts[str(cband)])
                base.append(bbase)
            else:
                opt_dict={}
                opt_dict['band']=str(cband)
                opt_dict['SourceBand']=str(cband)
                bbase=serializeBand(indataset,opt_dict=opt_dict)
                base.append(bbase)
        
    return base

def serializeRawBand(SourceFilename, band, DataType, ByteOrder,
                      ImageOffset, PixelOffset, LineOffset,Description=None):
    """ Serialize a raw (flat binary) raster band.
        Inputs:
        
        SourceFilename- filename of a gdal dataset (a string)
                    
        band- band number that the serialized band will correspond
              to in the output dataset (an integer).

        DataType- data type (a string).  May be 'Byte', 'UInt16',
                  'Int16', 'UInt32', 'Int32', 'Float32', 'Float64',
                  'CInt16', 'CInt32', 'CFloat32', 'CFloat64'.
                  
        ByteOrder- MSB or LSB (string)
        
        ImageOffset- offset to first pixel of band (int)
                
        PixelOffset- offset between successive pixels in the input (int)

        LineOffset- offset between successive lines in the input (int)

        Description- OPTIONAL description for the band (a string)
    """
    base=[gdal.CXT_Element,'VRTRasterBand']
        
    base.append([gdal.CXT_Attribute,'dataType',
                     [gdal.CXT_Text,DataType]])
        
    base.append([gdal.CXT_Attribute,'band',[gdal.CXT_Text,str(band)]])

    base.append([gdal.CXT_Attribute,'subClass',
                 [gdal.CXT_Text,"VRTRawRasterBand"]])

    if Description is not None:
        base.append([gdal.CXT_Element,'Description',
                       [gdal.CXT_Text,Description]])
        
    base.append([gdal.CXT_Element,'SourceFilename',
                       [gdal.CXT_Text,SourceFilename]])
    base[len(base)-1].append([gdal.CXT_Attribute,'relativeToVRT',
                    [gdal.CXT_Text,GetRelativeToVRT(SourceFilename)]])

    base.append([gdal.CXT_Element,'ByteOrder',
                       [gdal.CXT_Text,ByteOrder]])

    base.append([gdal.CXT_Element,'ImageOffset',
                       [gdal.CXT_Text,str(ImageOffset)]])

    base.append([gdal.CXT_Element,'PixelOffset',
                       [gdal.CXT_Text,str(PixelOffset)]])

    base.append([gdal.CXT_Element,'LineOffset',
                       [gdal.CXT_Text,str(LineOffset)]])

    return base
    
def serializeBand(indataset=None,opt_dict={}):
    """ Serialize a raster band.
        Inputs:
            indataset- dataset to take default values from for
                       items that are not specified in opt_dict.
                       Set to None if not needed.
                       
            opt_dict- dictionary to take values from.

        opt_dict will be searched for the following keys:

        SourceFilename- filename of a gdal dataset (a string)
        
        SourceBand- an integer indicating the band from SourceFilename
                    to use.  1 if not specified.
                    
        band- band number that the serialized band will correspond
              to in the output dataset (an integer).  1 if not specified.

        DataType- data type (a string).  May be 'Byte', 'UInt16',
                  'Int16', 'UInt32', 'Int32', 'Float32', 'Float64',
                  'CInt16', 'CInt32', 'CFloat32', 'CFloat64'

        Description- OPTIONAL description to associate with the band (string).

        ColorInterp- OPTIONAL colour interpretation (a string).  One of
                     'Gray', 'Red', 'Green', 'Blue', 'Alpha', 'Undefined', or
                     'Palette'.  If palette is specified, then opt_dict
                     must also have a key 'Palette' with a value that
                     is a gdal ColorTable object.

        NoDataValue- OPTIONAL no data value.  Floating point or integer.

        ScaleOffset, ScaleRatio- OPTIONAL scaling offset and ratio for
                     rescaling the input bands (floating point numbers):
                     outband = ScaleOffset + (ScaleRatio*inband)

        SrcRect- a tuple of four integers specifying the extents of the
                 source to use (xoffset, yoffset, xsize, ysize)

        DstRect- a tuple of four integers specifying the extents that
                 SrcRect will correspond to in the output file.
                     
    """
    base=[gdal.CXT_Element,'VRTRasterBand']

    if opt_dict.has_key('SourceBand'):
        inband=int(opt_dict['SourceBand'])
    else:
        inband=1
    
    if opt_dict.has_key('band'):    
        outband=int(opt_dict['band'])
    else:
        outband=1
     
    if opt_dict.has_key('DataType'):
        base.append([gdal.CXT_Attribute,'dataType',
                     [gdal.CXT_Text,opt_dict['DataType']]])        
    elif indataset is not None:
        base.append([gdal.CXT_Attribute,'dataType',
                     [gdal.CXT_Text,
                      gdal.GetDataTypeName(
            indataset.GetRasterBand(inband).DataType)]])
    else:
        base.append([gdal.CXT_Attribute,'dataType',[gdal.CXT_Text,'Byte']])

        
    base.append([gdal.CXT_Attribute,'band',[gdal.CXT_Text,str(outband)]])

    if opt_dict.has_key('Description'):
        base.append([gdal.CXT_Element,'Description',
                         [gdal.CXT_Text,opt_dict['Description']]])
    elif indataset is not None:
        desc = indataset.GetRasterBand(inband).GetDescription()
        if len(desc) > 0:
            base.append([gdal.CXT_Element,'Description',
                         [gdal.CXT_Text,desc]])
        
    if opt_dict.has_key('ColorInterp'):
        if opt_dict['ColorInterp'] != 'Undefined':
            base.append([gdal.CXT_Element,'ColorInterp',
                         [gdal.CXT_Text,opt_dict['ColorInterp']]])
            if opt_dict['ColorInterp'] == 'Palette':
                base.append(opt_dict['Palette'].serialize())
            
    elif indataset is not None:
        cinterp=indataset.GetRasterBand(inband).GetRasterColorInterpretation()
        if cinterp != gdal.GCI_Undefined:
            cinterpname=gdal.GetColorInterpretationName(cinterp)
            base.append([gdal.CXT_Element,'ColorInterp',
                         [gdal.CXT_Text,cinterpname]])
            if cinterpname=='Palette':
                ct = indataset.GetRasterBand(inband).GetRasterColorTable()
                base.append(ct.serialize())

    if opt_dict.has_key('NoDataValue'):
        base.append([gdal.CXT_Element,'NoDataValue',
                         [gdal.CXT_Text,str(opt_dict['NoDataValue'])]])
    elif indataset is not None:
        nodata_val=indataset.GetRasterBand(inband).GetNoDataValue()
        if ((nodata_val is not None) and (nodata_val != '')):
            base.append([gdal.CXT_Element,'NoDataValue',
                         [gdal.CXT_Text,str(nodata_val)]])
                
    if opt_dict.has_key('ScaleOffset') or opt_dict.has_key('ScaleRatio'):
        ssbase=[gdal.CXT_Element,'ComplexSource']
    else:
        ssbase=[gdal.CXT_Element,'SimpleSource']

    if opt_dict.has_key('SourceFilename'):
        ssbase.append([gdal.CXT_Element,'SourceFilename',
                       [gdal.CXT_Text,opt_dict['SourceFilename']]])
        ssbase[len(ssbase)-1].append([gdal.CXT_Attribute,'relativeToVRT',
                 [gdal.CXT_Text,GetRelativeToVRT(opt_dict['SourceFilename'])]])
    elif indataset is not None:
        ssbase.append([gdal.CXT_Element,'SourceFilename',
                       [gdal.CXT_Text,indataset.GetDescription()]])
        ssbase[len(ssbase)-1].append([gdal.CXT_Attribute,'relativeToVRT',
                 [gdal.CXT_Text,GetRelativeToVRT(indataset.GetDescription())]])
    else:
        ssbase.append([gdal.CXT_Element,'SourceFilename',
                       [gdal.CXT_Text,'']])
        ssbase[len(ssbase)-1].append([gdal.CXT_Attribute,
                                      'relativeToVRT',[gdal.CXT_Text,'0']])

    ssbase.append([gdal.CXT_Element,'SourceBand',[gdal.CXT_Text,str(inband)]])

    srcwinbase=[gdal.CXT_Element,'SrcRect']    

    if opt_dict.has_key('SrcRect'):
        xoff=str(opt_dict['SrcRect'][0])
        yoff=str(opt_dict['SrcRect'][1])
        xsize=str(opt_dict['SrcRect'][2])
        ysize=str(opt_dict['SrcRect'][3])
    elif indataset is not None:
        xoff='0'
        yoff='0'
        xsize=str(indataset.GetRasterBand(inband).XSize)
        ysize=str(indataset.GetRasterBand(inband).YSize)
    else:
        xoff='0'
        yoff='0'
        xsize='0'
        ysize='0'
        
    srcwinbase.append([gdal.CXT_Attribute,'xOff',[gdal.CXT_Text,xoff]])        
    srcwinbase.append([gdal.CXT_Attribute,'yOff',[gdal.CXT_Text,yoff]])        
    srcwinbase.append([gdal.CXT_Attribute,'xSize',[gdal.CXT_Text,xsize]])        
    srcwinbase.append([gdal.CXT_Attribute,'ySize',[gdal.CXT_Text,ysize]])        
    ssbase.append(srcwinbase)
    
    dstwinbase=[gdal.CXT_Element,'DstRect']
    if opt_dict.has_key('DstRect'):
        x2off=str(opt_dict['DstRect'][0])
        y2off=str(opt_dict['DstRect'][1])
        x2size=str(opt_dict['DstRect'][2])
        y2size=str(opt_dict['DstRect'][3])
    elif indataset is not None:
        x2off='0'
        y2off='0'
        x2size=str(indataset.GetRasterBand(inband).XSize)
        y2size=str(indataset.GetRasterBand(inband).YSize)
    else:
        x2off='0'
        y2off='0'
        x2size='0'
        y2size='0'

    dstwinbase.append([gdal.CXT_Attribute,'xOff',[gdal.CXT_Text,x2off]])        
    dstwinbase.append([gdal.CXT_Attribute,'yOff',[gdal.CXT_Text,y2off]])        
    dstwinbase.append([gdal.CXT_Attribute,'xSize',[gdal.CXT_Text,x2size]])        
    dstwinbase.append([gdal.CXT_Attribute,'ySize',[gdal.CXT_Text,y2size]])        
    ssbase.append(dstwinbase)

    if opt_dict.has_key('ScaleOffset'):
        ssbase.append([gdal.CXT_Element,'ScaleOffset',[gdal.CXT_Text,str(opt_dict['ScaleOffset'])]])

    if opt_dict.has_key('ScaleRatio'):
        ssbase.append([gdal.CXT_Element,'ScaleRatio',[gdal.CXT_Text,str(opt_dict['ScaleRatio'])]])
        
    base.append(ssbase)

    return base


def GetSimilarFiles(filename):
    """ Looks in the directory of filename for files with the same size
        and extension, and returns a list containing their full paths.
    """

    import os
    import glob
    
    fdir=os.path.dirname(filename)
    froot,fext=os.path.splitext(filename)
    flist=glob.glob(os.path.join(fdir,'*'+fext))

    fsize=os.path.getsize(filename)
    slist=[]
    for item in flist:
        if os.path.getsize(item) == fsize:
            slist.append(item)

    return slist


def GetRelativeToVRT(path):
    """ Returns '0' if path is absolute, '1' if it is
        relative to vrt.
    """
    if path[0] == '<':
        # input path is an in-memory vrt file
        return "0"
    
    if os.path.isabs(path):
        return "0"
    else:
        return "1"

class VRTDatasetConstructor:
    """ Class to use for creating vrt datasets from scratch at
        the python level.

        Initial inputs:
            pixels- number of pixels in dataset
            lines- number of lines in dataset
    """
    def __init__(self,pixels,lines):
        self.base=[gdal.CXT_Element,'VRTDataset']
        self.base.append([gdal.CXT_Attribute,'rasterXSize',
                     [gdal.CXT_Text,str(pixels)]])
        self.base.append([gdal.CXT_Attribute,'rasterYSize',
                     [gdal.CXT_Text,str(lines)]])
        self.band_idx=1
        self.xsize=pixels
        self.ysize=lines

    def AddSimpleBand(self, SourceFilename, SourceBand, DataType,
                      SrcRect=None, DstRect=None, ColorInterp='Undefined',
                      colortable=None, NoDataValue=None,
                      ScaleOffset=None,ScaleRatio=None,
                      Description=None):
        """ Add a simple raster band

        SourceFilename- filename of a gdal dataset (a string)
        
        SourceBand- an integer indicating the band from SourceFilename
                    to use.

        DataType- data type (a string).  May be 'Byte', 'UInt16',
                  'Int16', 'UInt32', 'Int32', 'Float32', 'Float64',
                  'CInt16', 'CInt32', 'CFloat32', 'CFloat64'

        SrcRect- a tuple of four integers specifying the extents of the
                 source to use (xoffset, yoffset, xsize, ysize).
                 Defaults to (0, 0, xsize, ysize) for the dataset.

        DstRect- a tuple of four integers specifying the extents that
                 SrcRect will correspond to in the output file.
                 Defaults to (0, 0, xsize, ysize) for the dataset.
                 
        ColorInterp- OPTIONAL colour interpretation (a string).  One of
                     'Gray', 'Red', 'Green', 'Blue', 'Alpha', 'Undefined', or
                     'Palette'.  If 'Palette' is specified, then colortable
                     must also be specified.

        colortable- GDAL colortable object (only used if ColorInterp
                    is set to 'Palette').
                    
        NoDataValue- OPTIONAL no data value.  Floating point or integer.

        ScaleOffset, ScaleRatio- OPTIONAL scaling offset and ratio for
                     rescaling the input bands (floating point numbers):
                     outband = ScaleOffset + (ScaleRatio*inband)

        Description- OPTIONAL description for the band (a string).
       
        """
        opt_dict={'SourceFilename':SourceFilename,'SourceBand':SourceBand,
                  'DataType':DataType,'ColorInterp':ColorInterp}

        if ColorInterp == 'Palette':
            if colortable is None:
                raise 'Colour table not specified!'
            opt_dict['Palette']=colortable
        
        if SrcRect is not None:
            opt_dict['SrcRect']=SrcRect
        else:
            opt_dict['SrcRect']=(0,0,self.xsize,self.ysize)

        if DstRect is not None:
            opt_dict['DstRect']=DstRect
        else:
            opt_dict['DstRect']=(0,0,self.xsize,self.ysize)

        if ScaleOffset is not None:
            opt_dict['ScaleOffset']=ScaleOffset

        if ScaleRatio is not None:
            opt_dict['ScaleRatio']=ScaleRatio

        if NoDataValue is not None:
            opt_dict['NoDataValue']=NoDataValue

        if Description is not None:
            opt_dict['Description']=Description

        opt_dict['band']=self.band_idx
        
        bbase=serializeBand(None,opt_dict)
        
        self.base.append(bbase)
        self.band_idx=self.band_idx+1

    def AddRawBand(self, SourceFilename, DataType, ByteOrder,
                      ImageOffset, PixelOffset, LineOffset,
                      Description=None):
        """ Add a flat binary source raster band.
            Inputs:
                SourceFilename- path to source file name (string)
                
                DataType- datatype (string).  One of:
                                Byte        Float64
                                UInt16      CInt16
                                Int16       CInt32
                                UInt32      CFloat32
                                Int32       CFloat64
                                Float32

                ByteOrder- MSB or LSB (string)
                
                ImageOffset- offset to first pixel of band (int)
                
                PixelOffset- offset between successive pixels in the input (int)

                LineOffset- offset between successive lines in the input (int)

                Description- OPTIONAL description for the band (a string). 
        """
        bbase=serializeRawBand(SourceFilename,self.band_idx, DataType,
                               ByteOrder,ImageOffset,PixelOffset,
                               LineOffset,Description)
        self.base.append(bbase)
        self.band_idx=self.band_idx+1

    def AddMetadata(self, metadict):
        """ Add metadata from a dictionary """
        if len(metadict.keys()) < 1:
            return
        
        mbase=serializeMetadata(dict=metadict)
        self.base.append(mbase)

    def SetSRS(self, projection):
        """ Set projection information for geotransform (a WKT string)"""
        prjbase=[gdal.CXT_Element,'SRS',[gdal.CXT_Text,projection]]      
        self.base.append(prjbase)

    def SetGeoTransform(self, gt, srcrect=None, dstrect=None, force_geo=0):
        """ Add a geotransform (input is a tuple of 6 numbers)
            
            Optional srcrect and dstrect arguments are used to shift
            and scale the transform in case of cropping or resolution
            changes.  The srcrect and dstrect arguments must both be
            tuples of the form (xstart,ystart,xsize,ysize).  If only
            one is specified, it will be ignored.

            force_geo- Set to 1 to force the geotransform to be serialized
                       even if the input geotransform is just the
                       default.  Is 0 (off) by default.
         """
        gbase=serializeGeoTransform(geotransform=gt, srcrect=srcrect,
                                    dstrect=dstrect, force_geo=force_geo)
        if gbase is not None:
            self.base.append(gbase)

    def SetGCPs(self, gcps, projection='', reprojection=None, srcrect=None,
                dstrect=None):
        """ Add gcps from a list of GDAL GCP objects.
            Optional projection argument should be a WKT string.
            Optional reprojection argument should also be a WKT
            string, and should only be specified if the projection
            argument is also specified.
            
            Optional srcrect and dstrect arguments are used to shift
            and scale the gcps in case of cropping or resolution
            changes.  The srcrect and dstrect arguments must both be
            tuples of the form (xstart,ystart,xsize,ysize).  If only
            one is specified, it will be ignored.
        """
        gcpbase=serializeGCPs(gcplist=gcps,projection_attr_txt=projection,
                              reproj=reprojection, srcrect=srcrect,
                              dstrect=dstrect)
        self.base.append(gcpbase)

    def GetVRTLines(self):
        """ Return lines suitable for writing to a vrt file. """
        return gdal.SerializeXMLTree(self.base)

    def GetVRTString(self):
        """ Return a vrt string that can be opened as a gdal dataset. """
        lines = self.GetVRTLines()
        vrtstr = string.join(lines,'')
        return vrtstr


if __name__ ==  '__main__':
    import string
    
    ds=VRTDatasetConstructor(2000,2000)
    ds.AddSimpleBand('reltest.tif',2,'Float32')
    ds.AddSimpleBand('/data/abstest.tif',1,'Byte',
                     SrcRect=(1000,2000,4000,4000),
                     ScaleOffset=2,ScaleRatio=3)
    ds.AddRawBand('rawtest.x00','CFloat32','MSB',0,8,16000)
    for item in string.split(ds.GetVRTLines(),'\n'):
        print item
        

