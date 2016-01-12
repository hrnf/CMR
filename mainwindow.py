from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
from styleconstants import StyleConstants
import os
import io

import cairo

class MainWindow(Gtk.Window):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("mainwindow.glade")
        window = builder.get_object("mainwindow")
        window.show_all()

        drawingarea = builder.get_object("catalogue")
        drawingarea.connect("draw", self.draw_callback, drawingarea)

        Gtk.main()

    def draw_callback (self, widget, cr, da):
        image = self.load_image()
        Gdk.cairo_set_source_pixbuf(cr, image, 0, 0)
        cr.rectangle(0, 0, image.get_width(), image.get_height())
        cr.fill()
        widget.queue_draw_area(0, 0, image.get_width(),image.get_height())
        da.set_size_request(image.get_width(),image.get_height())

        return True

    def load_image(self):
        image = GdkPixbuf.Pixbuf.new_from_file_at_size("sample-cover.jpg",
            StyleConstants.CATALOGUE_IMAGE_SIZE[0],
            StyleConstants.CATALOGUE_IMAGE_SIZE[1])
        return image

    def make_list():
        releasesdir = os.path.expanduser("~/.CMR/releases")
        metadata = []

        os.remove(releasesdir+"/list")

        for subdirname in os.listdir(releasesdir):
            try:
                with open(releasesdir+"/"+subdirname+"/"+"data") as datafile:
                    data = datafile.read()
                    metadata.append("|//" + subdirname)
                    metadata.append(data+"\n")
            except:
                pass

        listfile = open(releasesdir+"/list",'a')
        for data in metadata:
            listfile.write(data)
        listfile.close()
