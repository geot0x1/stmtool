
import subprocess

def execute(cmd, cwd=None):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=False, cwd=cwd)
    for stdout_line in iter(popen.stdout.readline, b''):
        yield stdout_line.decode('latin1')
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)