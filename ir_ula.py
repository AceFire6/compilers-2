import sys
from llvmlite import ir

from compilers1.parse_ula import parser

last_var = ''
var_dict = {}


def gen_ula_code(ast):
    global last_var
    if ast[0] == 'Program':
        for branch in ast[1:]:
            gen_ula_code(branch)
    elif ast[0] == 'AssignStatement':
        last_var = ast[1][0].replace('ID,', '')
        var_dict[last_var] = builder.alloca(float_literal)
        builder.store(gen_ula_code(ast[1][1]), var_dict[last_var])
    elif ast[0] == 'AddExpression':
        return builder.fadd(gen_ula_code(ast[1]), gen_ula_code(ast[2]))
    elif ast[0] == 'SubExpression':
        return builder.fsub(gen_ula_code(ast[1]), gen_ula_code(ast[2]))
    elif ast[0] == 'MulExpression':
        return builder.fmul(gen_ula_code(ast[1]), gen_ula_code(ast[2]))
    elif ast[0] == 'DivExpression':
        return builder.fdiv(gen_ula_code(ast[1]), gen_ula_code(ast[2]))
    elif ast[0] == 'FloatExpression':
        return ir.Constant(
            float_literal, float(ast[1][0].replace('FLOAT_LITERAL,', '')))
    elif ast[0] == 'IdentifierExpression':
        return builder.load(var_dict[ast[1][0].replace('ID,', '')])


float_literal = ir.FloatType()
function = ir.FunctionType(float_literal, ())

module = ir.Module(name='ula')
main = ir.Function(module, ftype=function, name='main')

block = main.append_basic_block('entry')
builder = ir.IRBuilder(block)

if __name__ == '__main__':
    ula_file = sys.argv[-1]
    # Check for argument
    if ula_file == sys.argv[0]:
        print('No ula file specified!')
    else:
        with open(ula_file) as open_file:
            in_data = open_file.read()

        parsed_ula = parser.parse(in_data)
        gen_ula_code(parsed_ula)

        builder.ret(builder.load(var_dict[last_var]))

        print(module)
        with open(ula_file.replace('.ula', '.ir'), 'w') as out_file:
            print(module, file=out_file)

