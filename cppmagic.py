# -*- coding: utf-8 -*-
"""C++ magic


"""
#-----------------------------------------------------------------------------
# Copyright (C) 2013, Svenn-Arne Dragly
#
# Distributed under the terms of the GNU GPLv3 License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import print_function

import io
import os
import pipes
import subprocess
import sys

try:
    import hashlib
except ImportError:
    import md5 as hashlib

from IPython.core.magic import Magics, magics_class, cell_magic

@magics_class
class CppMagics(Magics):
    """Magics for C++ compilation"""

    @cell_magic
    def cpp(self, line, cell):
        """Compile C++ code into an executable, run it and show the output.

        Usage, in cell mode::

            %%cpp <compiler flags>
            <C++ code>

        The compiler flags are passed verbatim to `g++` so they may be
        used to control warnings (`-Wall`), add optimizations (`-O2`), and
        modify features (`-fno-builtin`).
        """  
        
        code = cell if cell.endswith('\n') else cell+'\n'
        lib_dir = os.path.join(self.shell.ipython_dir, 'tmp_cpp_magic')
        key = line, code, sys.version_info, sys.executable
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)

        module_name = "_cpp_magic_" + \
                      hashlib.md5(str(key).encode('utf-8')).hexdigest()
        c_name = module_name+'.cpp'
        o_name = module_name+'.o'

        c_path = os.path.join(lib_dir, c_name)
        o_path = os.path.join(lib_dir, o_name)

        if not os.path.exists(c_path):
            with io.open(c_path, 'w', encoding='utf-8') as f:
                f.write(code)

        if not os.path.exists(o_path):
            try:
                startupinfo = None
                if os.name == 'nt':
                    # Avoid a console window in Microsoft Windows.
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.check_output(['g++', c_name, "-o", o_name] + line.split(),
                                        stderr=subprocess.STDOUT,
                                        cwd=lib_dir,
                                        startupinfo=startupinfo)
                
            except subprocess.CalledProcessError as e:
                print(e.output, file=sys.stderr)
                print("ERROR: command `%s` failed." %
                      ' '.join(map(pipes.quote, e.cmd)),
                      file=sys.stderr)
                return
#        with io.open(o_path, 'rb') as f:
#            bitcode = f.read()
        try:
            program_output = subprocess.check_output(['./' + o_name],
                                        stderr=subprocess.STDOUT,
                                        cwd=lib_dir)
            print(program_output)
        except subprocess.CalledProcessError as e:
            print(e.output, file=sys.stderr)
            print("ERROR: command `%s` failed." %' '.join(map(pipes.quote, e.cmd)),file=sys.stderr)
            return

_loaded = False

def load_ipython_extension(ip):
    """Load the extension in IPython."""
    global _loaded
    if not _loaded:
        ip.register_magics(CppMagics)
        _loaded = True
