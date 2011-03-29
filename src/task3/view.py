import _importer

from gtkmvc import View

class Monitor (View):
    glade = "Monitor.glade"
    top = "main_window"

    def set_cpu_info(self, msg):
        self['label5'].set_text(msg)
        return
    
    def set_proc_list_info(self, new):
        tv = self['treeview']
        tv.set_model(new)

        rend = gtk.CellRendererText()
        col = gtk.TreeViewColumn('Pid', rend, text=0)
        col.set_name('col_pid')
        tv.append_column(col)

        rend = gtk.CellRendererText()
        col = gtk.TreeViewColumn('Process Name', rend, text=1)
        col.set_name('col_proc')
        tv.append_column(col)
        
        pass
        
    pass
