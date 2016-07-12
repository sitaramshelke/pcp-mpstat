from pcp import pmapi
from pcp import pmcc
import sys
MPSTAT_METRICS = ['pmda.uname', 'hinv.map.cpu_num', 'hinv.ncpu', 'hinv.cpu.online', 'kernel.all.cpu.user',
                'kernel.all.cpu.nice', 'kernel.all.cpu.sys', 'kernel.all.cpu.wait.total',
                'kernel.all.cpu.irq.hard', 'kernel.all.cpu.irq.soft', 'kernel.all.cpu.steal',
                'kernel.all.cpu.guest', 'kernel.all.cpu.guest_nice', 'kernel.all.cpu.idle',
                'kernel.percpu.cpu.user', 'kernel.percpu.cpu.nice', 'kernel.percpu.cpu.sys',
                'kernel.percpu.cpu.wait.total', 'kernel.percpu.cpu.irq.hard', 'kernel.percpu.cpu.irq.soft',
                'kernel.percpu.cpu.steal', 'kernel.percpu.cpu.guest','kernel.percpu.cpu.guest_nice',
                'kernel.percpu.cpu.idle']

class NamedInterrupts:
    def __init__(self):
        self.context = None
        self.interrupt_list = []

    def AppendCallback(self, args):
        self.interrupt_list.append(args)

    def GetAllNamedInterrupts(self):
        self.context = pmapi.pmContext()
        self.context.pmTraversePMNS("kernel.percpu.interrupts",self.AppendCallback)
        return self.interrupt_list

class ReportingMetricRepository:
    def __init__(self,group):
        self.group = group
        self.current_cached_values = {}
        self.previous_cached_values = {}
    def __fetch_current_values(self,metric,instance):
        if instance is not None:
            return dict(map(lambda x: (x[0].inst, x[2]), self.group[metric].netValues))
        else:
            return self.group[metric].netValues[0][2]

    def __fetch_previous_values(self,metric,instance):
        if instance is not None:
            return dict(map(lambda x: (x[0].inst, x[2]), self.group[metric].netPrevValues))
        else:
            return self.group[metric].netPrevValues[0][2]

    def current_value(self, metric, instance):
        if not metric in self.group:
            return None
        if instance is not None:
            if self.current_cached_values.get(metric, None) is None:
                lst = self.__fetch_current_values(metric,instance)
                self.current_cached_values[metric] = lst

            return self.current_cached_values[metric].get(instance,None)
        else:
            if self.current_cached_values.get(metric, None) is None:
                self.current_cached_values[metric] = self.__fetch_current_values(metric,instance)
            return self.current_cached_values.get(metric, None)

    def previous_value(self, metric, instance):
        if not metric in self.group:
            return None
        if instance is not None:
            if self.previous_cached_values.get(metric, None) is None:
                lst = self.__fetch_previous_values(metric,instance)
                self.previous_cached_values[metric] = lst
            return self.previous_cached_values[metric].get(instance,None)
        else:
            if self.previous_cached_values.get(metric, None) is None:
                self.previous_cached_values[metric] = self.__fetch_previous_values(metric,instance)
            return self.previous_cached_values.get(metric, None)

    def current_values(self, metric_name):
        if self.group.get(metric_name, None) is None:
            return None
        if self.current_cached_values.get(metric_name, None) is None:
            self.current_cached_values[metric_name] = self.__fetch_current_values(metric_name,True)
        return self.current_cached_values.get(metric_name, None)

    def previous_values(self, metric_name):
        if self.group.get(metric_name, None) is None:
            return None
        if self.previous_cached_values.get(metric_name, None) is None:
            self.previous_cached_values[metric_name] = self.__fetch_previous_values(metric_name,True)
        return self.previous_cached_values.get(metric_name, None)

class CoreCpuUtil:
    def __init__(self, instance, delta_time, metric_repository):
        self.delta_time = delta_time
        self.instance = instance
        self.metric_repository = metric_repository
    def __all_or_percpu(self):
        return 'all' if self.instance is None else 'percpu'
    def cpu_number(self):
        return self.instance
    def cpu_online(self):
        return self.metric_repository.current_value('hinv.cpu.online', self.instance)
    def user_time(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.user'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%(((c_time - p_time)/self.delta_time)))
        else:
            return None
    def nice_time(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.nice'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%(((c_time - p_time)/self.delta_time)))
        else:
            return None
    def sys_time(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.sys'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%((c_time - p_time)/self.delta_time))
        else:
            return None
    def iowait_time(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.wait.total'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%((c_time - p_time)/self.delta_time))
        else:
            return None
    def irq_hard(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.irq.hard'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%((c_time - p_time)/self.delta_time))
        else:
            return None
    def irq_soft(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.irq.soft'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%((c_time - p_time)/self.delta_time))
        else:
            return None
    def steal(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.steal'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%((c_time - p_time)/self.delta_time))
        else:
            return None
    def guest_time(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.guest'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%((c_time - p_time)/self.delta_time))
        else:
            return None
    def guest_nice(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.guest_nice'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%((c_time - p_time)/self.delta_time))
        else:
            return None
    def idle_time(self):
        metric = 'kernel.' + self.__all_or_percpu() + '.cpu.idle'
        p_time = self.metric_repository.previous_value(metric, self.instance)
        c_time = self.metric_repository.current_value(metric, self.instance)
        if p_time is not None and c_time is not None:
            return float("%.2f"%((c_time - p_time)/self.delta_time))

class CpuUtil:
    def __init__(self, delta_time, metric_repository):
        self.__metric_repository = metric_repository
        self.delta_time = delta_time
    def get_totalcpu_util(self):
        return CoreCpuUtil(None, self.delta_time, self.__metric_repository)
    def get_percpu_util(self):
        return map((lambda cpuid: (CoreCpuUtil(cpuid, self.delta_time, self.__metric_repository))), self.__cpus())
    def __cpus(self):
        cpu_dict = self.__metric_repository.current_values('hinv.map.cpu_num')
        return sorted(cpu_dict.values())

class CpuFilter:
    def __init__(self, options):
        self.options = options
    def filter_cpus(self, cpus):
        return filter(lambda c: self.__predicate(c), cpus)
    def __predicate(self, cpu):
        return self.__matches_cpu(cpu)
    def __matches_cpu(self, cpu):
        if self.options.cpu_list == 'ALL':
            return True
        elif self.options.cpu_list == 'ON':
            if cpu.cpu_online() == 1:
                return True
            else:
                return False
        elif self.options.cpu_list is not None:
            if cpu.cpu_number() in self.options.cpu_list:
                return True
            else:
                return False
        else:
            return True

class CpuUtilReporter:
    def __init__(self, cpu_util, cpu_filter, mpstat_options):
        self.cpu_util = cpu_util
        self.cpu_filter = cpu_filter
        self.mpstat_options = mpstat_options
    def print_report(self, timestamp):
        print("Timestamp\tCPU\t%usr\t%nice\tsys\t%iowait\t%irq\t%soft\t%steal\t%guest\t%gnice\t%idle")
        if self.mpstat_options.cpu_list == 'ALL':
            cpu_util = self.cpu_util.get_totalcpu_util()
            print("%s\tALL\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(timestamp, cpu_util.user_time(), cpu_util.nice_time(), cpu_util.sys_time(), cpu_util.iowait_time(), cpu_util.irq_hard(), cpu_util.irq_soft(), cpu_util.steal(), cpu_util.guest_time(), cpu_util.guest_nice(), cpu_util.idle_time()))

        cpu_util_list = self.cpu_filter.filter_cpus(self.cpu_util.get_percpu_util())
        for cpu_util in cpu_util_list:
            print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(timestamp, cpu_util.cpu_number(), cpu_util.user_time(), cpu_util.nice_time(), cpu_util.sys_time(), cpu_util.iowait_time(), cpu_util.irq_hard(), cpu_util.irq_soft(), cpu_util.steal(), cpu_util.guest_time(), cpu_util.guest_nice(), cpu_util.idle_time()))





class MpstatOptions(pmapi.pmOptions):
    cpu_list = None
    cpu_filter = False
    def extraOptions(self, opt,optarg, index):
        if opt == 'P':
            if optarg == 'ALL' or optarg == 'ON':
                MpstatOptions.cpu_filter = True
                MpstatOptions.cpu_list = optarg
            else:
                MpstatOptions.cpu_filter = True
                try:
                    MpstatOptions.cpu_list = list(map(lambda x:int(x),optarg.split(',')))
                except ValueError as e:
                    print ("Invalid CPU List: use comma separated cpu nos without whitespaces")
                    sys.exit(1)

    def __init__(self):
        pmapi.pmOptions.__init__(self,"P:V?")
        self.pmSetOptionCallback(self.extraOptions)
        self.pmSetLongOptionVersion()
        self.pmSetLongOptionHelp()
        self.pmSetLongOption("",1,"P","[1,3..|ON|ALL]","Filter or Show All/Online CPUs")


class MpstatReport(pmcc.MetricGroupPrinter):
    Machine_info_count = 0

    def timeStampDelta(self, group):
        s = group.timestamp.tv_sec - group.prevTimestamp.tv_sec
        u = group.timestamp.tv_usec - group.prevTimestamp.tv_usec
        return (s + u / 1000000.0)

    def print_machine_info(self,group):
        machine_name = group['pmda.uname'].netValues[0][2]
        no_cpu =self.get_ncpu(group)
        print("%s\t(%s CPU)" % (machine_name,no_cpu))

    def get_ncpu(self,group):
        return group['hinv.ncpu'].netValues[0][2]

    def report(self,manager):
        group = manager['mpstat']
        if self.Machine_info_count == 0:
            self.print_machine_info(group)
            self.Machine_info_count = 1
            return  #to get prev timestamp value not none

        timestamp = group.contextCache.pmCtime(int(group.timestamp)).rstrip().split()
        interval_in_seconds = self.timeStampDelta(group)
        ncpu = self.get_ncpu(group)

        metric_repository = ReportingMetricRepository(group)
        cpu_util = CpuUtil(interval_in_seconds, metric_repository)
        cpu_filter = CpuFilter(MpstatOptions)
        reporter = CpuUtilReporter(cpu_util, cpu_filter, MpstatOptions)
        reporter.print_report(timestamp[3])





if __name__ == '__main__':
    namedInt = NamedInterrupts()
    interrupt_list = namedInt.GetAllNamedInterrupts()
    # print interrupt_list
    try:
        opts = MpstatOptions()
        manager = pmcc.MetricGroupManager.builder(opts,sys.argv)
        manager['mpstat'] = MPSTAT_METRICS
        manager.printer = MpstatReport()
        sts = manager.run()
        sys.exit(sts)
    except pmapi.pmErr as pmerror:
        sys.stderr.write('%s: %s\n' % (pmerror.progname,pmerror.message()))
    except pmapi.pmUsageErr as usage:
        usage.message()
        sys.exit(1)
    except KeyboardInterrupt:
        pass
