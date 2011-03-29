import _importer

from gtkmvc import View
import gtk

class Monitor (View):
    glade = "Monitor.glade"
    top = "main_window"

    def set_cpu_info(self, msg):
        self['label5'].set_text(msg)
        return
    
    def set_proc_list_info(self, tv_model):
        tv = self['treeview']
        tv.set_model(tv_model)
        model = tv.get_selection()
        model.set_mode(gtk.SELECTION_SINGLE)

        rend = gtk.CellRendererText()

        col = self['col_pid'] = gtk.TreeViewColumn('Pid', rend, text=0)
        col.set_clickable(True)
        tv.append_column(col)

        col = self['col_proc'] = gtk.TreeViewColumn('Process Name', rend, text=1)
        col.set_clickable(True)
        tv.append_column(col)
        
        pass
        
    pass
