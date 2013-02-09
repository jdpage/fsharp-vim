from subprocess import Popen, PIPE

class FSAutoComplete:
    def __init__(self):
        self.p = Popen('cat', shell=False, stdin=PIPE, stdout=PIPE)

    def read_to_eof(self):
        while True:
            line = self.p.stdout.readline().strip('\n')
            if line == '<<EOF>>':
                break
            else:
                yield line

    def complete(self, line, column):
        self.p.stdin.write('hello\nworld\nfrom\npython\nand\nf#\n<<EOF>>\n')
        return list(self.read_to_eof())

if __name__ == '__main__':
    fsac = FSAutoComplete()
    assert fsac.complete(0, 0) == [ 'hello', 'from', 'python', 'and', 'f#' ]
