		Open Source GIS/RS Binary Kit for Windows
		=========================================

FWTools For Windows 98/NT/2000
------------------------------

VERSION: FWTools 2.4.7  (Jan 19, 2010)

After installing FWTools you should have a new FWTools menu group in
Start->All Programs list.  From there you can launch OpenEV directly or
launch a command shell with the environment all setup to run the various
commands for GDAL, OGR, PROJ, MapServer and related projects.  

You can also use the various commands from other win32 command shells as long
as you run the setfw.bat file in the FWTools directly first to setup the 
PATH and various other environment variables.  


Other Libraries, and Utilities
------------------------------
 o MapServer (4.9cvs): cgi and utilities, with WFS/WMS server and client, 
   WCS server, freetype, gdal/ogr, PostGIS, and Python and CSharp MapScript.
 o GDAL-svn, including gdalinfo, gdal_translate, and gdaltindex, and gdalwarp.
   - Includes JPEG2000 (Kakadu and ECW), HDF4, HDF5, ECW, netcdf, MrSID,
     GRIB and OGDI raster support. 
   - Includes C#, VB6 and Python bindings.
 o OGR-svn, including ogrinfo, ogr2ogr, and ogrtindex utilities.
   - Includes OGDI vector, PostGIS, SQLite and GML support.
   - Includes C#, Python bindings and WCTS server.
 o Mario B's WMSTool for OpenEV.
 o PROJ 4.5.0 plus proj.exe and cs2cs.exe and Canadian and US grid shift files
 o Gnuplot plotting package (run pgnuplot).
 o OGDI 3.1.5, gltpd, ogdi_import and ogdi_info
 o GEOS 3.0.0 (rc2)
 o Python 2.3.4



About this Package
------------------ 

This package was prepared by Frank Warmerdam (warmerdam@pobox.com) as a
handy bundle containing several related packages, with a maximum of 
inter-component linkages enabled and the most recent code from CVS.  It is 
considerably more ad-hoc than some of the more formal release packages, but 
it may have greater functionality than formal releases.  This package 
aspires to be a "tool bench" of GIS/RS tools for the end user.

  http://fwtools.maptools.org/

