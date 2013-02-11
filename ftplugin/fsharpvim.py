from subprocess import Popen, PIPE
from os import path
import tempfile
import unittest

class FSAutoComplete:
    def __init__(self, dir):
        command = ['mono', dir + '/bin/fsautocomplete.exe']
        opts = { 'stdin': PIPE, 'stdout': PIPE, 'universal_newlines': True }
        try:
            self.p = Popen(command, **opts)
        except WindowsError:
            self.p = Popen(command[1:], **opts)

        self.logfile = open(tempfile.gettempdir() + "/log.txt", "w")
        
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

    def read_and_find(self, line):
        while True:
            msg = list(self.read_to_eof())
            if msg[0].startswith(line):
                return msg[1:]
            else:
                return msg

    def help(self):
        self.send("help\n")

    def project(self, fn):
        self.send("project \"%s\"\n" % path.abspath(fn))

    def parse(self, fn, full, lines):
        fulltext = "full" if full else ""
        self.send("parse \"%s\" %s\n" % (fn, fulltext))
        for line in lines:
            self.send(line + "\n")
        self.send("<<EOF>>\n")
        self.read_and_find('INFO: Background parsing started')

    def quit(self):
        self.send("quit\n")
        self.p.wait()
        self.logfile.close()

    def complete(self, fn, line, column, base):
        self.logfile.write('complete: base = %s\n' % base)
        self.send('completion "%s" %d %d 10000\n' % (fn, line, column))
        msg = self.read_and_find('DATA: completion')
        if base != '':
            msg = filter(lambda(line): line.startswith(base), msg)

        return msg

    def tooltip(self, fn, line, column):
        self.send('tooltip "%s" %d %d 1000\n' % (fn, line, column))
        return self.read_and_find('DATA: tooltip')

class FSharpVimFixture(unittest.TestCase):
    def setUp(self):
        self.fsac = FSAutoComplete('.')
        self.testscript = 'test/TestScript.fsx'
        with open(self.testscript, 'r') as content_file:
            content = map(lambda(line): line.strip('\n'), list(content_file))

        self.fsac.parse(self.testscript, True, content)

    def tearDown(self):
        self.fsac.quit()

    def test_completion(self):
        completions = self.fsac.complete(self.testscript, 7, 16, '')
        self.assertEqual([ 'function1', 'function2', 'gunction' ], completions)

if __name__ == '__main__':
    unittest.main()
