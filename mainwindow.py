from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("mainwindow.glade")
        window = builder.get_object("mainwindow")

        window.show_all()
        Gtk.main()
