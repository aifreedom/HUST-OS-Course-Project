import _importer

from gtkmvc import View

class Monitor (View):
    glade = "Monitor.glade"
    top = "main_window"

    def set_cpu_info(self, msg):
        print msg
        self['label5'].set_text(msg)
        return
    
    pass
