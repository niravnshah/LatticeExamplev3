import os, sys, re


def main():
    
    AutoGen()

def parse_file( file ):
    fin = open(file, "r")

    fullfile = fin.read()
    fin.close()
    fullfile = re.sub(r"([^/]*)(//.*)", r"\1",  fullfile) # remove single line comments
    
    # remove multiline comments
    match = 1
    while( match ):
        match = re.match(r"(.*?)/\*(.*?)\*/(.*)", fullfile, flags=re.MULTILINE | re.DOTALL)
        if match:
            fullfile = re.sub(r"(.*?)/\*(.*?)\*/(.*)",r"\1\3", fullfile, flags=re.MULTILINE | re.DOTALL)

    lines = fullfile.split('\n')

    lines = [line.strip() for line in lines if line.strip()]   # exclude empty lines
    lines = [line for line in lines if line[0] != '#'] # exclude #define, #include, #ifdef, ... pre processors

    separator = '\n'
    lines = separator.join( lines ) + '\n'
    funcs = []

    while ( lines ):
        # exclude any non functional lines
        match = 1
        while( match ):
            match = re.match( r"([^\(]*?)\n(.*)", lines, flags=re.MULTILINE | re.DOTALL )
            if match:
                lines = re.sub( r"([^\(]*?)\n(.*)",r"\2", lines, flags=re.MULTILINE | re.DOTALL )

        # match the function definition over multiple lines.
        match = re.match( r"(.*?)\s*([^\s]*?)\s*\(\s*(.*?)\s*\)\s*;\s*(.*)", lines, flags=re.MULTILINE | re.DOTALL )
        if match:
            params = [ s.strip() for s in match.group(3).replace("\n","").split(',') if s.strip() ]
            newparams = []

            # standardize the pointer usage in the parameter
            for param in params:
                str = [ p.strip() for p in param.split(' ') ]
                if str[-1][0] == '*':
                    str[-1] = str[-1][1:]
                    str[-2] = str[-2] + '*'

                newparams.append( { 'name' : str[-1], 'type' : ' '.join( str[0:-1] ) } )

            funcs.append({'ret_type' : match.group(1).replace("\n",""),
                          'fun_name' : match.group(2).replace("\n",""), 
                          'params' : newparams } )

            # TODO: extract parameter names to determine if parameter name is given in the definition or not
            # excluding this as of now, as this would require extensive C parsing for C keywords and user defined data types to differentiate between a parameter name or a keyword/UDD

            lines = re.sub( r"(.*?)\s*([^\s]*?)\s*\(\s*(.*?)\s*\)\s*;\s*(.*)", r"\4", lines, flags=re.MULTILINE | re.DOTALL )

    return funcs

def gen_header( func ):
        #paramstr = []
        #for param in func['params']:
        #    paramstr.append( param['type'] + ' ' + param['name'] )
        #str = func['ret_type'] + " " + func['fun_name'] + '( ' + ', '.join( paramstr ) + ' )'
    str = func['ret_type'] + " " + func['fun_name'] + '( ' + ', '.join( [ (param['type'] + ' ' + param['name']) for param in func['params'] ] ) + ' )'
    str += '\n{\n    '

    return str;


def gen_call( func ):
    str = ''
    if func['ret_type'] != 'void':
        str += func['ret_type'] + ' ret_val = '
    str += func['fun_name'] + '( ' + ', '.join( [ param['name'] for param in func['params'] ] ) + ' );\n'

    return str


def gen_return( func ):
    str = '    return'
    if func['ret_type'] != 'void':
        str += ' ret_val'
    str+= ';\n'
    str += '}\n'

    return str


def generate_code( funcs, file ):

    fout = open(file, "w+")
    for func in funcs:
        str = ''
        str += gen_header( func )
        str += gen_call( func )
        str += gen_return( func )

        fout.write( str )
        fout.write("\n")

    fout.close()


def AutoGen():

    input_file = "lattice.h"
    output_file = "lattice.c"

    funcs = parse_file( input_file )

    generate_code( funcs, output_file )

    print ( funcs )


if __name__ == "__main__":
    main()