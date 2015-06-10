##############################################################################
# wmstool.py, v1.07b 2005/09/14
#
# Project:  OpenEV
# Purpose:  WMS Client support for OpenEV, tool version.
# Author:  Mario Beauchamp
# Comments: Beta release for testing.
# TODO: Cache management dialog. Better handling of exceptions.
###############################################################################
#
#  Revision 1.07b 2005/09/14
#  Added Help button.
#  Fixed for Python 2.2.
#
#  Revision 1.06b 2005/08/16
#  Fixed proxies support so it works with Python <2.3 as well.
#
#  Revision 1.05b 2005/06/15
#  Added support for http proxy.
#  Changed datatype in vrt files from 'Byte' to datatype of returned images.
#    This will ensure correct interpretation of elevation data, for example.
#  Service exception reports now displayed.
#
#  Revision 1.04b 2005/03/30
#  Fixed failure to return the proper SRS in getSRS().
#
#  Revision 1.03b 2005/03/26
#  Corrected problem when saving a new map.
#
#  Revision 1.02b 2005/03/25
#  Fixed a problem when deleting a map or saving an existing one after edits.
#  Changed the name of the default map to "landsat321" instead of "Landsat321".
#  Added a way to put the tool in the icon bar.
#  Added a way to set a more suitable background color.
#
#  Revision 1.01b 2005/03/25
#  Corrected a few bugs. Added way to select layers without opening Props window.
#  Added ServiceCaps.validateURL().
#
#  Revision 1.00b 2005/03/24
#  Beta release.
#
###############################################################################
import gtk
from gtk import TRUE,FALSE # for convenience...
import os
import osr
import vrtutils
import gdal
import gvutils
import gview
import pickle
import urllib
import gvsignaler
import pgucolor
import gviewapp

wms_dir = os.path.join(gview.home_dir,'wms')
cachepath = os.path.join(wms_dir,'cache')
srv_dir = os.path.join(wms_dir,'services')

global servDic

# set desired proxy in prefs file (.openev) as such:
# http_proxy=http://170.222.120.200:8000/
proxy = gview.get_preference('http_proxy')
if proxy != None:
    proxyDic = {'http':proxy}
else:
    proxyDic = None

def loadServices():
    global servDic
    servDic = {}
    hosts = os.listdir(srv_dir)
    for host in hosts:
        srvnames = os.listdir(os.path.join(srv_dir,host))
        for name in srvnames:
            servDic[name[:-4]] = host

def openService(srvname):
    host = servDic[srvname]
    path = os.path.join(srv_dir,host,srvname+'.xml')
    if servCaps.open(path):
        # we don't need the buffer here
        del servCaps.buffer
        servCaps.buffer = None
        return 1
    else: # unlikely but just in case...
        gvutils.error(path+' does not appear to be a valid GetCapabilities response.')
        return 0


def createCapsEntry(srvname,path=srv_dir):
    host,p = urllib.splithost(urllib.splittype(servCaps.href)[1])
    hname = host.split(':')[0]
    newhost = os.path.join(path,hname)

    if not os.path.exists(newhost):
        os.mkdir(newhost)

    newcaps = os.path.join(newhost,srvname+'.xml')
    fd = file(newcaps,'w')
    fd.write(servCaps.buffer)
    fd.close()
    return hname

def buildServicesDir(lst,path=srv_dir):
    for line in lst:
        if not line.startswith('#'):
            srvname,url = line.split(',')
            if servCaps.open(url):
                if createCapsEntry(srvname,path) is None:
                    print "Service "+url+" not saved"
                    outfile = os.path.join(path,srvname+'-tmp.xml')
                    fd = file(outfile,'w')
                    fd.write(servCaps.buffer)
                    fd.close()
                else:
                    print "Service "+servCaps.title+" saved"

                del servCaps.buffer
                servCaps.buffer = None
            else:
                print "Service "+url+" not saved"
                print "Server responded:"
                print servCaps.buffer
                del servCaps.buffer
                servCaps.buffer = None

def fixCaps(xmlStr):
    idx = xmlStr.find('[')
    if idx > 0:
        idx2 = xmlStr.find(']>') + 1
        return xmlStr.replace(xmlStr[idx:idx2],'')
    return xmlStr

def Element(tag, attrib={}, **extra):
    attrib = attrib.copy()
    attrib.update(extra)
    return _ElementInterface(tag, attrib)

def makeElement(node):
    if hasattr(node, "tag"):
        return node
    attrib = {}
    tag = ''
    text = ''
    children = []
    element = None
    if node[0] == gdal.CXT_Element:
        tag = node[1]
        for subnode in node[2:]:
            if subnode[0] == gdal.CXT_Attribute:
                attrib[subnode[1]] = subnode[2][1]
            elif subnode[0] == gdal.CXT_Element:
                children.append(subnode)
            elif subnode[0] == gdal.CXT_Text:
                text = subnode[1]

        element = Element(tag,attrib)
        element.text = text
        element._children = children

    return element

class _ElementInterface:
    tag = None
    attrib = None
    text = None
    def __init__(self, tag, attrib):
        self.tag = tag
        self.attrib = attrib
        self._children = []

    def __getitem__(self,index):
        return self._children[index]

    def __len__(self):
        return len(self._children)

    def _find(self,path,all=0):
        foundLst=[]
        splitted = path.split('/',1)
        if len(splitted) == 2:
            component, remainder = splitted
        else:
            component, remainder = splitted[0], None
        for subnode in self._children:
            if subnode[1] == component:
                if remainder is None:
                    foundLst.append(subnode)
                    if not all:
                        break
                else:
                    subElem = makeElement(subnode)
                    subLst = subElem._find(remainder,all)
                    if subLst is not None:
                        if all == 1:
                            foundLst.extend(subLst)
                        else:
                            foundLst.append(subLst)
 
        if len(foundLst) == 0:
            return None
        elif all == 1:
            return foundLst
        else:
            return foundLst[0]

    def append(self,element):
        self._children.append(element)

    def get(self,key,default=None):
        return self.attrib.get(key,default)

    def find(self,path):
        result = self._find(path)
        if result is None:
            return None

        return makeElement(result)

    def findall(self,path):
        result = self._find(path,all=1)
        if result is None:
            return None

        foundLst = []
        for child in result:
            foundLst.append(makeElement(child))

        return foundLst

    def findtext(self,path,default=None):
        result = self.find(path)
        if result is None:
            return default

        return result.text

    def getiterator(self,tag=None):
        nodes = []
        for node in self._children:
            elem = makeElement(node)
            if tag is None or elem.tag == tag:
                nodes.append(elem)
        return nodes

    def items(self):
        return self.attrib.items()

    def keys(self):
        return self.attrib.keys()

class ElementTree:
    def __init__(self, element=None):
        self._root = element # first node

    def getroot(self):
        return self._root

    def parse(self,capsBuf):
        rawXML = fixCaps(capsBuf)
        try:
            tree = gdal.ParseXMLString(rawXML)
        except:
            return None

        element = makeElement(tree[len(tree)-1])
        if element is None:
            return None

        self._root = element

        return rawXML

    def find(self,path):
        return self._root.find(path)

    def findall(self,path):
        return self._root.findall(path)

    def findtext(self,path,default=None):
        return self._root.findtext(path,default)

    def getiterator(self,tag=None):
        return self._root.getiterator(tag)

class ServiceCaps(ElementTree):
    def __init__(self):
        ElementTree.__init__(self)
        self.title = None
        self.buffer = None

    def open(self,url):
        del self._root
        self._root = None
        capsBuf = self.getCapabilities(url)
        # checks
        if capsBuf is None:
            self.buffer = ''
            return 0
        self.buffer = self.parse(capsBuf)
        if self._root is None:
            return 0
        if self._root.tag != 'WMT_MS_Capabilities':
            return 0

        self.version = self._root.get('version')
        servTree = self.find('Service')
        self.name = servTree.findtext('Name')
        self.abstract = servTree.findtext('Abstract')
        self.title = servTree.findtext('Title')
        self.layer = self.find('Capability/Layer')
        self.layer.title = self.layer.findtext('Title')
        res = self.find('Capability/Request/GetMap/DCPType/HTTP/Get/OnlineResource')
        self.href = res.get('xlink:href')
        if not '?' in self.href:
            self.href+='?'
        # we got here so everything is ok.
        return 1

    def getCapabilities(self,url):
        type,path = urllib.splittype(url)
        if path.endswith('?'):
            # 1.1.x only
            url+='VERSION=1.1&SERVICE=WMS&REQUEST=GetCapabilities'
        if type == 'http':
            try:
                opener = urllib.URLopener(proxies=proxyDic)
                fp = opener.open(url)
            except:
                return None
        else:
            try:
                fp = file(url,'r')
            except:
                return None

        return fp.read()

    def getTitles(self,tree):
        keys = []
        for node in tree:
            keys.append(node.findtext('Title'))

        keys.sort()
        return keys

    def getLayerNode(self,title=None,name=None):
        # check if we have the root layer
        if name is None:
            if title == self.layer.title:
                return self.layer
        else:
            layname = self.layer.findtext('Name')
            if layname is not None and layname == name:
                return self.layer

        # else iterate the root tree
        rootTree = self.layer.findall('Layer')
        return self.findLayer(rootTree,title,name)

    def findLayer(self,tree,title,name):
        if name is None:
            laynode = self.findByTitle(tree,title)
        else:
            laynode = self.findByName(tree,name)
        if laynode is not None:
            return laynode
        for layer in tree:
            if layer.find('Layer'):
                layerTree = layer.findall('Layer')
                laynode = self.findLayer(layerTree,title,name)
                if laynode is not None:
                    return laynode

    def findByTitle(self,tree,title):
        for node in tree:
            ntitle = node.findtext('Title')
            if ntitle == title:
                return node

    def findByName(self,tree,name):
        for node in tree:
            nname = node.findtext('Name')
            if nname == name:
                return node

    def getPropList(self,path):
        propTree = self.findall(path)
        propLst = []
        for prop in propTree:
            propLst.append(prop.text)

        propLst.sort()
        return propLst

    def getSRSList(self,tree):
        srsLst = []
        srsTree = tree.find('SRS')
        if srsTree is None:
            return None

        lst = srsTree.text.split(' ')
        if len(lst) == 1:
            for srsElem in tree.findall('SRS'):
                srsLst.append(srsElem.text)
        else:
            for srsTxt in lst:
                srsLst.append(srsTxt)

        srsLst.sort()
        return srsLst

    def sortLayerTree(self,laynode):
        titles = []
        layerTree = laynode.getiterator('Layer')
        for node in layerTree:
            titles.append(node.findtext('Title'))
        
        titles.sort()
        sorted = []
        for title in titles:
            sorted.append(self.findByTitle(layerTree,title))

        return sorted

    def encodeURL(self,parmDic,url=None):
        parms = {}
        if url is None:
            url = self.href

        for parm,value in parmDic.items():
            if parm == 'STYLES' or parm == 'map':
                pass
            elif parm == 'LAYERS':
                layerLst = []
                styleLst = []
                for title in parmDic['LAYERS']:
                    node = self.getLayerNode(title)
                    name = node.findtext('Name')
                    layerLst.append(name)
                    idx = parmDic['LAYERS'].index(title)
                    stitle = parmDic['STYLES'][idx]
                    if len(stitle):
                        style = self.findByTitle(node.findall('Style'),stitle)
                        sname = style.findtext('Name')
                    else:
                        sname = ''
                    styleLst.append(sname)
                parms['LAYERS'] = ','.join(layerLst)
                parms['STYLES'] = ','.join(styleLst)
            elif type(value) == type([]):
                parms[parm] = ','.join(parmDic[parm])
            else:
                parms[parm] = parmDic[parm]

        return url + urllib.urlencode(parms)

    def decodeURL(self,url):
        splitLst = url.split('?')
        parmLst = splitLst[1].split('&')
        parmDic = {}
        for parmStr in parmLst:
            parmLst = parmStr.split('=')
            parmDic[parmLst[0]] = urllib.unquote_plus(parmLst[1])
        
        layerLst = parmDic['LAYERS'].split(',')
        styleLst = parmDic['STYLES'].split(',')
        laytitles = []
        stytitles = []
        for name in layerLst:
            node = self.getLayerNode(name=name)
            title = node.findtext('Title')
            laytitles.append(title)
            idx = layerLst.index(name)
            if len(styleLst[idx]):
                style = self.findByName(node.findall('Style'),styleLst[idx])
                stitle = style.findtext('Title')
            else:
                stitle = ''
            stytitles.append(stitle)
            
        parmDic['LAYERS'] = laytitles
        parmDic['STYLES'] = stytitles

        return parmDic

    def validateSRS(self,srs):
        srsLst = self.getSRSList(self.layer)
        for srsTxt in srsLst:
            if srsTxt == srs:
                return 1

        return 0

    def validateURL(self,url):
        try:
            params = self.decodeURL(url)
        except:
            return 'Invalid URL'

    def getMap(self,url):
        opener = urllib.URLopener(proxies=proxyDic)
        f = opener.open(url)
        h = f.info()
        if h.getheader('Content-Type') == 'application/vnd.ogc.se_xml':
            print 'Exception occured'
        return f

servCaps = ServiceCaps()

class WMSTool(gviewapp.Tool_GViewApp):
    def __init__(self,app=None):
        gviewapp.Tool_GViewApp.__init__(self,app)
        self.init_menu()
        # uncomment this line if you want to create an icon entry
##        self.init_icon()

    def launch_window(self,*args):
        self.win = WMSDialog()
        if self.win is None:
            return
        else:
            self.win.show()

    def init_menu(self):
        self.menu_entries.set_entry("Tools/WMS maps",1,self.launch_window)

    def init_icon(self):
        self.icon_entries.set_entry("worldrgb.xpm","WMS maps",1,self.launch_window)

class WMSDialog(gtk.GtkWindow):
    def __init__(self):
        gtk.GtkWindow.__init__(self,title='WMS Tool')
        self.set_policy(FALSE,TRUE,TRUE)
        self.tips = gtk.GtkTooltips()
        self.updating = TRUE
        loadServices()
        self.curServ = None
        self.loadMaps()
        self.setMap(self.mapKeys[0])
        self.rezX = 1.0
        self.rezY = 1.0
        self.extentBX = None
        self.viewwin = gview.app.view_manager.get_active_view_window()
        self.srs = self.getSRS()
        # uncomment this line if you want to set the view's BG color to yellow
##        self.viewwin.viewarea.set_background_color((1,1,0.8,1))
        self.display_change_id = self.viewwin.viewarea.connect("view-state-changed",self.viewChanged)
        self.active_changed_id = self.viewwin.viewarea.connect("active-changed",self.layerChanged)

        gui_OK = self.createGUI()
        if gui_OK is FALSE:
            return None
        else:
            self.updateGUI()
            self.updateExtentGUI()
            self.updating = FALSE
            self.show_all()

    def createGUI(self):
        mainbox = gtk.GtkVBox(spacing=5)
        mainbox.set_border_width(5)
        self.add(mainbox)

        frame = gtk.GtkFrame("Map")
        mainbox.add(frame,expand=FALSE)

# Map ctrl
        box = gtk.GtkHBox(spacing=5)
        box.set_border_width(5)
        frame.add(box)
        self.mapCB = gtk.GtkCombo()
        self.mapCB.set_popdown_strings(self.mapKeys)
        self.mapCB.list.connect('selection-changed',self.mapSelected)
        box.add(self.mapCB,expand=FALSE)
        box.add(gtk.GtkLabel('Background color'),expand=FALSE)
        self.colorBT = pgucolor.ColorButton((0,0,0,0))
        box.add(self.colorBT,expand=FALSE)

# Map params
        mainbox.add(self.createCornersGUI(),expand=FALSE)
# Resolution
        mainbox.add(self.createResolutionGUI(),expand=FALSE)
# Size
        mainbox.add(self.createSizeGUI(),expand=FALSE)

# Extent
        frame = gtk.GtkFrame("Extent")
        mainbox.add(frame,expand=FALSE)
        self.extentBX = gtk.GtkHBox(spacing=3)
        self.extentBX.set_border_width(3)
        frame.add(self.extentBX)
# Controls
        frame = gtk.GtkFrame("Controls")
        mainbox.add(frame,expand=FALSE)
        vbox = gtk.GtkVBox(spacing=1)
        vbox.set_border_width(5)
        frame.add(vbox)

        box = gtk.GtkHBox(spacing=5)
        vbox.add(box,expand=FALSE)
        self.autoTO = gtk.GtkCheckButton(label='Update from')
        self.autoTO.set_active(TRUE)
        self.autoTO.connect('toggled',self.autoUpdateChanged)
        box.add(self.autoTO,expand=FALSE)

        self.viewModeRB = gtk.GtkRadioButton(label='view')
        self.viewModeRB.set_active(TRUE)
        self.viewModeRB.connect('toggled',self.autoUpdateChanged)
        box.add(self.viewModeRB,expand=FALSE)
        self.layerModeRB = gtk.GtkRadioButton(label='layer',group=self.viewModeRB)
        self.layerModeRB.connect('toggled',self.autoUpdateChanged)
        box.add(self.layerModeRB,expand=FALSE)

        box.add(gtk.GtkLabel('EPSG:'),expand=FALSE)
        self.epsgTE = gtk.GtkEntry()
        self.epsgTE.set_usize(50,-1)
        self.epsgTE.set_text(self.getEPSG())
        self.epsgTE.connect('activate',self.epsgChanged)
        box.add(self.epsgTE,expand=FALSE)


# Buttons
        box = gtk.GtkHBox(spacing=5)
        mainbox.add(box,expand=FALSE)
        getBT = gtk.GtkButton('Get map')
        getBT.connect('clicked',self.addLayer)
        box.add(getBT)

        validBT = gtk.GtkButton('Validate')
        self.tips.set_tip(validBT,'Validate map')
        validBT.connect('clicked',self.validateMap)
        box.add(validBT)

        setupBT = gtk.GtkButton('Setup')
        self.tips.set_tip(setupBT,'Setup maps and services')
        setupBT.connect('clicked',self.setup)
        box.add(setupBT)

        closeBT = gtk.GtkButton('Close')
        closeBT.connect('clicked',self.close)
        box.add(closeBT)

        helpBT = gtk.GtkButton('Help')
        helpBT.connect('clicked',self.help)
        box.add(helpBT)

    def createCornersGUI(self):
        frame = gtk.GtkFrame("Corners")
        vbox = gtk.GtkVBox(spacing=3)
        vbox.set_border_width(5)
        frame.add(vbox)

        # create entries
        isgeo = self.srs.IsGeographic()
        self.ulxGE = GeoEntry(isgeo)
        self.ulyGE = GeoEntry(isgeo)
        self.lrxGE = GeoEntry(isgeo)
        self.lryGE = GeoEntry(isgeo)

# Upper left corner
        box = gtk.GtkHBox(spacing=3)
        vbox.add(box)

        box.add(gtk.GtkLabel('UL '))
        box.add(gtk.GtkLabel('X:'))
        self.ulxGE.connect('changed',self.updateFromEntry,'ulx')
        box.add(self.ulxGE)

        box.add(gtk.GtkLabel('Y:'))
        self.ulyGE.connect('changed',self.updateFromEntry,'uly')
        box.add(self.ulyGE)

# Lower right corner
        box = gtk.GtkHBox(spacing=3)
        vbox.add(box)

        box.add(gtk.GtkLabel('LR '))
        box.add(gtk.GtkLabel('X:'))
        self.lrxGE.connect('changed',self.updateFromEntry,'lrx')
        box.add(self.lrxGE)

        box.add(gtk.GtkLabel('Y:'))
        self.lryGE.connect('changed',self.updateFromEntry,'lry')
        box.add(self.lryGE)

        return frame

    def createResolutionGUI(self):
        frame = gtk.GtkFrame("Resolution")
        vbox = gtk.GtkVBox(spacing=3)
        vbox.set_border_width(5)
        frame.add(vbox)

        box = gtk.GtkHBox(spacing=3)
        vbox.add(box)

        # create entries
        isgeo = self.srs.IsGeographic()
        self.rezxGE = GeoEntry(isgeo,dgsz=15,scsz=48,mtsz=125)
        self.rezxGE.setRound(3)
        self.rezyGE = GeoEntry(isgeo,dgsz=15,scsz=48,mtsz=125)
        self.rezyGE.setRound(3)
        box.add(gtk.GtkLabel('X:'))
        self.rezxGE.connect('changed',self.setResolution,'rezX')
        box.add(self.rezxGE)

        box.add(gtk.GtkLabel('-'))
        self.linkTO = gtk.GtkCheckButton(label='-')
        self.linkTO.set_active(TRUE)
        box.add(self.linkTO,expand=FALSE)

        box.add(gtk.GtkLabel('Y:'))
        self.rezyGE.connect('changed',self.setResolution,'rezY')
        box.add(self.rezyGE)

        return frame

    def createSizeGUI(self):
        frame = gtk.GtkFrame("Size")
        vbox = gtk.GtkVBox(spacing=3)
        vbox.set_border_width(5)
        frame.add(vbox)
        box = gtk.GtkHBox(spacing=3)
        vbox.add(box,expand=FALSE)

        box.add(gtk.GtkLabel('Width: '),expand=FALSE)
        self.wTE = gtk.GtkEntry()
        self.wTE.set_usize(50,-1)
        self.wTE.connect('changed',self.updateFromEntry,'w')
        box.add(self.wTE,expand=FALSE)
        box.add(gtk.GtkLabel('px   '),expand=FALSE)

        isgeo = self.srs.IsGeographic()
        self.xGE = GeoEntry(isgeo)
        self.xGE.connect('changed',self.updateFromEntry,'x')
        box.add(self.xGE)

        box = gtk.GtkHBox(spacing=3)
        vbox.add(box)

        box.add(gtk.GtkLabel('Height:'),expand=FALSE)
        self.hTE = gtk.GtkEntry()
        self.hTE.set_usize(50,-1)
        self.hTE.connect('changed',self.updateFromEntry,'h')
        box.add(self.hTE,expand=FALSE)
        box.add(gtk.GtkLabel('px   '),expand=FALSE)

        self.yGE = GeoEntry(isgeo)
        self.yGE.connect('changed',self.updateFromEntry,'y')
        box.add(self.yGE)

        return frame

    def updateExtentGUI(self):
        children = self.extentBX.children()
        if len(children):
            for child in children:
                child.destroy()

        if 'Extents' in self.curMap:
            vbox = gtk.GtkVBox(spacing=3)
            self.extentBX.add(vbox)
            for parm,value in self.curMap['Extents'].items():
                box = gtk.GtkHBox(spacing=2)
                vbox.add(box,expand=FALSE)
                box.add(gtk.GtkLabel(parm+': '),expand=FALSE)
                box.add(gtk.GtkLabel(value),expand=FALSE)
            editBT = gtk.GtkButton('Edit')
            editBT.set_usize(40,18)
            editBT.connect('clicked',self.editExtentClicked)
            self.extentBX.add(editBT,expand=FALSE)
        else:
            self.extentBX.add(gtk.GtkLabel('No extents defined'))

        self.extentBX.show_all()

    def colorClicked(self,bt):
        self.bgColor = bt.get_color()

    def help(self,bt):
        from gvhtml import LaunchHTML
        LaunchHTML('http://pages.infinit.net/starged/openev/wmstool/home.htm')

    def layerChanged(self,view):
        if not self.autoTO.active or self.updating:
            return

        layer = view.active_layer()
        if layer is None or gvutils.is_of_class(layer.__class__,'GvRasterLayer' ) == 0:
            return

        srs = self.getSRS()
        if not srs.IsSame(self.srs):
            self.srs = srs
            self.epsgTE.set_text(self.getEPSG())
            self.updateModeGUI()

        self.updateGUI()

    def viewChanged(self,view):
        if not self.autoTO.active or self.updating or self.layerModeRB.active:
            return

        self.updateGUI()

    def editExtentClicked(self,*args):
        self.showEditExtentGUI()

    def mapSelected(self,*args):
        if self.updating:
            return
        mapKey = self.mapCB.entry.get_text()
        self.setMap(mapKey)
        self.updateExtentGUI()

    def extentChanged(self,entry,name):
        if self.updating: return
        self.curMap['Extents'][name] = entry.get_text()

    def autoUpdateChanged(self,*args):
        if not self.autoTO.active:
            return
        if self.layerModeRB.active:
            layer = self.viewwin.viewarea.active_layer()
            if layer is None or gvutils.is_of_class(layer.__class__,'GvRasterLayer' ) == 0:
                return

        srs = self.getSRS()
        if not srs.IsSame(self.srs):
            self.srs = srs
            self.epsgTE.set_text(self.getEPSG())
            self.updateModeGUI()

        self.updateGUI()

    def epsgChanged(self,*args):
        espgTxt = self.epsgTE.get_text()
        self.srs = self.getSRS(int(espgTxt))
        self.updateModeGUI()
        self.updateGUI()

    def showEditExtentGUI(self):
        for child in self.extentBX.children():
            child.destroy()
        parms = servCaps.decodeURL(self.curMap['URL'])
        layerNode = servCaps.getLayerNode(parms['LAYERS'][0])
        extentTree = layerNode.findall('Extent')
        vbox = gtk.GtkVBox(spacing=3)
        self.extentBX.add(vbox,expand=FALSE)
        for extent in extentTree:
            name = extent.get('name')
            extentTE = ExtentEntry(extent)
            extentTE.connect('changed',self.extentChanged,name)
            vbox.add(extentTE,expand=FALSE)
            value = extent.text
            if name in self.curMap['Extents']:
                value = self.curMap['Extents'][name]
            extentTE.entry.set_text(value)

        self.extentBX.show_all()

    def updateGUI(self,*args):
        self.updating = TRUE
        if self.viewModeRB.active:
            params = self.getInfoFromView()
        elif self.layerModeRB.active:
            params = self.getInfoFromLayer()
        else:
            return
        self.ulxGE.setValue(params[0])
        self.ulyGE.setValue(params[1])
        self.lrxGE.setValue(params[2])
        self.lryGE.setValue(params[3])
        self.rezxGE.setValue(self.rezX)
        self.rezyGE.setValue(abs(self.rezX))
        self.wTE.set_text(str(params[4]))
        self.hTE.set_text(str(params[5]))
        self.xGE.setValue(params[6])
        self.yGE.setValue(params[7])
        self.updating = FALSE

    def updateModeGUI(self):
        self.updating = TRUE
        isgeo = self.srs.IsGeographic()
        self.ulxGE.setMode(isgeo)
        self.ulyGE.setMode(isgeo)
        self.lrxGE.setMode(isgeo)
        self.lryGE.setMode(isgeo)
        self.rezxGE.setMode(isgeo)
        self.rezyGE.setMode(isgeo)
        self.xGE.setMode(isgeo)
        self.yGE.setMode(isgeo)
        self.updating = FALSE

    def updateFromEntry(self,entry,id):
        if self.updating:
            return
        self.updating = TRUE
        rezX = self.rezX
        rezY = self.rezY
        if id == 'lrx':
            lrx = self.lrxGE.getValue()
            ulx = self.ulxGE.getValue()
            x = abs(ulx - lrx)
            self.xGE.setValue(x)
            w = int(x/rezX)
            self.wTE.set_text(str(w))
        elif id == 'lry':
            lry = self.lryGE.getValue()
            uly = self.ulyGE.getValue()
            y = abs(uly - lry)
            self.yGE.setValue(y)
            h = int(y/abs(rezY))
            self.hTE.set_text(str(h))
        elif id == 'w' or id == 'ulx':
            txt = self.wTE.get_text()
            if not len(txt): return
            w = int(txt)
            x = w*rezX
            self.xGE.setValue(x)
            ulx = self.ulxGE.getValue()
            lrx = ulx+x
            self.lrxGE.setValue(lrx)
        elif id == 'h' or id == 'uly':
            txt = self.hTE.get_text()
            if not len(txt): return
            h = int(txt)
            y = h*rezY
            self.yGE.setValue(abs(y))
            uly = self.ulyGE.getValue()
            lry = uly+y
            self.lryGE.setValue(lry)
        elif id == 'x':
            x = self.xGE.getValue()
            w = int(x/rezX)
            self.wTE.set_text(str(w))
            ulx = self.ulxGE.getValue()
            lrx = ulx+x
            self.lrxGE.setValue(lrx)
        elif id == 'y':
            y = self.yGE.getValue()
            h = int(y/abs(rezY))
            self.hTE.set_text(str(h))
            uly = self.ulyGE.getValue()
            lry = uly-y
            self.lryGE.setValue(lry)

        self.updating = FALSE

    def getInfoFromView(self):
        view = self.viewwin.viewarea
        bbox = view.get_extents()
        w = view.get_width()
        h = view.get_height()
        ulx = bbox[0]
        uly = bbox[3]
        lrx = bbox[2]
        lry = bbox[1]
        dx = abs(ulx - lrx)
        dy = abs(uly - lry)
        self.rezX = dx/w
        self.rezY = -dy/h
        return (ulx,uly,lrx,lry,w,h,dx,dy)

    def getInfoFromLayer(self):
        layer = self.viewwin.viewarea.active_layer()
        if layer is None:
            return
        ds = layer.get_parent().get_dataset()
        w = ds.RasterXSize
        h = ds.RasterYSize
        geoTr = ds.GetGeoTransform()
        ulx = geoTr[0]
        uly = geoTr[3]
        self.rezX = geoTr[1]
        self.rezY = geoTr[5]
        lrx = ulx + w*self.rezX
        lry = uly + h*self.rezY
        dx = abs(ulx - lrx)
        dy = abs(uly - lry)
        return (ulx,uly,lrx,lry,w,h,dx,dy)

    def addLayer(self,*args):
        mapfn = self.checkCache(self.curMap['Name'])
        self.updateMapURL()

        wmsFile = servCaps.getMap(self.curMapURL)
        h = wmsFile.info()
        if h.getheader('Content-Type') == 'application/vnd.ogc.se_xml':
##            wmsFile = file('c:\\FWTools\\wms\\cache\\landsat321_23-exception.xml')
            excepStr = ''
            line = wmsFile.readline()
            while len(line):
                if line.find('<ServiceException code')>0:
                    excepStr += wmsFile.readline()
                line = wmsFile.readline()
            wmsFile.close()
            gvutils.error("Error getting map. Server responded:\n\n"+excepStr)
##            excepFile = open(mapfn+'-exception.xml','wb')
##            excepFile.write(buf)
##            excepFile.close()
            return
            
        layerFile = open(mapfn+'.tmp','wb')
        layerFile.write(wmsFile.read())
        layerFile.close()
        wmsFile.close()

        ds = gdal.Open(mapfn+'.tmp',gdal.GA_ReadOnly)
        if ds is None:
            gvutils.error("Error opening image")
            return

        w = ds.RasterXSize
        h = ds.RasterYSize
        mapVrt = vrtutils.VRTDatasetConstructor(w, h)

        mapVrt.SetSRS(self.srs.ExportToWkt())
        mapVrt.SetGeoTransform(self.getGeoTransform())

        nBands = ds.RasterCount
        fname = ds.GetDescription()
        if nBands == 1:
            band = ds.GetRasterBand(1)
            nodata = band.GetNoDataValue()
            ci = band.GetRasterColorInterpretation()
            dtype = gdal.GetDataTypeName(band.DataType)
            if ci == gdal.GCI_PaletteIndex:
                ct = band.GetRasterColorTable()
                mapVrt.AddSimpleBand(fname,1,dtype,NoDataValue=nodata,ColorInterp='Palette',colortable=ct)
            else:
                mapVrt.AddSimpleBand(fname,1,dtype,NoDataValue=nodata,ColorInterp='Grey')
        else:
            for bandno in range(1,nBands+1):
                band = ds.GetRasterBand(bandno)
                nodata = band.GetNoDataValue()
                dtype = gdal.GetDataTypeName(band.DataType)
                mapVrt.AddSimpleBand(fname,bandno,dtype,NoDataValue=nodata)

        mapFile = open(mapfn+'.vrt','w')
        mapFile.writelines(mapVrt.GetVRTString())
        mapFile.close()

        self.viewwin.open_gdal_dataset(gdal.Open(mapfn+'.vrt'))

    def checkCache(self,mapname):
        count = 1
        filtLst = filter(lambda n:n.startswith(mapname) and n.endswith('vrt'),
                         os.listdir(cachepath))
        inLst = TRUE
        while inLst:
            name = mapname+'_'+str(count)
            if name+'.vrt' in filtLst:
                count+=1
            else:
                inLst = FALSE

        return os.path.join(cachepath,name)

    def setup(self,*args):
        SetupDialog(self)

    def loadMaps(self):
        try:
            maps = pickle.load(open(os.path.join(wms_dir,'maps.dat'),'r'))
        except:
            maps = {'True Color Landsat': {'Name':"landsat321",
                                            'Title':"True Color Landsat",
                                            'Server':'OnEarth',
                                            'URL':"http://wms.jpl.nasa.gov/wms.cgi?VERSION=1.1.1&LAYERS=global_mosaic_base"+ \
                                                    "&STYLES=visual&FORMAT=image%2Fpng&REQUEST=GetMap&SERVICE=WMS" + \
                                                    "&EXCEPTIONS=application%2Fvnd.ogc.se_xml"
                                           }
                    }

        self.maps = maps
        self.mapKeys = self.maps.keys()
        self.mapKeys.sort()

    def setMap(self,mapKey):
        self.updating = TRUE
        self.curMap = self.maps[mapKey]
        srvname = self.curMap['Server']
        if self.curServ is not None:
            if self.curServ == srvname: # don't open if it is already
                self.updating = FALSE
                return
        if openService(srvname):
            self.curServ = srvname
        self.updating = FALSE

    def validateMap(self,*args):
        # will eventually have more checks, only SRS for now
        result = ''
        parms = self.addParms()
        self.updateMapURL(parms)
        check = servCaps.validateURL(self.curMapURL)
        if check is not None:
            result+=check
        elif not servCaps.validateSRS(parms['SRS']):
           result+='Invalid SRS\n'
        if len(result):
            result+='Map is invalid. Verify parameters above.\nURL:'
        else:
            result+='Map is valid.\nLocal file:'
            result+=self.checkCache(self.curMap['Name'])
            result+='\nURL:'

        showValidateMapResult(result,self.curMapURL)

    def addParms(self):
        bbox = []
        parms = {}
        bbox.append(self.ulxGE.get_text())
        bbox.append(self.lryGE.get_text())
        bbox.append(self.lrxGE.get_text())
        bbox.append(self.ulyGE.get_text())
        parms['BBOX'] = bbox
        parms['WIDTH'] = self.wTE.get_text()
        parms['HEIGHT'] = self.hTE.get_text()
        parms['SRS'] = 'EPSG:'+self.epsgTE.get_text()
        color = self.colorBT.get_color()
        if color[3] == 0.0:
            parms['TRANSPARENT'] = 'TRUE'
        else:
            color = int(color[0]*16711425)+int(color[1]*65535)+int(color[2]*255)
            parms['BGCOLOR'] = hex(color)
            parms['TRANSPARENT'] = 'FALSE'
        if 'Extents' in self.curMap:
            for extent,value in self.curMap['Extents'].items():
                if extent in ['time','elevation']:
                    parms[extent] = value
                else:
                    parms['dim_'+extent] = value
        return parms

    def updateMapURL(self,parms=None):
        if parms is None:
            parms = self.addParms()
        self.curMapURL = servCaps.encodeURL(parms,self.curMap['URL']+'&')

    def getGeoTransform(self):
        ulx = self.ulxGE.getValue()
        uly = self.ulyGE.getValue()
        rezX = self.rezX
        rezY = self.rezY
        return [ulx,rezX,0,uly,0,rezY]

    def getSRS(self,epsg=None):
        srs = osr.SpatialReference()
        if epsg is None:
            view = self.viewwin.viewarea
            proj = view.get_projection()
            if proj is not None:
                srs.ImportFromWkt(proj)
                return srs

        try: # in case of epsg not recognised
            srs.ImportFromEPSG(epsg)
        except:
            srs.ImportFromEPSG(4326) # default: WGS84 GEOGCS

        return srs

    def getEPSG(self):
        if self.srs.IsGeographic():
            epsg = self.srs.GetAuthorityCode('GEOGCS')
        else:
            epsg = self.srs.GetAuthorityCode('PROJCS')

        return str(epsg)

    def setResolution(self,entry,id):
        if self.updating:
            return
        if id == 'rezX':
            self.rezX = self.rezxGE.getValue()
            self.updateFromEntry(entry,'w')
            if self.linkTO.active:
                self.rezY = -self.rezX
                self.rezyGE.setValue(self.rezX)
        elif id == 'rezY':
            self.rezY = -self.rezyGE.getValue()
            self.updateFromEntry(entry,'h')

    def close(self,*args):
        self.viewwin.viewarea.disconnect(self.active_changed_id)
        self.viewwin.viewarea.disconnect(self.display_change_id)
        self.destroy()

class SetupDialog(gtk.GtkWindow):
    def __init__(self,mapwin):
        gtk.GtkWindow.__init__(self,title='Setup')
        self.set_policy(FALSE,TRUE,TRUE)
        self.tips = gtk.GtkTooltips()
        self.curServ = None
        self.mapDic = mapwin.maps
        self.mapKeys = mapwin.mapKeys
        self.mapWin = mapwin
        self.curMap = None
        self.updating = TRUE
        self.editingMap = FALSE
        self.editingSrv = FALSE
        self.layerDlg = None
        self.connect('delete-event',self.close)

        gui_OK = self.createGUI()
        if gui_OK is FALSE:
            return None
        else:
            self.updateServiceInfo()
            self.updateMapInfo()
            self.show_all()

        self.updating = FALSE
        self.mapCB.entry.set_text(mapwin.curMap['Title'])

    def createGUI(self):
        mainbox = gtk.GtkVBox(spacing=5)
        mainbox.set_border_width(5)
        self.add(mainbox)

# Maps
        frame = gtk.GtkFrame("Maps")
        mainbox.add(frame, expand=FALSE)
        vbox = gtk.GtkVBox()
        vbox.set_border_width(5)
        frame.add(vbox)
        box = gtk.GtkHBox(spacing=5)
        box.set_border_width(5)
        vbox.add(box, expand=FALSE)
        self.mapCB = gtk.GtkCombo()
        self.mapCB.disable_activate()
        self.mapCB.entry.connect('changed',self.mapSelected)
        box.add(self.mapCB,expand=FALSE)
        box.add(gtk.GtkLabel('Name:'),expand=FALSE)
        self.mapnameTE = gtk.GtkEntry()
        self.mapnameTE.set_usize(100,-1)
        box.add(self.mapnameTE,expand=FALSE)

        delBT = gtk.GtkButton("Del")
        self.tips.set_tip(delBT,'Delete map')
        delBT.connect("clicked", self.delMap)
        box.add(delBT)
        newBT = gtk.GtkButton("New")
        self.tips.set_tip(newBT,'New map')
        newBT.connect("clicked", self.enterMap)
        box.add(newBT)
        self.saveBT = gtk.GtkButton("Save")
        self.tips.set_tip(self.saveBT,'Save map')
        self.saveBT.connect("clicked", self.saveMap)
        box.add(self.saveBT)

        self.selectedCL = gtk.GtkCList(cols=2, titles=['Layer','Style'])
        self.selectedCL.set_column_width(0,270)
        self.selectedCL.set_column_resizeable(0,TRUE)
        self.selectedCL.set_column_resizeable(1,TRUE)
        self.selectedCL.connect('select-row',self.selectedRow)
        swin = gtk.GtkScrolledWindow()
        swin.set_usize(-1,150)
        swin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        swin.add_with_viewport(self.selectedCL)
        vbox.add(swin, expand=FALSE)

# Services
        frame = gtk.GtkFrame("Services")
        mainbox.add(frame, expand=FALSE)
        vbox = gtk.GtkVBox(spacing=5)
        vbox.set_border_width(5)
        frame.add(vbox)
        box = gtk.GtkHBox(spacing=5)
        box.set_border_width(5)
        vbox.add(box, expand=FALSE)
        self.servCB = gtk.GtkCombo()
        self.servCB.set_usize(250,-1)
        self.servCB.disable_activate()
        self.servCB.entry.connect('activate',self.newService)
        self.servCB.entry.connect('changed',self.serviceSelected)
        box.add(self.servCB)

        delBT = gtk.GtkButton("Del")
        self.tips.set_tip(delBT,'Delete service')
        delBT.connect("clicked", self.delService)
        box.add(delBT)
        newBT = gtk.GtkButton("New")
        self.tips.set_tip(newBT,'Add new service')
        newBT.connect("clicked", self.enterService)
        box.add(newBT)
        saveBT = gtk.GtkButton("Save")
        self.tips.set_tip(saveBT,'Save service entry')
        saveBT.connect("clicked", self.saveService)
        box.add(saveBT)

# Service caps
        box = gtk.GtkHBox(spacing=3)
        box.set_border_width(5)
        vbox.add(box, expand=FALSE)
# Image formats
        box.add(gtk.GtkLabel('Format:'),expand=FALSE)
        self.formatCB = gtk.GtkCombo()
        box.add(self.formatCB)
# Exception formats
        box.add(gtk.GtkLabel('Except:'),expand=FALSE)
        self.exceptCB = gtk.GtkCombo()
        self.exceptCB.set_usize(205,-1)
        box.add(self.exceptCB)

# Layers
        lframe = gtk.GtkFrame('Available Layers')
        mainbox.add(lframe)
        lboxfr = gtk.GtkVBox(spacing=5)
        lboxfr.set_border_width(5)
        lframe.add(lboxfr)
        lwin = gtk.GtkScrolledWindow()
        lwin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        lwin.set_usize(-1,300)
        lboxfr.add(lwin)
        self.layersTR = gtk.GtkTree()
        lwin.add_with_viewport(self.layersTR)

# Buttons
        box = gtk.GtkHBox(spacing=5)
        mainbox.add(box, expand=FALSE)

        getBT = gtk.GtkButton("Get map")
        self.tips.set_tip(getBT,'Get map')
        getBT.connect("clicked", self.getMap)
        box.add(getBT)

        validBT = gtk.GtkButton('Validate')
        self.tips.set_tip(validBT,'Validate map')
        validBT.connect('clicked',self.validateMap)
        box.add(validBT)

        cancelBT = gtk.GtkButton("Cancel")
        self.tips.set_tip(cancelBT,'Exit without saving')
        cancelBT.connect("clicked", self.close)
        box.add(cancelBT)

        doneBT = gtk.GtkButton("Done")
        self.tips.set_tip(doneBT,'Save maps and exit')
        doneBT.connect("clicked", self.doneClicked)
        box.add(doneBT)

        return TRUE

    def doneClicked(self,*args):
        self.saveData()
        # update map window before closing
        self.updateMapWindow()
        self.close()

    def selectedRow(self,lst,row,col,event):
        if self.updating:
            return
        
        title = lst.get_text(row,0)
        index = self.curMapParms['LAYERS'].index(title)
        self.showLayerDialog(title,index)

    def layerItemSelected(self,item,event):
        self.updating = TRUE
        title = item.children()[0].get()
        if event.button == 3:
            item.toggle()
            self.showLayerDialog(title)
        elif event.button == 1:
            self.selectLayer(title)
            self.updateSelectedGUI()
            if self.layerDlg is not None:
                if self.layerDlg.flags() & gtk.VISIBLE:
                    self.showLayerDialog(title)

        self.updating = FALSE

    def showLayerDialog(self,title,index=None):
        if self.checkMap() and index is None:
            if title in self.curMapParms['LAYERS']:
                index = self.curMapParms['LAYERS'].index(title)

        if self.layerDlg is None:
            self.layerDlg = LayerDialog(title,self.curMapParms,index)
            self.layerDlg.subscribe('param-changed',self.updateSelectedGUI)
        else:
            self.layerDlg.get_window()._raise()
            self.layerDlg.create(title,self.curMapParms,index)
        
    def updateServiceInfo(self):
        self.updating = TRUE
        servKeys = servDic.keys()
        servKeys.sort()
        self.servCB.set_popdown_strings(servKeys)
        self.updating = FALSE

    def updateMapInfo(self):
        self.updating = TRUE
        self.mapKeys = self.mapDic.keys()
        self.mapKeys.sort()
        self.mapCB.set_popdown_strings(self.mapKeys)
        self.updating = FALSE

    def updateMapGUI(self):
        self.formatCB.entry.set_text(self.curMapParms['FORMAT'])
        self.exceptCB.entry.set_text(self.curMapParms['EXCEPTIONS'])

    def updateMapWindow(self):
        self.mapWin.updating = TRUE
        self.mapWin.mapKeys = self.mapKeys
        self.mapWin.maps = self.mapDic
        self.mapWin.mapCB.set_popdown_strings(self.mapWin.mapKeys)
        self.mapWin.mapCB.entry.set_text(self.curMap['Title'])
        self.mapWin.setMap(self.curMap['Title'])
        self.mapWin.updating = FALSE

    def mapSelected(self,*args):
        if self.updating or self.editingMap:
            return
        key = self.mapCB.entry.get_text()
        self.setMap(key)

    def setMap(self,key):
        self.updating = TRUE
        self.curMap = self.mapDic[key]
        self.mapnameTE.set_text(self.curMap['Name'])
        skey = self.curMap['Server']
        self.servCB.entry.set_text(skey)
        self.setService(skey)
        self.curMapParms = servCaps.decodeURL(self.curMap['URL'])
        if 'Extents' in self.curMap:
            self.curMapParms['Extents'] = self.curMap['Extents']

        self.updateMapGUI()
        self.updateSelectedGUI()
        self.updating = FALSE
        if self.layerDlg is not None:
            if self.layerDlg.flags() & gtk.VISIBLE:
                self.selectedCL.select_row(0,0)

    def checkMap(self):
        return self.curMap['Server'] == self.curServ \
               and not self.curMap['Server'] == 'None'

    def validateMap(self,*args):
        if self.checkMap():
            exmap = self.mapWin.curMap
            self.mapWin.curMap = self.makeMap()
            self.mapWin.validateMap()
            self.mapWin.curMap = exmap

    def enterMap(self,*args):
        self.updating = TRUE
        self.editingMap = TRUE
        self.mapCB.entry.set_text('New map')
        self.mapnameTE.set_text('newmap')
        self.servCB.entry.set_text('Select service')
        self.newMap()
        self.updateSelectedGUI()
        self.updating = FALSE

    def newMap(self):
        self.setService('Select service')
        map = {}
        parms = {}
        parms['SERVICE'] = 'WMS'
        parms['REQUEST'] = "GetMap"
        parms['LAYERS'] = []
        parms['STYLES'] = []
        map['Name'] = 'newmap'
        map['Title'] = 'New map'
        map['Server'] = 'None'
        self.curMap = map
        self.curMapParms = parms

    def saveMap(self,*args):
        self.updating = TRUE
        map = self.makeMap()
        if 'Extents' in self.curMapParms:
            map['Extents'] = self.curMapParms.get('Extents')
            del self.curMapParms['Extents']
        map['URL'] = servCaps.encodeURL(self.curMapParms)
        mapKey = map['Title']
        self.mapDic[mapKey] = map
        self.updateMapInfo()
        self.mapCB.entry.set_text(mapKey)
        self.setMap(mapKey)
        self.updateMapWindow()
        self.updating = FALSE
        self.editingMap = FALSE

    def delMap(self,*args):
        self.updating = TRUE
        del self.mapDic[self.curMap['Title']]
        self.updateMapInfo()
        self.setMap(self.mapKeys[0])
        self.updateMapWindow()
        self.updating = FALSE

    def getMap(self,*args):
        self.mapWin.curMap = self.makeMap()
        self.mapWin.addLayer()

    def makeMap(self):
        map = {}
        map['Title'] = self.mapCB.entry.get_text()
        map['Name'] = self.mapnameTE.get_text()
        map['Server'] = self.servCB.entry.get_text()
        self.curMapParms['FORMAT'] = self.formatCB.entry.get_text()
        self.curMapParms['EXCEPTIONS'] = self.exceptCB.entry.get_text()
        if 'Extents' in self.curMapParms:
            map['Extents'] = self.curMapParms['Extents']
        params = self.curMapParms.copy()
        map['URL'] = servCaps.encodeURL(params)

        return map

    def serviceSelected(self,*args):
        if self.updating or self.editingSrv:
            return
        skey = self.servCB.entry.get_text()
        self.setService(skey)
        if not self.curMap['Title'] in self.mapDic:
            self.curMapParms['EXCEPTIONS'] = self.exceptCB.entry.get_text()
            self.curMapParms['FORMAT'] = self.formatCB.entry.get_text()
            self.curMapParms['VERSION'] = servCaps.version
            self.curMap['Server'] = skey
            self.curMap['URL'] = servCaps.encodeURL(self.curMapParms)
            if servCaps.layer.find('Dimension') is not None:
                self.curMapParms['Extents'] = {}

    def setService(self,skey):
        self.updating = TRUE
        if skey == 'Select service':
            self.updateServiceGUI(skey)
            self.curServ = None
            self.updating = FALSE
            return
        if skey != self.curServ:
            if openService(skey):
                self.curServ = skey
                self.updateServiceGUI(skey)
                self.updateLayersList()

        self.updating = FALSE

    def enterService(self,*args):
        self.updating = TRUE
        self.editingSrv = TRUE
        self.servCB.entry.set_text('')
        self.tips.set_tip(self.servCB.entry,'Enter service filename/url and hit <Return>')
        self.updateServiceGUI('New service')
        self.updating = FALSE

    def newService(self,cb):
        self.updating = TRUE
        pathname = cb.get_text()
        fname = None
        type,p = urllib.splittype(pathname)
        if type is None:
            fname = pathname
            url = os.path.join(wms_dir,pathname)
        else:
            url = pathname

        if not servCaps.open(url):
            txt = 'Could not open ' + url+'.\nServer responded:\n'
            txt+=servCaps.buffer
            message(txt,title='GetCapabilities Result')
            del servCaps.buffer
            servCaps.buffer = None
            self.updating = FALSE
            self.editingSrv = FALSE
            return

        self.curServ = servCaps.title
        self.servCB.entry.set_text(servCaps.title)
        self.updateServiceGUI(self.curServ)
        self.updateLayersList()
        self.updating = FALSE

    def delService(self,*args):
        self.updating = TRUE
        srvname = self.servCB.entry.get_text()
        host = servDic.get(srvname)
        del servDic[srvname]
        os.remove(os.path.join(srv_dir,host,srvname+'.xml'))
        self.updateServiceInfo()
        self.updating = FALSE

    def saveService(self,*args):
        self.updating = TRUE
        srvKey = self.servCB.entry.get_text()
        try:
            host = createCapsEntry(srvKey)
            servDic[srvKey] = host
            self.updateServiceInfo()
        except:
            outfile = os.path.join(wms_dir,'caps-tmp.xml')
            fd = file(outfile,'w')
            fd.write(servCaps.buffer)
            fd.close()
            gvutils.error('The Service entry could not be created.\nSaved as '+outfile)
            srvKey = servDic.keys()[0]
        
        del servCaps.buffer
        servCaps.buffer = None
        self.editingSrv = FALSE
        self.updating = FALSE
        self.servCB.entry.set_text(srvKey)

    def updateServiceGUI(self,key):
        if key == 'Select service' or key == 'New service':
            self.formatCB.entry.set_text('')
            self.exceptCB.entry.set_text('')
            if key == 'Select service':
                self.tips.set_tip(self.servCB.entry,'Select the service for this map. \n Only one service per map.')
            self.layersTR.clear_items(0,-1)
            if key == 'New service':
                self.selectedCL.freeze()
                self.selectedCL.clear()
                self.selectedCL.thaw()
            return

        frmtLst = servCaps.getPropList('Capability/Request/GetMap/Format')
        self.formatCB.set_popdown_strings(frmtLst)
        excLst = servCaps.getPropList('Capability/Exception/Format')
        self.exceptCB.set_popdown_strings(excLst)

        try:
            self.tips.set_tip(self.servCB.entry,servCaps.abstract.encode('latin_1'))
        except:
            self.tips.set_tip(self.servCB.entry,servCaps.title)

    def updateLayersList(self):
        self.layersTR.clear_items(0,-1)
        item = gtk.GtkTreeItem(servCaps.layer.title)
        self.layersTR.append(item)
        mainTree = gtk.GtkTree()
        item.set_subtree(mainTree)
        item.connect('button-press-event',self.layerItemSelected)
        self.addLayerTree(servCaps.layer,mainTree)
        item.expand()
        item.show()

    def updateSelectedGUI(self,*args):
        self.updating = TRUE
        self.selectedCL.freeze()
        self.selectedCL.clear()
        for laytitle in self.curMapParms['LAYERS']:
            if len(self.curMapParms['STYLES']):
                idx = self.curMapParms['LAYERS'].index(laytitle)
                stitle = self.curMapParms['STYLES'][idx]
            self.selectedCL.insert(0,(laytitle,stitle))
        self.selectedCL.thaw()
        self.updating = FALSE

    def addLayerTree(self,laynode,tree):
        for node in servCaps.sortLayerTree(laynode):
            layItem = gtk.GtkTreeItem(node.findtext('Title'))
            tree.append(layItem)
            if node.find('Layer'):
                layTree = gtk.GtkTree()
                layItem.set_subtree(layTree)
                layItem.connect('expand',self.expandLayerTree,node)

            layItem.connect('button-press-event',self.layerItemSelected)
            layItem.show()


    def expandLayerTree(self,item,node):
        tree = item.subtree
        if len(tree.children()):
            return
        self.addLayerTree(node,tree)

    def selectLayer(self,title):
        if not self.checkMap():
            return
        layerNode = servCaps.getLayerNode(title)
        if layerNode.find('Name') is None:
            return
        if title in self.curMapParms['LAYERS']:
            index = self.curMapParms['LAYERS'].index(title)
            del self.curMapParms['LAYERS'][index]
            del self.curMapParms['STYLES'][index]
            if 'Extents' in self.curMapParms and len(self.curMapParms['LAYERS']) == 0:
                self.curMapParms['Extents'] = {}
        else:
            self.curMapParms['LAYERS'].append(title)
            styleNode = layerNode.find('Style')
            if styleNode:
                style = styleNode.findtext('Title')
            else:
                style = ''
            self.curMapParms['STYLES'].append(style)
            if layerNode.find('Extent') is not None:
                extents = layerNode.findall('Extent')
                for extent in extents:
                    self.curMapParms['Extents'][extent.get('name')] = extent.get('default')

    def saveData(self,*args):
        pickle.dump(self.mapDic,open(os.path.join(wms_dir,'maps.dat'),'w'))

    def close(self,*args):
        if self.layerDlg is not None:
            self.layerDlg.unsubscribe('param-changed',self.updateSelectedGUI)
            self.layerDlg.destroy()

        self.destroy()


class LayerDialog(gtk.GtkWindow,gvsignaler.Signaler):
    def __init__(self,title,params,index=None):
        gtk.GtkWindow.__init__(self,title='Layer Properties')
        self.set_policy(FALSE,TRUE,TRUE)
        self.connect('delete-event',self.close)
        self.publish('param-changed')
        self.create(title,params,index)

    def create(self,title,params,index=None):
        self.updating = TRUE
        self.layerNode = servCaps.getLayerNode(title)
        self.params = params
        self.index = index
        self.curStyle = None
        self.extentDic = {}
        if len(self.children()):
            for child in self.children():
                child.destroy()
        self.createGUI()
        self.show_all()
        self.updating = FALSE

    def createGUI(self):
        srsflag = TRUE
        mainbox = gtk.GtkVBox(spacing=5)
        mainbox.set_border_width(5)
        self.add(mainbox)
        frame = gtk.GtkFrame("Information")
        mainbox.add(frame)
        vbox = gtk.GtkVBox(spacing=3)
        vbox.set_border_width(5)
        frame.add(vbox)
        if self.layerNode.find('Name') is not None:
            self.selectedTO = gtk.GtkCheckButton(label='Selected')
            vbox.add(self.selectedTO,expand=FALSE)
            if self.index is not None:
                self.selectedTO.set_active(TRUE)
            self.selectedTO.connect('toggled',self.selectedToggled)
        for node in self.layerNode.getiterator():
            tag = node.tag
            if tag in ['Name','Title']:
                box = gtk.GtkHBox()
                vbox.add(box)
                box.add(gtk.GtkLabel(tag+': '+node.text),expand=FALSE)
            elif tag == 'Abstract':
                box = gtk.GtkHBox()
                vbox.add(box)
                label = gtk.GtkLabel(node.text)
                label.set_justify(gtk.JUSTIFY_FILL)
                label.set_line_wrap(TRUE)
                label.set_usize(400,-1)
                box.add(label)
            elif tag == 'SRS' and srsflag:
                srsLst = servCaps.getSRSList(self.layerNode)
                vbox.add(gtk.GtkHSeparator())
                box = gtk.GtkHBox(spacing=3)
                vbox.add(box)
                box.add(gtk.GtkLabel('SRS:'),expand=FALSE)
                srsCB = gtk.GtkCombo()
                srsCB.set_usize(110,-1)
                srsCB.set_popdown_strings(srsLst)
                tips = gtk.GtkTooltips()
                tips.set_tip(srsCB.entry,'For information only. Not selectable')
                box.add(srsCB,expand=FALSE)
                srsflag = FALSE
            elif tag in ['LatLonBoundingBox','BoundingBox']:
                vbox.add(self.createBBoxLabel(node),expand=FALSE)
            elif tag in ['Dimension','ScaleHint','MetadataURL','DataURL', \
                         'KeywordList','Attribution','AuthorityURL','Identifier','FeatureListURL']:
                vbox.add(self.createAttrLabel(node),expand=FALSE)

        vbox.add(self.createAttrLabel(self.layerNode))
        if self.layerNode.find('Style') is not None:
            mainbox.add(self.createStylesGUI())
        if self.layerNode.find('Extent') is not None:
            mainbox.add(self.createExtentGUI())

    def createStylesGUI(self):
        frame = gtk.GtkFrame("Style")
        vbox = gtk.GtkVBox(spacing=5)
        vbox.set_border_width(5)
        frame.add(vbox)
        box = gtk.GtkHBox(spacing=5)
        vbox.add(box, expand=FALSE)
        self.stylesCB = gtk.GtkCombo()
        box.add(self.stylesCB)

        styleTree = self.layerNode.findall('Style')
        styleLst = servCaps.getTitles(styleTree)
        self.stylesCB.set_popdown_strings(styleLst)
        self.styleTX = gtk.GtkLabel()
        vbox.add(self.styleTX,expand=FALSE)
        if self.index is None:
            self.setStyle(styleLst[0])
        else:
            self.setStyle(self.params['STYLES'][self.index])
        self.stylesCB.entry.set_text(self.curStyle)
        self.stylesCB.entry.connect('changed',self.styleChanged)

        legend = self.getStyle(self.curStyle).find('LegendURL')
        if legend:
            vbox.add(gtk.GtkLabel(legend.tag+'...'),expand=FALSE)
        return frame

    def createExtentGUI(self):
        extentTree = self.layerNode.findall('Extent')
        frame = gtk.GtkFrame("Extent")
        vbox = gtk.GtkVBox(spacing=3)
        vbox.set_border_width(5)
        frame.add(vbox)
        for extent in extentTree:
            extentTE = ExtentEntry(extent)
            vbox.add(extentTE,expand=FALSE)
            name = extent.get('name')
            extentTE.connect('changed',self.extentChanged,name)
            self.extentDic[name] = extentTE.entry
            if self.index is not None:
                extentTE.entry.set_text(self.params['Extents'][name])
        return frame

    def createBBoxLabel(self,elem):
        vbox = gtk.GtkVBox(spacing=3)
        vbox.add(gtk.GtkHSeparator())
        if elem.tag == 'BoundingBox':
            vbox.add(gtk.GtkLabel(elem.tag+' '+elem.get('SRS')),expand=FALSE)
        else:
            vbox.add(gtk.GtkLabel(elem.tag),expand=FALSE)
        label = gtk.GtkLabel('maxy'+':'+elem.get('maxy'))
        vbox.add(label,expand=FALSE)
        box = gtk.GtkHBox(spacing=10)
        vbox.add(box)
        lbox = gtk.GtkHBox()
        box.add(lbox)
        rbox = gtk.GtkHBox()
        box.add(rbox)
        label = gtk.GtkLabel('minx'+':'+elem.get('minx'))
        label.set_justify(gtk.JUSTIFY_LEFT)
        lbox.add(label)
        label = gtk.GtkLabel('maxx'+':'+elem.get('maxx'))
        label.set_justify(gtk.JUSTIFY_RIGHT)
        rbox.add(label)
        label = gtk.GtkLabel('miny'+':'+elem.get('miny'))
        vbox.add(label,expand=FALSE)
        return vbox

    def createAttrLabel(self,elem):
        tag = elem.tag
        vbox = gtk.GtkVBox(spacing=3)
        if len(elem.items()) == 0 and tag == 'Layer':
            return vbox
        vbox.add(gtk.GtkHSeparator())
        if tag in ['DataURL','MetadataURL','KeywordList','Attribution','AuthorityURL','Identifier','FeatureListURL']:
            vbox.add(gtk.GtkLabel(tag+'...'),expand=FALSE)
            return vbox
        vbox.add(gtk.GtkLabel(tag),expand=FALSE)
        for attr,value in elem.items():
            box = gtk.GtkHBox()
            vbox.add(box,expand=FALSE)
            label = gtk.GtkLabel(attr+': '+value)
            box.add(label,expand=FALSE)
        return vbox

    def selectedToggled(self,chk):
        if self.updating:
            return
        self.selectLayer(chk.active)

    def selectLayer(self,select):
        title = self.layerNode.findtext('Title')
        if select:
            self.params['LAYERS'].append(title)
            if self.curStyle is None:
                style = ''
            else:
                style = self.curStyle
            self.params['STYLES'].append(style)
            if 'Extents' in self.params:
                for extent,entry in self.extentDic.items():
                    self.params['Extents'][extent] = entry.get_text()
            self.index = self.params['LAYERS'].index(title)
        else:
            del self.params['LAYERS'][self.index]
            del self.params['STYLES'][self.index]
            if 'Extents' in self.params and len(self.params['LAYERS']) == 0:
                self.params['Extents'] = {}
            self.index = None

        self.notify('param-changed')

    def styleChanged(self,entry):
        if self.updating:
            return
        sel = entry.get_text()
        if len(sel):
            self.setStyle(sel)
    
    def extentChanged(self,entry,name):
        if self.updating:
            return
        sel = entry.get_text()
        if len(sel):
            self.params['Extents'][name] = sel

    def setStyle(self,title):
        self.curStyle = title
        if self.index is not None:
            self.params['STYLES'][self.index] = title
            self.notify('param-changed')

        self.updateStyleGUI()

    def getStyle(self,title):
        for style in self.layerNode.findall('Style'):
            if style.findtext('Title') == title:
                return style

    def updateStyleGUI(self):
        style = self.getStyle(self.curStyle)
        abstract = style.find('Abstract')
        if abstract is not None:
            self.styleTX.set_text(abstract.text)

    def close(self,*args):
        self.updating = TRUE
        self.hide()
        return TRUE

# custom widgets and dialogs
class GeneralDialog(gtk.GtkDialog):
    def __init__(self, widgets=[],buttons=[]):
        gtk.GtkDialog.__init__(self)
        self.connect("destroy", self.quit)
        self.connect("delete_event", self.quit)
        gtk.grab_add(self)
        for widget in widgets:
            hbox = gtk.GtkHBox()
            hbox.set_border_width(3)
            self.vbox.add(hbox)
            hbox.add(widget)

        for button in buttons:
            self.action_area.add(button)

        button = gtk.GtkButton('Close')
        self.action_area.add(button,expand=FALSE)
        button.connect("clicked", self.quit)

    def quit(self, *args):
        self.hide()
        self.destroy()
        gtk.mainquit()

def message(text,title="Message Box"):
    label = gtk.GtkLabel(text)
    label.set_justify(gtk.JUSTIFY_LEFT)
    label.set_line_wrap(TRUE)
    win = GeneralDialog(widgets=[label])
    win.set_title(title)
    win.show_all()
    gtk.mainloop()

def showValidateMapResult(result,url):
    label = gtk.GtkLabel(result)
    label.set_justify(gtk.JUSTIFY_LEFT)

    # just a trick to get the text length
    urltxt = gtk.GtkLabel(url)
    w,h = urltxt.size_request()

    urlTE = gtk.GtkEntry()
    urlTE.set_usize(w+10,-1)
    urlTE.set_text(url)
    urlwin = gtk.GtkScrolledWindow()
    urlwin.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
    urlwin.set_usize(-1,50)
    urlwin.add_with_viewport(urlTE)
    win = GeneralDialog(widgets=[label,urlwin])
    win.set_title('Map Validation')
    win.show_all()
    # do this last, just in case...
    urlTE.select_region(0,-1)
    urlTE.copy_clipboard()
    gtk.mainloop()

class GeoEntry(gtk.GtkHBox):
    def __init__(self,geo,dgsz=33,mnsz=22,scsz=40,mtsz=125):
        gtk.GtkHBox.__init__(self,spacing=3)
        self.degsz = dgsz
        self.metsz = mtsz
        self.minsz = mnsz
        self.secsz = scsz
        self.round = 2
        self.setMode(geo)

    def connect(self,signal,callback,data):
        if self.isGeo:
            self.degTE.connect(signal,callback,data)
            self.minTE.connect(signal,callback,data)
            self.secTE.connect(signal,callback,data)
        else:
            self.metersTE.connect(signal,callback,data)

    def setRound(self,value):
        self.round = value

    def setGeoMode(self):
        self.degTE = self.createEntry(self.degsz,'d')
        self.minTE = self.createEntry(self.minsz,'m')
        self.secTE = self.createEntry(self.secsz,'s')
        self.isGeo = TRUE

    def setMode(self,geo):
        if len(self.children()):
            for child in self.children():
                child.destroy()

        if geo:
            self.setGeoMode()
        else:
            self.setProjMode()

        self.show_all()

    def setProjMode(self):
        self.metersTE = self.createEntry(self.metsz,'m')
        self.isGeo = FALSE

    def createEntry(self,size,lbl):
        te = gtk.GtkEntry()
        te.set_usize(size,-1)
        self.add(te,expand=FALSE)
        self.add(gtk.GtkLabel(lbl),expand=FALSE)
        return te

    def getDegrees(self):
        txt = self.degTE.get_text()
        return self.validateInt(txt)

    def getMinutes(self):
        txt = self.minTE.get_text()
        return self.validateInt(txt)

    def getSeconds(self):
        txt = self.secTE.get_text()
        return self.validateFloat(txt)

    def getMeters(self):
        txt = self.metersTE.get_text()
        return self.validateFloat(txt)

    def validateInt(self,txt):
        if len(txt) and txt != '-':
            value = int(txt)
        else:
            value = 0

        return value

    def validateFloat(self,txt):
        if len(txt) and txt != '-':
            value = float(txt)
        else:
            value = 0.0

        return value

    def setDegrees(self,value):
        self.degTE.set_text(str(value))

    def setMinutes(self,value):
        self.minTE.set_text(str(value))

    def setSeconds(self,value):
        self.secTE.set_text(str(round(value,self.round)))

    def setMeters(self,value):
        self.metersTE.set_text(str(value))

    def setValue(self,value):
        if self.isGeo:
            dms = self.deg2dms(value)
            self.setDegrees(dms[0])
            self.setMinutes(dms[1])
            self.setSeconds(dms[2])
        else:
            self.setMeters(value)

    def set_text(self,txt):
        self.setValue(float(txt))

    def getValue(self):
        dms = []
        if self.isGeo:
            dms.append(self.getDegrees())
            dms.append(self.getMinutes())
            dms.append(self.getSeconds())
            return self.dms2deg(dms)
        else:
            return self.getMeters()

    def get_text(self):
        value = self.getValue()
        return str(value)

    def deg2dms(self,dd):
        deg = int(dd)
        dec = abs(dd-deg)
        mn = int(dec*60)
        sec = (dec*60 - mn)*60
        if round(sec,self.round) >= 60.0:
            sec = 0.0
            mn+=1
        return (deg,mn,sec)

    def dms2deg(self,dms):
        dd = abs(dms[0])+dms[1]/60.0+dms[2]/3600.0
        if dms[0] < 0:
            return -dd
        else:
            return dd

class ExtentEntry(gtk.GtkHBox):
    def __init__(self,extent):
        gtk.GtkHBox.__init__(self,spacing=3)
        name = extent.get('name')
        label = gtk.GtkLabel(name+': ')
        self.add(label,expand=FALSE)
        extLst = extent.text.split(',')
        if len(extLst) > 1:
            extentCB = gtk.GtkCombo()
            extentCB.entry.set_usize(75,-1)
            self.add(extentCB,expand=FALSE)
            extentCB.set_popdown_strings(extLst)
            extentCB.entry.set_text(extent.get('default'))
            self.entry = extentCB.entry
            dimTree = servCaps.layer.findall('Dimension')
            for elem in dimTree:
                if elem.get('name') == name:
                    units = elem.get('unitSymbol')
                    break
            if units is not None:
                self.add(gtk.GtkLabel(units),expand=FALSE)
        else:
            extLst = extent.text.split('/')
            if len(extLst) == 1:
                label = gtk.GtkLabel(extent.text)
                self.add(label,expand=FALSE)
                self.entry = label
            else:
                extentTE = gtk.GtkEntry()
                extentTE.set_text(extent.get('default'))
                extentTE.set_usize(75,-1)
                self.add(extentTE,expand=FALSE)
                self.entry = extentTE
                label = ' from '+extLst[0]+' to '+extLst[1]+' by '+extLst[2][1:]
                self.add(gtk.GtkLabel(label),expand=FALSE)

    def connect(self,signal,callback,data):
        self.entry.connect(signal,callback,data)

TOOL_LIST = ['WMSTool']
if __name__ == '__main__':
    import sys
    if not os.path.exists(wms_dir):
        os.mkdir(wms_dir)
    if not os.path.exists(cachepath):
        os.mkdir(cachepath)
    if not os.path.exists(srv_dir):
        os.mkdir(srv_dir)
    
    if len(sys.argv)>1:
        intxt = file(sys.argv[1],'r').read()
        lst = intxt.splitlines()
    else:
        lst = ['OnEarth,http://wms.jpl.nasa.gov/wms.cgi?','GLOBE,http://globe.digitalearth.gov/viz-bin/wmt.cgi?']

    if len(sys.argv)>2:
        srvDir = os.path.join(wms_dir,sys.argv[2])
    else:
        srvDir = srv_dir
    if not os.path.exists(srvDir):
        os.mkdir(srvDir)

    print "Processing list..."
    buildServicesDir(lst,srvDir)
    sys.exit(0)
