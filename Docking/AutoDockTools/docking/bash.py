#! /usr/bin/env python
import threading
import subprocess
import traceback
import shlex
import asyncio

class Command(object):
    """
    Enables to run subprocess commands in a different thread with TIMEOUT option.
    Based on jcollado's solution:
    http://stackoverflow.com/questions/1191374/subprocess-with-timeout/4825933#4825933
    """
    command = None
    process = None
    status = None
    output, error = '', ''
    commands=[]

    def run(self, cmd,timeout=None, **kwargs):
        """ Run a command then return: (status, output, error). """
        def target(**kwargs):
            try:
                print(self.command)
                self.process = subprocess.Popen(cmd, **kwargs)
                self.output, self.error = self.process.communicate()
                self.status = self.process.returncode
            except:
                self.error = traceback.format_exc()
                self.status = -1
        # default stdout and stderr
        if 'stdout' not in kwargs:
            kwargs['stdout'] = subprocess.PIPE
        if 'stderr' not in kwargs:
            kwargs['stderr'] = subprocess.PIPE
        # thread
        thread = threading.Thread(target=target, kwargs=kwargs)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
        return self.status, self.output, self.error

    def add_command(self,cmd):
        cmd = shlex.split(cmd)
        self.commands.append(cmd)
    #async def command(self):
    #    proc = await asyncio.create_subprocess_shell(
    #        self.command,
    #        stdout=asyncio.subprocess.PIPE,
    #        stderr=asyncio.subprocess.PIPE)

    #        stdout, stderr = await proc.communicate()

    #    print(f'[{cmd!r} exited with {proc.returncode}]')
    #    if stdout:
    #        print(f'[stdout]\n{stdout.decode()}')
    #    if stderr:
    #        print(f'[stderr]\n{stderr.decode()}')
    
    