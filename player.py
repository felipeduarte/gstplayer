#coding: utf-8
import pygtk
import gtk
pygtk.require('2.0')
import pygst
pygst.require('0.10')
import gst


class Tela(object):    

    def __init__(self):
        win = gtk.Window()
        win.set_title("GstPlayer")
        win.set_size_request(500, 300)
        win.connect("destroy", gtk.main_quit)

        container = gtk.HBox(False, 0)
        win.add(container)

        fixar = gtk.Fixed()
        container.pack_start(fixar)
        fixar.show()

        #botão play:
        bt_play = gtk.Button("Play")
        fixar.put(bt_play, 50, 100)
        container.pack_start(bt_play)
        bt_play.connect("clicked", self.clicada_play)

        #botão stop:
        bt_stop = gtk.Button("Stop")
        fixar.put(bt_stop, 100, 100)
        container.pack_start(bt_stop)
        bt_stop.connect("clicked", self.clicada_stop)

        #botão pause:
        bt_pause = gtk.Button("Pause")
        fixar.put(bt_pause, 150, 100)
        container.pack_start(bt_pause)
        bt_pause.connect("clicked", self.clicada_pause)

        win.show_all()

        self.paipe = gst.Pipeline('paipeline')
        self.source = gst.element_factory_make('filesrc', 'source')
        self.decoder = gst.element_factory_make('mad', 'decoder')
        self.convert = gst.element_factory_make('audioconvert', 'convert')
        self.resample = gst.element_factory_make('audioresample', 'resample')
        self.sink = gst.element_factory_make('alsasink', 'sink')

        self.paipe.add(self.source)
        self.paipe.add(self.decoder)
        self.paipe.add(self.convert)
        self.paipe.add(self.resample)
        self.paipe.add(self.sink)

        gst.element_link_many(self.source, self.decoder, self.convert, self.resample, self.sink)

        self.paipe.set_state(gst.STATE_READY)

    def clicada_play(self, bt_play):
        if self.paipe.get_state()[1] == gst.STATE_READY or self.paipe.get_state()[1] == gst.STATE_NULL:
            dialog = gtk.FileChooserDialog("Open..",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            dialog.set_default_response(gtk.RESPONSE_OK)
            filter = gtk.FileFilter()
            filter.set_name("All files")
            filter.add_pattern("*")
            dialog.add_filter(filter)
            filter = gtk.FileFilter()
            filter.set_name("Musics")
            filter.add_pattern("*.mp3")
            dialog.add_filter(filter)
            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                print dialog.get_filename(), 'selected'
            elif response == gtk.RESPONSE_CANCEL:
                print 'Closed, no files selected'
            self.caminho = dialog.get_filename()
            dialog.destroy()
            self.source.set_property('location', self.caminho)
            self.paipe.set_state(gst.STATE_PLAYING)
        elif self.paipe.get_state()[1] == gst.STATE_PAUSED:
            self.paipe.set_state(gst.STATE_PLAYING)
        elif self.paipe.get_state()[1] == gst.STATE_PLAYING:
            self.confirmar_tocando()
    
    def confirmar_tocando(self):
        self.aviso = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.aviso.set_border_width(10)
        self.aviso.set_title("Aviso")
        self.mensagem = gtk.Label("A música já esta em execução!!")
        container = gtk.HBox(False, 0)
        self.aviso.add(container)
        fixar = gtk.Fixed()
        container.pack_start(fixar)
        fixar.show()
        container.pack_start(self.mensagem)
        self.aviso.show_all()

    def clicada_stop(self, bt_stop):
        self.paipe.set_state(gst.STATE_NULL)

    def clicada_pause(self, bt_pause):
        if self.paipe.get_state()[1] == gst.STATE_PLAYING:
            self.paipe.set_state(gst.STATE_PAUSED)

if __name__ == "__main__":
    tela = Tela()
    gtk.main()
    
