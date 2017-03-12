from ipykernel.kernelbase import Kernel
import os
import re
import pexpect


class JavaKernel(Kernel):
    implementation = 'JavaKernel'
    implementation_version = '0.0.1'
    language = 'Java'
    language_version = '1.8'
    language_info = {
        'name': 'Java'
    }

    java_exe = "{}/bin/java".format(os.environ.get("JAVA_HOME")) if "JAVA_HOME" in os.environ else "java"
    java_repl = os.environ.get("JAVA_REPL", "javarepl.jar")
    classpath = os.environ.get("CLASSPATH", "")
    java_opts = os.environ.get("JAVA_OPTS", "")
    

    repl = pexpect.spawn('{} -cp "{}:{}" {} javarepl.Main'.format(java_exe, java_repl, classpath, java_opts))
    repl.expect('java>')

    banner=repl.before.decode('utf-8')

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.repl.sendline(re.sub(r'\s+', ' ', code, flags=re.MULTILINE))
        self.repl.expect('java>')
        response=self.repl.before.decode('utf-8')
        if not silent:
            stream_content = {'output_type':'stream', 'name':'stdout', 'text': response.split('\n',1)[1]}
            self.send_response(self.iopub_socket, 'stream', stream_content)
            return {
                'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
            }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=JavaKernel)
