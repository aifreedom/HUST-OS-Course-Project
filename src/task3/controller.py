from gtkmvc import Controller
import gobject
import gtk
import commands

class ProcMntrCtrl (Controller):
    """Handles signal processing, and keeps alignment of model and
    view"""

    def register_view(self, view):
        # sets initial values for the view
        self.view['main_window'].show()
        self.view.set_cpu_info(self.model.cpu_info)
    
    # gtk signals
    def on_main_window_show(self, widget):
        self.__set_system_info()
        self.__set_hardware_info()
        self.g_id = gobject.timeout_add(500, self.__ref_timer)

    def on_main_window_delete_event(self, window, event):
        gtk.main_quit()
        return True

    def on_button_ref_clicked(self, button):
        self.model.ref_cpu_info()

    # observable properties    
    def property_cpu_info_value_change(self, model, old, new):
        self.view.set_cpu_info(new)
        return
    
    # private methods
    def __ref_timer(self):
        self.model.ref_cpu_info()
        return True
    
    def __set_system_info(self):
        # Release
        self.view['release_label'].set_text(
            ' '.join(('Release',
                      self.model.release,
                      '(%s)' % self.model.release_code,)))

        # Kernel
        self.view['kernel_label'].set_text(
            ' '.join(('Kernel',
                      self.model.kernel,)))
        # Gnome
        self.view['gnome_label'].set_text(self.model.gnome_ver)

    def __set_hardware_info(self):
        self.view['hardware_mem_label'].set_text(self.model.meminfo['MemTotal'])

        self.view['hardware_table'].resize(len(self.model.cpuinfo)+1, 2)
        
        for (id, core) in zip(range(len(self.model.cpuinfo)), self.model.cpuinfo):
            self.view['cpu%d_label' % id] = gtk.Label('Processor %d:' % id)
            self.view['hardware_table'].attach(self.view['cpu%d_label' % id], 0, 1, id+1, id+2, gtk.FILL, gtk.FILL)

            self.view['cpu%d_info' % id] = gtk.Label(core['model name'])
            self.view['hardware_table'].attach(self.view['cpu%d_info' % id], 1, 2, id+1, id+2, gtk.FILL, gtk.FILL)

            self.view['cpu%d_label' % id].show()
            self.view['cpu%d_info' % id].show()

    pass # end of class
