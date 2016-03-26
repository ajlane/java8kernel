from IPython.kernel.zmq.kernelbase import Kernel
import pexpect


class JavaKernel(Kernel):
    implementation = 'JavaKernel'
    implementation_version = '0.0.1'
    language = 'Java'
    language_version = '1.8'

    repl = pexpect.spawn('java -jar /home/vagrant/javakernel/javarepl.jar')
    repl.expect('java>')

    banner=repl.before.decode('utf-8')

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.repl.sendline(code)
        self.repl.expect('java>')
        if not silent:
            stream_content = {'name':'stdout', 'text': self.repl.before.decode('utf-8')}
            self.send_response(self.iopub_socket, 'stream', stream_content)
            return {
                'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
            }

if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=JavaKernel)
