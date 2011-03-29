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
    pid_stat_cols = ('pid',  'comm',  'state',  'ppid',  'pgrp',  'session',  'tty_nr',  'tpgid',  'flags',  'minflt',  'cminflt',  'majflt',  'cmajflt',  'utime',  'stime',  'cutime',  'cstime',  'priority',  'nice',  'num_threads',  'itrealvalue',  'starttime',  'vsize',  'rss',  'rsslim',  'startcode',  'endcode',  'startstack',  'kstkesp',  'kstkeip',  'signal',  'blocked',  'sigignore',  'sigcatch',  'wchan',  'nswap',  'cnswap',  'exit_signal',  'processor',  'rt_priority ',  'policy',  'delayacct_blkio_ticks',  'guest_time',  'cguest_time', )

    def __init__(self):
        Model.__init__(self)
        stat = open('/proc/stat').readline().rstrip().split(' ')
        stat = [int(i) for i in stat[1:] if i != '']
        self.last_idle = sum(stat[1:])
        self.last_cpu = stat[3]
        self.proc_list_store = gtk.ListStore(int, str, str)
        self.proc_list = {}
        
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
        # self.proc_list_store.clear()
        # self.proc_list.clear()
        stat = open('/proc/stat').readline().rstrip().split(' ')
        stat = [int(i) for i in stat[1:] if i != '']
        now_cpu = sum(stat[1:])
        now_idle = stat[3]
        if now_cpu - self.last_cpu != 0:
            self.cpu_info = str(100 - float(now_idle-self.last_idle) / (now_cpu - self.last_cpu) * 100)
        self.last_idle = now_idle
        self.last_cpu = now_cpu
        proc = set((pid for pid in os.listdir('/proc') if str.isdigit(pid)))
        
        for pid in proc:
            try:
                stat = file(os.path.join('/', 'proc', pid, 'stat')).read().split(' ')
            except:
                pass
            if self.proc_list.has_key(pid):
                pl = self.proc_list[pid]
                iter = self.proc_list[pid]['iter']
                
                self.proc_list_store.set(iter,
                                         0, int(pl['pid']),
                                         1, pl['comm'],
                                         2, pl['state'])
            else:
                pl = self.proc_list[pid] = dict(zip(self.pid_stat_cols, stat))
                iter = self.proc_list_store.append((int(pl['pid']), pl['comm'],
                                                    pl['state']))
                self.proc_list[pid]['iter'] = iter
                self.proc_list_store.set(iter)
                # self.proc_list_store.append([stat[0], stat[1]])

        for pid in set(self.proc_list.keys()) - proc:
            self.proc_list_store.remove(self.proc_list[pid]['iter'])
            self.proc_list.pop(pid)
            
        pass
                
    pass

