import _importer
from gtkmvc import Model
import gtk
import re
from commands import getoutput
import os
import os.path

class ProcModel (Model):
    __observables__ = ('cpu_info', )
    cpu_info = '0.0'


    def __init__(self):
        Model.__init__(self)
        stat = open('/proc/stat').readline().rstrip().split(' ')
        stat = [int(i) for i in stat[1:] if i != '']
        self.last_idle = sum(stat[1:])
        self.last_cpu = stat[3]
        self.get_system_info()
        self.get_cpu_info()
        self.get_mem_info()
        self.get_proc_info()
        return

    def ref_cpu_info(self):
        stat = open('/proc/stat').readline().rstrip().split(' ')
        stat = [int(i) for i in stat[1:] if i != '']
        now_cpu = sum(stat[1:])
        now_idle = stat[3]
        if now_cpu - self.last_cpu != 0:
            self.cpu_info = str(100 - float(now_idle-self.last_idle) / (now_cpu - self.last_cpu) * 100)
        self.last_idle = now_idle
        self.last_cpu = now_cpu

    def get_system_info(self):
        self.release = getoutput('lsb_release -rs')
        self.release_code = getoutput('lsb_release -cs')

        self.kernel = getoutput('uname -sr')
        tmp = getoutput('gnome-about --version').split(' ')
        self.gnome_ver = tmp[0] + ' ' + tmp[-1]


    def get_cpu_info(self):
        self.cpuinfo = []
        cpuinfo = file('/proc/cpuinfo').read()
        
        for cpu in cpuinfo.split('\n\n')[:-1]:
            self.cpuinfo.append({})
            for line in cpu.splitlines():
                if line.split(':')[0].strip() != '':
                    self.cpuinfo[-1][line.split(':')[0].strip()] = line.split(':')[1].strip()

    def get_mem_info(self):
        self.meminfo = {}
        meminfo = file('/proc/meminfo').readlines()
        for line in meminfo:
            if line.split(':')[0].strip() != '':
                self.meminfo[line.split(':')[0].strip()] = line.split(':')[1].strip()

    def get_proc_info(self):
        self.proc_list_store = gtk.ListStore(str, str)
        proc = [pid for pid in os.listdir('/proc') if str.isdigit(pid)]
        for pid in proc:
            stat = file(os.path.join('/', 'proc', pid, 'stat')).read().split(' ')
            self.proc_list_store.append([stat[0], stat[1]])
        pass
                
    pass

