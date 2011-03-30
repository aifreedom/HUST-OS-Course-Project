#!/usr/bin/python

import gtk

if __name__ == "__main__":

    from model import ProcModel
    from controller import ProcMntrCtrl
    from view import MonitorWindow
    
    m = ProcModel()
    v = MonitorWindow()
    c = ProcMntrCtrl(m,v)

    gtk.main()
    pass
