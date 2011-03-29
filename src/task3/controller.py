from gtkmvc import Controller
import gobject
import gtk
import signal
import os

class ProcMntrCtrl (Controller):
    """Handles signal processing, and keeps alignment of model and
    view"""

    def register_view(self, view):
        # sets initial values for the view
        view['main_window'].show()
        view.set_cpu_info(self.model.cpu_prcnt)
        view.set_proc_list_info(self.model.proc_list_store)
        self.sort_order = gtk.SORT_ASCENDING
        view['col_pid'].connect('clicked', self.on_column_clicked, 0)
        view['col_proc'].connect('clicked', self.on_column_clicked, 1)
        view['col_cpu'].connect('clicked', self.on_column_clicked, 2)
        view['treeview'].connect("cursor-changed", self.on_treeview_cursor_changed)


    # gtk signals
    def on_main_window_show(self, widget):
        self.__set_system_info()
        self.__set_hardware_info()
        self.g_id = gobject.timeout_add_seconds(1, self.__ref_timer)

    def on_main_window_delete_event(self, window, event):
        gtk.main_quit()
        return True

    def on_button_ref_clicked(self, button):
        self.model.ref_cpu_info()

    def on_button_end_clicked(self, button):
        print 'end'
        os.kill(self.curson_pid, signal.SIGTERM)

    def on_column_clicked(self, tc, user_data):
        print "column clicked", tc, user_data
        column = user_data
        self.model.proc_list_store.set_sort_column_id(column, self.sort_order)

        if self.sort_order == gtk.SORT_ASCENDING:
            self.sort_order = gtk.SORT_DESCENDING
        else:
            self.sort_order = gtk.SORT_ASCENDING

    def on_treeview_cursor_changed(self, treeview):
        print "Treeview Cursor changed"
        s = treeview.get_selection()
        (ls, iter) = s.get_selected()
        if iter is None:
            print "nothing selected"
            self.view['button_end'].set_sensitive(False)
        else:
            self.curson_pid = ls.get_value(iter, 0)
            data0 = ls.get_value(iter, 0)
            data1 = ls.get_value(iter, 1)
            self.view['button_end'].set_sensitive(True)
            print "Selected:", data0, data1

    # observable properties    
    def property_cpu_prcnt_value_change(self, model, old, new):
        self.view.set_cpu_info(new)
        return

    # def property_proc_list_store_value_change(self, model, old, new):
    #     self.view.set_proc_list_info(new)
    
    # private methods
    def __ref_timer(self):
        # self.model.ref_cpu_info()
        self.model.get_proc_info()
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
        
        for (id, core) in enumerate(self.model.cpuinfo):
            self.view['cpu%d_label' % id] = gtk.Label('Processor %d:' % id)
            self.view['hardware_table'].attach(self.view['cpu%d_label' % id], 0, 1, id+1, id+2, gtk.FILL, gtk.FILL)

            self.view['cpu%d_info' % id] = gtk.Label(core['model name'])
            self.view['hardware_table'].attach(self.view['cpu%d_info' % id], 1, 2, id+1, id+2, gtk.FILL, gtk.FILL)

            self.view['cpu%d_label' % id].show()
            self.view['cpu%d_info' % id].show()

    pass # end of class
