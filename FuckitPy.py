from __future__ import print_function

import time
import multiprocessing as mp
import sys
import os


class Process(mp.Process):
    def __init__(self, *args, **kwargs):
        mp.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = mp.Pipe()
        self._exception = None

    def run(self):
        try:
            mp.Process.run(self)
            self._cconn.send(None)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            exc_info = []
            while exc_tb:
                file_name = exc_tb.tb_frame.f_code.co_filename
                if file_name == os.path.abspath(__file__):
                    file_name = -1
                exc_info.append((file_name, exc_tb.tb_lineno))
                exc_tb = exc_tb.tb_next
            if hasattr(exc_obj, 'lineno') and hasattr(exc_obj, 'filename'):
                exc_info.append((exc_obj.filename, exc_obj.lineno))
            self._cconn.send(exc_info[::-1])
            # raise e  # You can still rise this exception if you need to

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


# In cases your ugly code runs endless loop
TIMEOUT = 300


def py_executor(__pycode):
    gbs = dict(globals())
    for variable in globals().keys():
        if variable[0:2] != "__":
            del gbs[variable]
    del variable
    exec(__pycode, gbs)


class PyClean:
    def __init__(self, py_input, py_path):
        self.py_input = py_input
        self.py_path = py_path

    def clean(self):
        lines = self.py_input.split('\n')
        while lines:
            if any(x.strip() for x in lines):
                code = '\n'.join(lines)
                try:
                    p = Process(target=py_executor, args=(code,))
                    start_time = time.time()
                    p.start()
                    while time.time() - start_time <= TIMEOUT:
                        if not p.is_alive():
                            break
                        time.sleep(0.5)

                    if p.is_alive():
                        # Don't try to loop endlessly
                        p.kill()
                        print('Execution timeout! Removing last line...')
                        lines = lines[:-1]
                        continue

                    elif p.exception:
                        # Good, we found an error
                        for fn, tb_lineno in p.exception:
                            if fn == -1:
                                break
                            if fn and fn != self.py_path and os.path.isfile(fn):
                                # Remove shitty imports...
                                try:
                                    print('Correcting {}...'.format(fn))
                                    with open(fn, 'r+', errors='ignore') as f:
                                        temp_lines = list(f.readlines())
                                        temp_lines[tb_lineno - 1] = '\n'
                                        f.seek(0)
                                        f.truncate(0)
                                        f.writelines(temp_lines)
                                    break
                                except OSError:
                                    continue
                            else:
                                print('Resolving error on line {}'.format(tb_lineno))
                                lines[tb_lineno - 1] = ''
                            break
                    else:
                        print('Congratulations!')
                        # Your code is runnable now!
                        break
                except mp.ProcessError:
                    # In case something error occurs.
                    print(f'Something error in processing')
                    lines = lines[:-1]
            else:
                # Nothing left, perfect
                break
        return '\n'.join(lines)


def clean_py(py_file):
    if os.path.isfile(py_file):
        try:
            with open(py_file, 'r+', errors='ignore') as f:
                o = PyClean(f.read(), os.path.abspath(py_file))
                f.seek(0)
                new_code = o.clean()
                f.truncate(0)
                f.write(new_code)
                f.flush()
        except OSError:
            print('Cannot open {}'.format(py_file))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        clean_py(sys.argv[1])
    else:
        print('No arguments')
