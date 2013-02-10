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
        self.logfile.write("> " + txt)
        self.logfile.flush()
        self.p.stdin.write(txt)
        
    def read_to_eof(self):
        while True:
            line = self.p.stdout.readline()
            if line == '<<EOF>>\n':
                break
            else:
                if ':' in line:
                    self.logfile.write("< " + line)
                    self.logfile.flush()

                yield line.strip('\n')

    def help(self):
        self.send("help\n")

    def project(self, fn):
        self.p("project \"%s\"\n" % path.abspath(fn))

    def parse(self, fn, full, lines):
        fulltext = "full" if full else ""
        self.send("parse \"%s\" %s\n" % (fn, fulltext));
        for line in lines:
            self.send(line + "\n");
        self.send("<<EOF>>\n");

    def quit(self):
        self.send("quit\n")
        self.p.wait()
        self.logfile.close()

    def complete(self, fn, line, column, base):
        self.logfile.write('complete: base = %s\n' % base)
        self.send('completion "%s" %d %d 10000\n' % (fn, line, column))
        msg = [""]
        while not msg[0].startswith("DATA: completion"):
            if msg[0].startswith("ERROR:"):
                return msg
            msg = list(self.read_to_eof())

        msg = msg[1:]
        if base != "":
            msg = filter(lambda(line): line.startswith(base), msg)

        return msg

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
