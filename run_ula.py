###
# Most of this was taken from the llvmlite example
# that can be found here:
# http://llvmlite.pydata.org/en/latest/binding/examples.html#compiling-a-trivial-function
###

import sys
from ctypes import CFUNCTYPE, c_float

import llvmlite.binding as llvm


# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one

def create_execution_engine():
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly('')
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    return mod


if __name__ == '__main__':
    ula_file = sys.argv[-1]
    # Check for argument
    if ula_file == sys.argv[0]:
        print('No ula file specified!')
    else:
        with open(ula_file) as open_file:
            in_data = open_file.read()

        engine = create_execution_engine()
        mod = compile_ir(engine, in_data)

        # Look up the function pointer (a Python int)
        func_ptr = engine.get_function_address('main')

        # Run the function via ctypes
        cfunc = CFUNCTYPE(c_float)(func_ptr)

        res = cfunc()

        print(res)
        with open(ula_file.replace('.ir', '.run'), 'w') as out_file:
            print(res, file=out_file)
