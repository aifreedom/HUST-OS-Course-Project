import _importer
from gtkmvc import Model
import gtk
import re
from commands import getoutput
import os
import os.path

class CPUStat:
    def __init__(self, stat=None, busy_time=0, total_time=0):
        if stat:
            ti = [int(i) for i in stat.split(' ')]
            self.total_time = sum(ti)
            self.idle_time = ti[3]
        else:
            self.total_time = total_time
            self.idle_time = total_time - busy_time

    @staticmethod
    def diff(old, new):
        if new.total_time - old.total_time != 0:
            return 100 - float(new.idle_time - old.idle_time) / (new.total_time - old.total_time) * 100
        else:
            return 100
    

class ProcModel (Model):
    __observables__ = ('cpu_prcnt', )
    # cpu_info = '0.0'
    cpu_prcnt = '0.0'
    proc_list_store = gtk.ListStore(int, str, float)
    proc_list = {}
    meminfo = {}
    old_core_stat = {}
    new_core_stat = {}
    old_proc_stat = {}
    new_proc_stat = {}
    
    pid_stat_cols = ('pid',  'comm',  'state',  'ppid',  'pgrp',  'session',  'tty_nr',  'tpgid',  'flags',  'minflt',  'cminflt',  'majflt',  'cmajflt',  'utime',  'stime',  'cutime',  'cstime',  'priority',  'nice',  'num_threads',  'itrealvalue',  'starttime',  'vsize',  'rss',  'rsslim',  'startcode',  'endcode',  'startstack',  'kstkesp',  'kstkeip',  'signal',  'blocked',  'sigignore',  'sigcatch',  'wchan',  'nswap',  'cnswap',  'exit_signal',  'processor',  'rt_priority ',  'policy',  'delayacct_blkio_ticks',  'guest_time',  'cguest_time', )
    cpuline_pattern = re.compile(r'^cpu( |\d+) ([\d ]+)$')

    def __init__(self):
        Model.__init__(self)
        # stat = open('/proc/stat').readline().rstrip().split(' ')
        # stat = [int(i) for i in stat[1:] if i != '']
        # self.last_idle = sum(stat[1:])
        # self.last_cpu = stat[3]
        
        self.get_system_info()
        self.get_cpu_info()
        self.get_mem_info()
        self.proc_init()
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
        try:
            meminfo = file('/proc/meminfo').readlines()
        except:
            pass
        
        for line in meminfo:
            if line.split(':')[0].strip() != '':
                self.meminfo[line.split(':')[0].strip()] = line.split(':')[1].strip()

    def get_proc_info(self):
        try:
            stat = open(os.path.join('/', 'proc', 'stat')).readlines()
        except:
            pass

        it = iter(stat)
        for i in range(len(self.cpuinfo) + 1):
            line = it.next()
            ma = self.cpuline_pattern.match(line)
            if ma.group(1) == ' ':
                # general cpu info
                self.old_overall_stat = self.new_overall_stat
                self.new_overall_stat = CPUStat(ma.group(2))
            else:
                # core info
                self.old_core_stat[ma.group(1)] = self.new_core_stat[ma.group(1)]
                self.new_core_stat[ma.group(1)] = CPUStat(ma.group(2))
                pass

        self.cpu_prcnt = str(CPUStat.diff(self.old_overall_stat, self.new_overall_stat))
        
        try:
            proc = set((pid for pid in os.listdir(os.path.join('/', 'proc'))
                    if str.isdigit(pid)))
        except:
            pass
        
        total_time = self.new_overall_stat.total_time
        for pid in proc:
            
            try:
                stat = file(os.path.join('/', 'proc', pid, 'stat')).read().split(' ')
                cmdline = file(os.path.join('/', 'proc', pid, 'cmdline')).read().split('\0')[0].split(' ')[0]
            except:
                pass

            # Parse new stat
            new_list = dict(zip(self.pid_stat_cols, stat))
            new_stat = CPUStat(busy_time=int(new_list['utime']) + int(new_list['stime']), total_time=total_time)
            new_list['name'] = os.path.split(cmdline)[1]
            if (new_list['name'] == ''):
                new_list['name'] = new_list['comm'][1:-1]
            # new_list['name'] = cmdline

            if not self.proc_list.has_key(pid):
                self.proc_list[pid] = new_list
                self.new_proc_stat[pid] = new_stat
                
                new_list['cpu_prcnt'] = 100.0
                new_list['iter'] = it = self.proc_list_store.append(
                    (int(new_list['pid']), new_list['comm'], new_list['cpu_prcnt']))


            old_list = self.proc_list[pid]
            old_stat = self.new_proc_stat[pid]

            it = old_list['iter']

            new_list['cpu_prcnt'] = CPUStat.diff(old_stat, new_stat)

            self.proc_list_store.set(it,
                                     0, int(new_list['pid']),
                                     1, new_list['name'],
                                     2, float(new_list['cpu_prcnt']),)
            
            # Update the list 
            for key, val in new_list.items():
                old_list[key] = val
                
            self.old_proc_stat[pid] = old_stat
            self.new_proc_stat[pid] = new_stat


        for pid in set(self.proc_list.keys()) - proc:
            self.proc_list_store.remove(self.proc_list[pid]['iter'])
            self.proc_list.pop(pid)
            
        pass

    def proc_init(self):
        try:
            stat = open(os.path.join('/', 'proc', 'stat')).readlines()
        except:
            pass

        it = iter(stat)
        for i in range(len(self.cpuinfo) + 1):
            line = it.next()
            ma = self.cpuline_pattern.match(line)
            if ma.group(1) == ' ':
                # general cpu info
                self.new_overall_stat = CPUStat(ma.group(2))
            else:
                # core info
                self.new_core_stat[ma.group(1)] = CPUStat(ma.group(2))
                pass

        # end of cpuinfo loop
                
    pass

