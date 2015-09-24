import sys

from compilers1.parse_ula import parser
from compilers1.lex_ula import lexer

variables = []


def parse_ast(ast, line_no=1, file_handle=None):
    if len(ast) == 1:
        return
    elif ast[0] == 'Program':
        for line in ast[1:]:
            parse_ast(line, line_no, file_handle)
            line_no += 1
    else:
        if ast[0] == 'AssignStatement':
            parse_ast(ast[1], line_no, file_handle)
            return
        elif 'ID,' in ast[0]:
            if ast[0] in variables:
                print('semantic error on line %d' % line_no)
                # print('\tMulti Assigns of %s' % ast[0].replace('ID,', ''))
                if file_handle:
                    file_handle.write('semantic error on line %d\n' % line_no)
                return
            else:
                variables.append(ast[0])
                # print("Assign %s" % ast[0])
                parse_ast(ast[1], line_no, file_handle)
        elif ast[0] == 'IdentifierExpression':
            if ast[1][0] not in variables:
                print('semantic error on line %d' % line_no)
                # print('\t%s Not assigned' % ast[1][0].replace('ID,', ''))
                if file_handle:
                    file_handle.write('semantic error on line %d\n' % line_no)
                return
        elif 'Expression' in ast[0]:
            parse_ast(ast[1], line_no, file_handle)
            return
        for branch in ast[1]:
            parse_ast(branch, line_no, file_handle)


if __name__ == '__main__':
    ula_file = sys.argv[-1]
    # Check for argument
    if ula_file == sys.argv[0]:
        print('No ula file specified!')
    else:
        with open(ula_file) as open_file:
            in_data = open_file.read()
        # in_data = ''''''
        parsed_ula = parser.parse(in_data)
        # print(parsed_ula)

        with open(ula_file.replace('.ula', '.err'), 'w') as out_file:
            if parsed_ula and not (parser.p_error or lexer.l_error):
                parse_ast(parsed_ula, file_handle=out_file)
            else:
                if lexer.l_error:
                    print("lexical error on line %d" % lexer.lineno)
                    out_file.write("lexical error on line %d\n" % lexer.lineno)
                elif parser.p_error:
                    print("parse error on line %d" % lexer.lineno)
                    out_file.write("parse error on line %d\n" % lexer.lineno)
