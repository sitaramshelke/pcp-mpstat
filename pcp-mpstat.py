from pcp import pmapi

class NameInterrupts:
    def __init__(self):
        self.context = None
        self.interrupt_list = []

    def PrintCallback(self, args):
        self.interrupt_list.append(args)

    def GetAllNamedInterrupts(self):
        self.context = pmapi.pmContext()
        self.context.pmTraversePMNS("kernel.percpu.interrupts",self.PrintCallback)
        return self.interrupt_list

if __name__ == '__main__':
    namedInt = NameInterrupts()
    interrupt_list = namedInt.GetAllNamedInterrupts()
    print interrupt_list
