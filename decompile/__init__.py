'''
Decompiler module.

This module can decompile arbitrary code objects into a python ast. 
'''

from decompile.instructions import make_module, make_function

import _ast
import struct
import time
import sys
import marshal



def decompile_func(func):
    '''
    Decompile a function into ast.FunctionDef node.
    
    :param func: python function (can not be a built-in)
    
    :return: ast.FunctionDef instance.
    '''

    code = getattr(func, 'func_code', None)
    if code is None:
        raise TypeError('can not get ast from %r' % (func,))

    # For python 3
    defaults = func.func_defaults if sys.version_info.major < 3 else func.__defaults__
    if defaults:
        default_names = code.co_varnames[:code.co_argcount][-len(defaults):]
    else:
        default_names = []
    defaults = [_ast.Name(id='%s_default' % name, ctx=_ast.Load() , lineno=0, col_offset=0) for name in default_names]
    ast_node = make_function(code, defaults=defaults, lineno=code.co_firstlineno)

    return ast_node

def compile_func(ast_node, filename, globals, **defaults):
    '''
    Compile a function from an ast.FunctionDef instance.
    
    :param ast_node: ast.FunctionDef instance
    :param filename: path where function source can be found. 
    :param globals: will be used as func_globals
    
    :return: A python function object
    '''

    funcion_name = ast_node.name
    module = _ast.Module(body=[ast_node])

    ctx = {'%s_default' % key : arg for key, arg in defaults.items()}

    code = compile(module, filename, 'exec')

    eval(code, globals, ctx)

    function = ctx[funcion_name]

    return function


def decompile_pyc(bin_pyc, output=sys.stdout):
    '''
    decompile apython pyc or pyo binary file.
    
    :param bin_pyc: input file objects
    :param output: output file objects
    '''
    
    from asttools import python_source
    
    bin = bin_pyc.read()
    
    code = marshal.loads(bin[8:])
    
    mod_ast = make_module(code)
    
    python_source(mod_ast, file=output)
