import gtk

class pguEntry( gtk.GtkEntry ):

    def __init__(self):
        gtk.GtkEntry.__init__(self)
        self.add_events(gtk.GDK.FOCUS_CHANGE_MASK)
        self.connect('focus-out-event', self.cleanup)

    def cleanup(self, *args):
        self.select_region(0, 0)
        self.queue_draw()
