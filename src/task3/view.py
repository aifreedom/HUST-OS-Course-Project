import _importer

from gtkmvc import View
import gtk
from gtk.gdk import Color
from math import pi
import cairo

class MonitorWindow(View):
    glade = "MonitorWindow.glade"
    top = "main_window"
    cpu_color = (1.0, 0.0, 0.0)
    mem_color = (0.0, 0.0, 1.0)
    
    def __init__(self):
        View.__init__(self)

        self['cpu_monitor'] = Monitor(self.cpu_color)
        self['cpu_monitor'].show()
        self['box_cpu'].pack_start(self['cpu_monitor'])
    
        self['mem_monitor'] = Monitor(self.mem_color)
        self['mem_monitor'].show()
        self['box_mem'].pack_start(self['mem_monitor'])

        self['button_cpu_prcnt'].set_color(
            Color(*(self['cpu_monitor'].line_color)))
        self['button_mem_prcnt'].set_color(
            Color(*(self['mem_monitor'].line_color)))
        
    def set_cpu_info(self, msg):
        self['cpu_prcnt'].set_text('CPU %.2f %%' % msg)
        return

    def set_mem_info(self, msg):
        self['mem_prcnt'].set_text('Memory %.2f %%' % msg)
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
    maxlen = 0

    bg_color = (.7, .7, .7)
    monitor_color = (1, 1, 1)
    
    help_line_color = (0, 0, 0)
    help_line_width = 0.5
    help_line_dash  = (3,)
    
    p_upleft = (40, 10)
    padding = (5, 20)
    time_grid = 72
    load_grid = 40

    def __init__(self, line_color):
        gtk.DrawingArea.__init__(self)
        # self.set_double_buffered(False)
        self.line_color = line_color

    
    # Handle the expose-event by drawing
    def do_expose_event(self, event):
        # Create the cairo context
        cr = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                          event.area.width, event.area.height)
        cr.clip()


        width, height = (i-j-k for i, j, k in
                         zip(self.window.get_size(), self.padding,
                             self.p_upleft))
        
        self.draw_cord(cr, width, height)
        self.draw_curve(cr, width, height)
        # print dir(event)

    def draw_text(self, cr, text, x, y):
        (xbearing, ybearing,
         fwidth, fheight,
         xadvance, yadvance) = cr.text_extents(text)
        cr.move_to(x - fwidth - 5, y + fheight/2)
        cr.show_text(text)
        cr.stroke()
        
    def draw_cord(self, cr, width, height):
        cr.set_source_rgb(*self.bg_color)
        cr.rectangle(0, 0, *self.window.get_size())
        cr.fill()
        
        cr.set_source_rgb(*self.monitor_color)

        cr.save()
        cr.translate(*self.p_upleft)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        cr.restore()

        cr.save()
        
        cr.translate(*self.p_upleft)

        cr.set_source_rgb(*self.help_line_color)
        cr.set_line_width(self.help_line_width)
        cr.set_dash(self.help_line_dash)
        
        load_step = float(height) / (height / self.load_grid)

        cr.save()
        cr.select_font_face('Serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(10)
        for i in range(int(height / load_step) - 1):
            cr.move_to(0, (i+1)*load_step)
            cr.line_to(width, (i+1)*load_step)
            cr.stroke()
            self.draw_text(cr,
                           '%.0f %%' % (100 -
                                        float(i+1) /
                                        (height / load_step)
                                        * 100),
                           0, (i+1)*load_step)
        cr.restore()
        self.draw_text(cr, '100 %', 0, 0)
        self.draw_text(cr, '0 %', 0, height)
            
        time_step = float(width) / 6
        for i in range(int(width / time_step) - 1):
            text = '%d s' % (50 - i*10)
            x = (i+1)*time_step
            y = height
            (xbearing, ybearing,
             fwidth, fheight,
             xadvance, yadvance) = cr.text_extents(text)
            cr.move_to(x - fwidth/2 , y + fheight + 5)
            cr.show_text(text)
            cr.stroke()
            cr.move_to(x, 0)
            cr.line_to(x, y)
            cr.stroke()
            
        cr.restore()


    def draw_curve(self, cr, width, height):
        history = [i/100 for i in self.history]
        history.reverse()

        cr.save()
        cr.set_source_rgb(*self.line_color)
        
        cr.translate(*self.p_upleft)
        cr.scale(width, height)
        cr.rotate(pi)
        cr.translate(-1, -1)
        cr.scale(1.0/width, 1.0/height)

        step = float(width) / (self.maxlen-1)
        for i, j in enumerate(history):
            cr.line_to(i*step, j*height)
        cr.stroke()
        cr.restore()

    pass
