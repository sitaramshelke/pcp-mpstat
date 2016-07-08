from pcp import pmapi

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

if __name__ == '__main__':
    namedInt = NamedInterrupts()
    interrupt_list = namedInt.GetAllNamedInterrupts()
    print interrupt_list
