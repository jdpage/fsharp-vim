from subprocess import Popen, PIPE
from os import path
import time

class FSAutoComplete:
    def __init__(self, dir):
        self.p = Popen(['mono', dir + '/bin/fsautocomplete.exe'],
                       stdin=PIPE,
                       stdout=PIPE)
        self.logfile=open("/tmp/log.txt", "w")
        
    def send(self, txt):
        #print "sending '%s'" % txt
        self.logfile.write(txt)
        self.logfile.flush()
        self.p.stdin.write(txt)
        
    def read_to_eof(self):
        while True:
            line = self.p.stdout.readline().strip('\n')
            if line == '<<EOF>>':
                break
            else:
                yield line

    def help(self):
        self.send("help\n")

    def project(self, fn):
        self.p("project \"%s\"\n" % path.abspath(fn))

    def parse(self, fn, full, txt):
        fulltext = "full" if full else ""
        self.send("parse \"%s\" %s\n%s\n<<EOF>>\n" %
                                (fn, fulltext, txt))

    def quit(self):
        self.send("quit\n")
        self.p.wait()
        self.logfile.close()

    def complete(self, fn, line, column):
        self.send('completion "%s" %d %d 1000\n' % (fn, line, column))
        msg = [""]
        while not msg[0].startswith("DATA: completion"):
            if msg[0].startswith("ERROR:"):
                return []
            msg = list(self.read_to_eof())
            self.logfile.write("\n".join(msg))
        return msg[1:]

if __name__ == '__main__':
    testscript = "test/TestScript.fsx"
    with open(testscript, 'r') as content_file:
        content = content_file.read()
    fsac = FSAutoComplete()
    fsac.parse(testscript, True, content)
    completions = fsac.complete(testscript, 7, 16)
    #print completions
    try:
        assert completions == []
        time.sleep(2.0)
        completions = fsac.complete(testscript, 7, 16)
        assert completions == [ 'function1', 'function2', 'gunction' ]
    finally:
        fsac.quit()
