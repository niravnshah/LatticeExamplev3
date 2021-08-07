import os, sys, re, ntpath, shutil,datetime


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
        match = re.match( r"DLLENTRY (.*?)\s*([^\s]*?)\s*\(\s*(.*?)\s*\)\s*;\s*(.*)", lines, flags=re.MULTILINE | re.DOTALL )
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

def gen_header( header_dir, header_name ):
    base_lib = os.path.join( header_dir, '..', 'build', 'lib', 'Debug', header_name + '_orig.dll')
    base_lib = base_lib.replace('\\','\\\\')
    str = ''
    #str += '//' + datetime.datetime.now().strftime("%H:%M:%S") + '\n'
    str += '#include <stdio.h>\n'
    str += '#include \"Windows.h\"\n'
    str += '#include \"' + header_name + '.h\"\n\n'

    str += '''
void* GetFunctionPointer( const char* func_name )
{
    static HMODULE lib = NULL;
    if( lib == NULL )\n'''
    str += '        lib = LoadLibraryEx( \"' + base_lib +'\", NULL, 0 );\n'
    str += '''
    void* pfnptr = NULL;
    if( lib )
        pfnptr = GetProcAddress( lib, func_name );
    return pfnptr;
}'''
    str += '\n\n'
    return str

def gen_func_header( func ):
        #paramstr = []
        #for param in func['params']:
        #    paramstr.append( param['type'] + ' ' + param['name'] )
        #str = func['ret_type'] + " " + func['fun_name'] + '( ' + ', '.join( paramstr ) + ' )'
    str = ''
    str += 'typedef ' + func['ret_type'] + ' ( *pfn_' + func['fun_name'] + ' ) ( ' + ', '.join( [ (param['type']) for param in func['params'] ] ) + ' );\n'
    str += func['ret_type'] + " " + func['fun_name'] + '( ' + ', '.join( [ (param['type'] + ' ' + param['name']) for param in func['params'] ] ) + ' )'
    str += '\n{\n'

    return str;


def gen_pre( func ):
    str = '    // This section is pre processing\n'
    
    str += '    printf(\"Entering ' + func['fun_name'] + '\\n\");\n'

    str += '\n'
    return str


def gen_post( func ):
    str = '    // This section is Post processing\n'
    
    str += '    printf(\"Exiting ' + func['fun_name'] + '\\n\");\n'

    str += '\n'
    return str


def gen_call( func ):
    str = '    '
    str += 'pfn_' + func['fun_name'] + ' fnptr = ( pfn_' + func['fun_name'] + ' )GetFunctionPointer( \"' + func['fun_name'] + '\" );\n'
    str += '    '
    if func['ret_type'] != 'void':
        str += func['ret_type'] + ' ret_val = '
    str += 'fnptr( ' + ', '.join( [ param['name'] for param in func['params'] ] ) + ' );\n'

    str += '\n'
    return str


def gen_return( func ):
    str = '    return'
    if func['ret_type'] != 'void':
        str += ' ret_val'
    str+= ';\n'
    str += '}\n'

    return str


def generate_code( funcs, header_dir, header_file, output_file ):

    fout = open(output_file, "w+")
    
    str = gen_header( header_dir, header_file )
    fout.writelines( str )

    for func in funcs:
        str = ''
        str += gen_func_header( func )
        str += gen_pre( func )
        str += gen_call( func )
        str += gen_post( func )
        str += gen_return( func )

        fout.writelines( str )

    fout.close()


def AutoGen():

    header_file = os.path.join('C:\\', 'NNS','Backup','VmVare','LatticeExamplev3','LatticeExamplev3','lib','lattice.h')
    header_dir = os.path.dirname( header_file );

    autogen_dir = os.path.join('.','lib')
    if not os.path.exists(autogen_dir):
        os.makedirs(autogen_dir)

    header_name = os.path.splitext(os.path.basename(header_file))[0]
    output_file = os.path.join( autogen_dir,header_name + '.c' )

    shutil.copy( header_file, os.path.join( autogen_dir ) )

    funcs = parse_file( header_file )

    generate_code( funcs, header_dir, header_name, output_file )

    print ( funcs )


if __name__ == "__main__":
    main()