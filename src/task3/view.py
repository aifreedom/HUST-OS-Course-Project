import _importer

from gtkmvc import View
import gtk
from math import pi
import cairo

class MonitorWindow(View):
    glade = "MonitorWindow.glade"
    top = "main_window"
    
    def __init__(self):
        View.__init__(self)

        self['cpu_monitor'] = Monitor()
        self['cpu_monitor'].show()
        self['box_cpu'].pack_start(self['cpu_monitor'])
    
    def set_cpu_info(self, msg):
        self['label5'].set_text('%.2f %%' % msg)
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
        
        col = self['col_cpu'] = gtk.TreeViewColumn('% CPU', rend, text=2)
        col.set_clickable(True)
        tv.append_column(col)

        col = self['col_mem'] = gtk.TreeViewColumn('Memory', rend, text=3)
        col.set_clickable(True)
        tv.append_column(col)
        pass
        
    pass

class Monitor(gtk.DrawingArea):
    # Draw in response to an expose-event
    __gsignals__ = { "expose-event": "override" }
    history = []

    bg_color = (.5, .5, .5)
    monitor_color = (1, 1, 1)
    p_upleft = (20, 10)
    padding = 5

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.set_double_buffered(False)

    
    # Handle the expose-event by drawing
    def do_expose_event(self, event):
        # Create the cairo context
        self.cr = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        self.cr.rectangle(event.area.x, event.area.y,
                          event.area.width, event.area.height)
        self.cr.clip()

        self.width = self.window.get_size()[0]-self.padding-self.p_upleft[0]
        self.height = self.window.get_size()[1]-self.padding-self.p_upleft[1]
        print self.width, self.height
        
        self.draw_cord(*self.window.get_size())
        # print dir(event)
        
    def draw_cord(self, width, height):
        cr = self.cr
        # print 'cord'
        # draw the canvas
        cr.set_source_rgb(*self.bg_color)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        
        cr.set_source_rgb(*self.monitor_color)

        cr.save()
        cr.translate(*self.p_upleft)
        cr.rectangle(0, 0, self.width, self.height)
        cr.fill()
        cr.restore()
        # self.draw_curve(map(lambda x, y: x*y, range(0, 100), [0.01]*100), 100)

    def draw_curve(self, his, maxlen):
        if self.window:
            self.draw_cord(*self.window.get_size())
            cr = self.cr
            history = his[:]
            # history[0] = 0.3
            history.reverse()
            history = [1-i for i in history]
            # print 'before'
            # cr.set_source_rgb(1, 0, 0)
            # cr.rectangle(10, 10, 100, 100)
            # cr.fill()
            # print 'after'
            
            cr.save()
            cr.set_line_width(0.01)
            cr.set_source_rgb(1, 0, 0)
            cr.translate(*self.p_upleft)
            cr.scale(self.width, self.height)
            cr.rotate(pi)
            cr.translate(-1, -1)

            # cr.move_to(0, 0)
            # cr.line_to(1, 1)
            # cr.stroke()
            # cr.arc(0, 0, 0.1, 0, pi*2)
            # cr.stroke()
            
            step = 1.0 / (maxlen-1)
            cr.move_to(0, history[0])
            print 0, history[0]
            for i, j in enumerate(history[1:]):
                print (i+1)*step, j
                cr.set_source_rgba(1, 0, 0, 1)
                cr.line_to((i+1)*step, j)
            print ''
            cr.stroke()
            cr.restore()
        pass

    def draw(self, width, height):
        cr = self.cr
        width = min(width, height)
        height = min(width, height)
        
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        # draw a rectangle
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.rectangle(10, 10, width - 20, height - 20)
        cr.fill()

        # draw lines
        cr.set_source_rgb(0.0, 0.0, 0.8)
        cr.move_to(width / 3.0, height / 3.0)
        cr.rel_line_to(0, height / 6.0)
        cr.move_to(2 * width / 3.0, height / 3.0)
        cr.rel_line_to(0, height / 6.0)
        cr.stroke()

        # and a circle
        cr.set_source_rgb(1.0, 0.0, 0.0)
        radius = min(width, height)
        cr.arc(width / 2.0, height / 2.0, radius / 2.0 - 20, 0, 2 * pi)
        cr.stroke()
        cr.arc(width / 2.0, height / 2.0, radius / 3.0 - 10, pi / 3, 2 * pi / 3)
        cr.stroke()

    pass
