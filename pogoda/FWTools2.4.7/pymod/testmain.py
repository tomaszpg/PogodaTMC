#!/usr/bin/env python
import gtk, gtkmissing, gview
import layerdlg

def create_view(name, plines, areas, raster):
    win = gtk.GtkWindow()
    win.set_title(name)
    win.set_policy(gtk.TRUE, gtk.TRUE, gtk.FALSE)

    shell = gtk.GtkVBox()
    win.add(shell)
    
    view = gview.GvViewArea()
    view.size(512,512)
    shell.pack_start(view, expand=gtk.TRUE)
    
    if raster:
        raster_layer = gview.GvRasterLayer(raster)
        view.add_layer(raster_layer)
    view.add_layer(gview.GvPqueryLayer())
    view.add_layer(gview.GvAreaLayer(areas))
    view.add_layer(gview.GvLineLayer(plines))

    statusbar = gtk.GtkHBox()
    shell.pack_start(statusbar, expand=gtk.FALSE)
    label = gtk.GtkLabel()
    statusbar.pack_start(label, expand=gtk.FALSE, padding=3)
    tracker = gview.GvTrackTool(label)
    tracker.activate(view)

    view.connect('key-press-event', testmain_button_press)
    
    win.show_all()
    view.grab_focus()
    win.connect('delete-event', gtk.mainquit)
    gtk.quit_add_destroy(1, win)
    return view

def testmain_button_press(view, event, *args):
    global last_group
    
    if event.string == 'g':
        last_group = gview.undo_start_group();
        
    if event.string == 'e':
        gview.undo_end_group(last_group);

    if event.string == 'p':
        view.print_to_file( 425, 550, "out.tif", "GTiff" )
        view.print_postscript_to_file( 425, 550, 1, "out.ps" )

class Toolbar(gtk.GtkWindow):
    def __init__(self):
        gtk.GtkWindow.__init__(self)

        toolbox = gview.GvToolbox()        
        toolbox.add_tool("select", gview.GvSelectionTool())
        toolbox.add_tool("line", gview.GvLineTool())
        toolbox.add_tool("area", gview.GvAreaTool())
        toolbox.add_tool("node", gview.GvNodeTool())
        toolbox.add_tool("point", gview.GvPointTool())
        toolbox.add_tool("roi", gview.GvRoiTool())
        
        toolbar = gtk.GtkToolbar(gtk.ORIENTATION_VERTICAL, gtk.TOOLBAR_TEXT)
        self.add(toolbar)
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, None,
                                     'Select', 'Selection tool',
                                     None, None, self.toggle, "select")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Query Pnt', 'Query point marking tool',
                                     None, None, self.toggle, "point")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Draw Line', 'Line drawing tool',
                                     None, None, self.toggle, "line")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Draw Area', 'Area drawing tool',
                                     None, None, self.toggle, "area")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Edit Node', 'Node edit tool',
                                     None, None, self.toggle, "node")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Draw ROI', 'ROI drawing tool',
                                     None, None, self.toggle, "roi")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_TOGGLEBUTTON, None,
                                     'Link Views', 'Link views together',
                                     None, None, self.link)
        
        self.connect('delete-event', gtk.mainquit)
        toolbar.show()
        self.show()
        self.toolbox = toolbox
        self.toolbar = toolbar
        self.link = gview.GvViewLink()
        
    def toggle(self, but, data):
        self.toolbox.activate_tool(data)
        
    def link(self, but):
        but = gtk.GtkToggleButton(_obj=but)
        if (but.active):
            self.link.enable()
        else:
            self.link.disable()
    def add_view(self, view):
        self.toolbox.activate(view)
        self.link.register_view(view)

def setup(numwin, fname=None):
    plines = gview.GvPolylines()
    plines.set_name("Some lines")
    gview.undo_register(plines)

    areas = gview.GvAreas()
    areas.set_name("Some areas")
    gview.undo_register(areas)

    if fname:
        raster = gview.GvRaster(fname,sample=gview.SMAverage)
        raster.set_name(fname)
    else:
        raster = None
            
    toolbar = Toolbar()
    ldlg = layerdlg.LayerDlg()
    ldlg.connect('destroy', gtk.mainquit)
    ldlg.show()

    for i in range(numwin):
        name = 'View %d' % (i+1)
        view = create_view(name, plines, areas, raster)
        toolbar.add_view(view)
        ldlg.add_view(name, view)

if __name__ == '__main__':
    try:
        import sys
        numwin = eval(sys.argv[1])
    except:
        numwin = 1
    if len(sys.argv) > 2:
        raster = sys.argv[2]
    else:
        raster = None
    setup(numwin, raster)
    gtk.mainloop()
