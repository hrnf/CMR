from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="CMR")
        self.connect("delete-event", Gtk.main_quit)

        self.boxmain = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.boxcontrol = Gtk.Box(spacing = 20)
        self.boxmanga = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.boxfilter = Gtk.Box(spacing = 3)
        self.boxsorting = Gtk.Box(spacing = 3)
        self.boxsearch = Gtk.Box(spacing = 3)

        self.add(self.boxmain)
        self.boxmain.pack_start(self.boxcontrol, False, False, 0)
        self.boxmain.pack_start(self.boxmanga, True, True, 0)
        self.boxmain.pack_start(self.boxfilter, False, False, 0)

        self.initboxControl()

        self.show_all()
        Gtk.main()

    def initboxControl(self):
        cbcatalogueModel = Gtk.ListStore(str)
        cbsortingModel = Gtk.ListStore(str)
        cblangModel = Gtk.ListStore(str)
        cbcatalogue = Gtk.ComboBox.new_with_model(cbcatalogueModel)
        cbsorting = Gtk.ComboBox.new_with_model(cbsortingModel)
        cbcatalogueRT = Gtk.CellRendererText()
        cbsortingRT = Gtk.CellRendererText()
        bttdecreasing = Gtk.Button.new_with_label("|>")
        bttincreasing = Gtk.Button.new_with_label("<|")
        entryname = Gtk.Entry()
        bttsearch = Gtk.Button.new_with_label("Q")
        cblang = Gtk.ComboBox.new_with_model(cblangModel)
        cblangRT = Gtk.CellRendererText()
        check18 = Gtk.CheckButton("+18")
        checkJP = Gtk.CheckButton("JP")

        cbcatalogueModel.append(["Suggested"])
        cbcatalogueModel.append(["Explore"])
        cbcatalogueModel.append(["Reading"])

        cbsortingModel.append(["Last Update"])
        cbsortingModel.append(["Date"])
        cbsortingModel.append(["Alphabetical"])

        cblangModel.append(["BR"])
        cblangModel.append(["EN"])
        cblangModel.append(["ES"])
        cblangModel.append(["JP"])
        cblangModel.append(["RU"])

        cbcatalogue.pack_start(cbcatalogueRT, True)
        cbcatalogue.add_attribute(cbcatalogueRT, "text", 0)
        cbcatalogue.set_active(0)

        cbsorting.pack_start(cbsortingRT, True)
        cbsorting.add_attribute(cbsortingRT, "text", 0)
        cbsorting.set_active(0)

        cblang.pack_start(cblangRT, True)
        cblang.add_attribute(cblangRT, "text", 0)
        cblang.set_active(1)

        self.boxsorting.pack_start(cbsorting, False, False, 0)
        self.boxsorting.pack_start(bttdecreasing, False, False, 0)
        self.boxsorting.pack_start(bttincreasing, False, False, 0)

        self.boxsearch.pack_start(entryname, False, False, 0)
        self.boxsearch.pack_start(bttsearch, False, False, 0)

        self.boxcontrol.pack_start(cbcatalogue, False, False, 0)
        self.boxcontrol.pack_start(self.boxsorting, False, False, 0)
        self.boxcontrol.pack_start(self.boxsearch, False, False, 0)

        self.boxcontrol.pack_end(checkJP, False, False, 0)
        self.boxcontrol.pack_end(check18, False, False, 0)
        self.boxcontrol.pack_end(cblang, False, False, 0)
