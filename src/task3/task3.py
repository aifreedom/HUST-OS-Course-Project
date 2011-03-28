import gtk

if __name__ == "__main__":

    from model import ProcModel
    from controller import ProcMntrCtrl
    from view import Monitor
    
    m = ProcModel()
    v = Monitor()
    c = ProcMntrCtrl(m,v)

    gtk.main()
    pass
