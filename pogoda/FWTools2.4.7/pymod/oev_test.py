
import gview
import GDK

print 'Loaded oev_test.py'

def key_press_cb( viewarea, event, *args ):

    if event.keyval == GDK.F3:
        app = gview.app
        roi = app.toolbar.get_roi()
        print roi

    if event.keyval == GDK.F4:
        view = gview.app.view_manager.get_active_view()
        shapes = view.active_layer().get_parent()

        for shp_index in range(len(shapes)):
            shape = shapes[shp_index]
            if shape is None:
                continue

            shape = shape.copy()
            shape._gv_ogrfs = 'SYMBOL(c:#FF0000,id:"ogr-sym-1",a:45)'
            shapes[shp_index] = shape

    if event.keyval == GDK.F5:
        import _gv

        file = 'e:/data/sdts/safe_dem/7096CATD.DDF'

        options = []
        options.append(('mesh_lod', '4'))
        
        view = gview.app.view_manager.get_active_view()

        rasterds = gview.manager.get_dataset(file)
        raster = gview.manager.get_dataset_raster( rasterds, 1)
        raster_layer = gview.GvRasterLayer(raster, options)
        raster_layer.add_height(raster)
        view.add_layer(raster_layer)
        view.set_active_layer(raster_layer)
        
        shapes = gview.GvShapes( _obj = _gv.gv_build_skirt( raster._o ) )

        layer = gview.GvShapesLayer( shapes )
        view.add_layer(layer)
        view.set_active_layer(layer)
        
    if event.keyval == GDK.F6:
        view = gview.app.view_manager.get_active_view()
        layer = gview.AppCurLayer()
        view.add_layer(layer)
        view.set_active_layer(layer)

    if event.keyval == GDK.F8:
        import gvgrass

        gvgrass.UpdateMenu( gview.app.view_manager.get_active_view_window() )
        
    if event.keyval == GDK.F9:
        view = gview.app.view_manager.get_active_view()
        view.active_layer().set_property( '_gv_ogrfs',
                                          'SYMBOL(c:#FF0000,id:"ogr-sym-7");'
                                          'LABEL(f:"Fixed",c:#FF00FF,t:{MOTHER})' )
        view.active_layer().display_change()

    if event.keyval == GDK.F10:
        view = gview.app.view_manager.get_active_view()
        shapes = view.active_layer().get_parent()

        for shp_index in range(len(shapes)):
            shape = shapes[shp_index]
            if shape is None:
                continue

            shape = shape.copy()
            
            shape._gv_ogrfs = 'LABEL(c:#FF0000,t:{MOTHER})'
            shapes[shp_index] = shape

    if event.keyval == GDK.F11:
        view = gview.app.view_manager.get_active_view()
        shapes = view.active_layer().get_parent()
        raster = gview.manager.get_dataset_raster( \
            gview.manager.get_dataset( 'final_dem.tif' ), 1 )

        shapes.add_height( raster, 15 )

view = gview.app.view_manager.get_active_view()
view.connect('key-press-event', key_press_cb)




