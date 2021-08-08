import os, sys, re, ntpath, shutil,datetime, yaml
from yaml.loader import SafeLoader

def main():
    AutoGen()

def parse_file( file ):
    print( '\nParsing the file.. ' + file )
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

                newparams.append( { 'name' : str[-1], 'type' : ' '.join( str[0:-1] ), 'inout': '', 'pointertype': '', 'arraysizeparam': '', 'arrayelementstride': '' } )

            funcs.append({'fun_name' : match.group(2).replace("\n",""), 
                          'ret_type' : match.group(1).replace("\n",""),
                          'params' : newparams } )

            # TODO: extract parameter names to determine if parameter name is given in the definition or not
            # excluding this as of now, as this would require extensive C parsing for C keywords and user defined data types to differentiate between a parameter name or a keyword/UDD

            lines = re.sub( r"(.*?)\s*([^\s]*?)\s*\(\s*(.*?)\s*\)\s*;\s*(.*)", r"\4", lines, flags=re.MULTILINE | re.DOTALL )

    return funcs

def gen_header( header_dir, header_name, base_lib ):

    log_name = 'logfile.log'
    str = ''
    str += '//' + datetime.datetime.now().strftime("%H:%M:%S") + '\n'
    str += '#include <stdio.h>\n'
    str += '#include \"Windows.h\"\n'
    str += '#include \"' + header_name + '.h\"\n\n'

    str += '''
FILE* logfile = NULL;

void log( const char* str )
{
    fprintf( logfile, "%s", str );
}
void log_longlong( const long long ll )
{
    fprintf( logfile, "%lld", ll );
}
void log_ulonglong( const unsigned long long ull )
{
    fprintf( logfile, "%llu", ull );
}
void log_longdouble( const long double ld )
{
    fprintf( logfile, "%Lf", ld );
}
void log_char( const char c )
{
    fprintf( logfile, "%c", c );
}
void log_ptr( const void* vp )
{
    fprintf( logfile, "%p", vp );
}
void log_longlong_arr( const long long* ll, int size )
{
    fprintf( logfile, "[ " );
    int i = 0;
    for( ; i < size-2; i++ )
        fprintf( logfile, "%lld, ", *(ll+i) );
    if( size > 0 )
        fprintf( logfile, "%lld ", *(ll+i) );
    fprintf( logfile, "]" );
}
void log_ulonglong_arr( const unsigned long long* ull, int size )
{
    fprintf( logfile, "[ " );
    int i = 0;
    for( ; i < size-2; i++ )
        fprintf( logfile, "%llu, ", *(ull+i) );
    if( size > 0 )
        fprintf( logfile, "%llu ", *(ull+i) );
    fprintf( logfile, "]" );
}
void log_longdouble_arr( const long double* ld, int size )
{
    fprintf( logfile, "[ " );
    int i = 0;
    for( ; i < size-2; i++ )
        fprintf( logfile, "%LF, ", *(ld+i) );
    if( size > 0 )
        fprintf( logfile, "%LF ", *(ld+i) );
    fprintf( logfile, "]" );
}
void log_char_arr( const char* c, int size )
{
    fprintf( logfile, "[ " );
    int i = 0;
    for( ; i < size-2; i++ )
        fprintf( logfile, "%c, ", *(c+i) );
    if( size > 0 )
        fprintf( logfile, "%c ", *(c+i) );
    fprintf( logfile, "]" );
}
void log_ptr_arr( const void* vp, int size, int stride )
{
    fprintf( logfile, "[ " );
    int i = 0;
    for( ; i < size-2; i++ )
        fprintf( logfile, "%x, ", *((byte*)vp+i) );
    if( size > 0 )
        fprintf( logfile, "%x ", *((byte*)vp+i) );
    fprintf( logfile, "]" );
}
void log_start( const char* str )
{
    if( logfile == NULL )
        logfile = fopen( "''' + log_name + '''", "a+" );
    if( str != NULL )
        fprintf( logfile, "\\n%s\\n", str );
}
void log_end( const char* str )
{
    if( str != NULL )
        fprintf( logfile, "%s\\n", str );
    if( logfile != NULL )
    {
        fclose( logfile );
        logfile = NULL;
    }
}
'''

    str += '''
void* get_base_library_symbol( const char* func_name )
{
    static HMODULE lib = NULL;
    if( lib == NULL )
        lib = LoadLibraryEx( "'''+ base_lib +'''", NULL, 0 );

    void* pfnptr = NULL;
    if( lib )
        pfnptr = GetProcAddress( lib, func_name );
    return pfnptr;
}
'''
    str += '\n'
    return str

def gen_func_header( func, prepost, isref ):
        #paramstr = []
        #for param in func['params']:
        #    paramstr.append( param['type'] + ' ' + param['name'] )
        #str = func['ret_type'] + " " + func['fun_name'] + '( ' + ', '.join( paramstr ) + ' )'
    str = '\n'
    return_param = ''
    if prepost != '':
        return_type = 'void '
        if prepost == '_post':
            if func['ret_type'] != 'void':
                return_param = ', ' + func['ret_type'] + '& ret_value'
    else:
        return_type = func['ret_type'] + " "

    str += return_type + func['fun_name'] + prepost + '( ' + ', '.join( [ (param['type'] + isref +' ' + param['name']) for param in func['params'] ] ) + return_param + ' )'
    str += '\n{'

    return str;


def param_log( param ):
    ints = ['short','short int','signed short','signed short int','int','signed','signed int','long','long int','signed long','signed long int','long long','long long int','signed long long','signed long long int','size_t','int8_t','int16_t','int32_t','int64_t',]
    uints = ['unsigned short','unsigned short int','unsigned','unsigned int','unsigned long','unsigned long int','unsigned long long','unsigned long long int','uint8_t,','uint16_t','uint32_t','uint64_t']
    chars = ['char','signed char','unsigned char']
    floats = ['float','double','long double']

    str = '\n    log("\\n  ' + param['name'] + ' = ");'
        
    pointertype = 0
    arraysizeparam = ''
    param_type = param['type']
    param_type = param_type.lower().replace('const','').strip()
    if param_type[-1] == '*':
        pointertype = 1
        param_type = param_type.replace('*','')
        log_fun = 'log_ptr'

        

    if param_type in ints:
        log_fun = 'log_longlong'
    elif param_type in uints:
        log_fun = 'log_ulonglong'
    elif param_type in floats:
        log_fun = 'log_longdouble'
    elif param_type in chars:
        if param['pointertype'] == 'string':
            log_fun = 'log'
            pointertype = 0
        else:
            log_fun = 'log_char'

    if pointertype:
        if param['arraysizeparam'] != '':
            log_fun += '_arr'
            arraysizeparam = param['arraysizeparam']
        elif param['pointertype'] == 'value':
            log_fun += '_arr'
            arraysizeparam = '1'
        else:
            log_fun = 'log_ptr'


    str += '\n    ' + log_fun + '( ' + param['name']
    if arraysizeparam != '':
        str += ', ' + arraysizeparam
    if log_fun == 'log_ptr_arr':
        str += ' , ' + param['arrayelementstride']
    
    str += ' );'

    return str

def gen_param_logger( func ):
    str = ''
    if len(func['params']) > 0:
        str += '\nvoid ' + func['fun_name'] + '_param_logger' + '( ' + ', '.join( [ (param['type'] + ' ' + param['name']) for param in func['params'] ] ) + ' )'
        str += '\n{'
        for param in func['params']:
            str += param_log( param )
        str += '\n    return;'
        str += '\n}\n'

    return str

def gen_pre( func ):

    str = ''    
    str += '\n    log_start(\"Enter : ' + func['fun_name'] + '\");'

    if len(func['params']) > 0:
        str += '\n\n    log(\"Params before function call:\");'
    #for param in func['params']:
    #    str += param_log( param )
        str += '\n    ' + func['fun_name'] + '_param_logger( ' + ', '.join( [ param['name'] for param in func['params'] ] ) + ' );'

    str += '\n\n    // This section is pre processing'
    #str += '\n    ' + func['fun_name'] + '_pre( ' + ', '.join( [ param['name'] for param in func['params'] ] ) + ' );'
    return str


def gen_post( func ):
    str = '\n\n    // This section is Post processing\n'

    if len(func['params']) > 0:
        str += '\n    log(\"\\nParams after function call:\");'
    #for param in func['params']:
    #    str += param_log( param )
        str += '\n    ' + func['fun_name'] + '_param_logger( ' + ', '.join( [ param['name'] for param in func['params'] ] ) + ' );'

    str += '\n    log_end(\"\\nExit  : ' + func['fun_name'] + '\");'
    return str


def gen_call( func ):
    str = '\n\n    log( "\\nBase function call : ' + func['fun_name'] + '" );'
    str += '\n    typedef ' + func['ret_type'] + ' ( *pfn_' + func['fun_name'] + ' ) ( ' + ', '.join( [ (param['type']) for param in func['params'] ] ) + ' );'
    str += '\n    pfn_' + func['fun_name'] + ' base_function = ( pfn_' + func['fun_name'] + ' ) get_base_library_symbol( \"' + func['fun_name'] + '\" );'
    str += '\n    '
    if func['ret_type'] != 'void':
        str += func['ret_type'] + ' ret_val = '
    str += 'base_function( ' + ', '.join( [ param['name'] for param in func['params'] ] ) + ' );'

    return str


def gen_return( func, prepost ):
    str = '\n    return'
    if prepost == '':
        if func['ret_type'] != 'void':
            str += ' ret_val'
    str+= ';'
    str += '\n}\n'

    return str


def generate_code( funcs, header_dir, header_file, base_lib, output_file ):
    print( 'Generating code for.. ' + output_file)
    fout = open(output_file, "w+")
    
    str = gen_header( header_dir, header_file, base_lib )
    fout.writelines( str )

    for func in funcs:
        str = ''
        str += gen_param_logger( func )
        str += gen_func_header( func, '', '' )
        str += gen_pre( func )
        str += gen_call( func )
        str += gen_post( func )
        str += gen_return( func, '' )

        fout.writelines( str )

    fout.close()

def generate_pre_post_code( funcs, header_dir, header_file, base_lib, output_file, prepost ):
    output_file = os.path.splitext(output_file)[0] + prepost + 'proc.hpp'
    print( 'Generating ' + prepost + ' processing code code for.. ' + header_file + ' -> ' + output_file )
    fout = open(output_file, "w+")
    
    #str = gen_header( header_dir, header_file, base_lib )
    #fout.writelines( str )

    for func in funcs:
        str = ''
        str += gen_func_header( func, prepost ,'&' )
        #str += gen_pre( func )
        #str += gen_call( func )
        #str += gen_post( func )
        str += gen_return( func, prepost )

        fout.writelines( str )

    fout.close()

class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def generate_func_params_yaml( funcs, autogen_dir, header_name, force_gen_yaml ):

    old_yaml = os.path.join( autogen_dir, header_name + '_func_params_old.yaml' )
    yml = os.path.join( autogen_dir, header_name + '_func_params.yaml' )
    
    if not os.path.exists( yml ):
        force_gen_yaml = True;

    if force_gen_yaml:
        if os.path.exists( old_yaml ):
            os.remove( old_yaml )

        if os.path.exists( yml ):
            os.rename( yml, old_yaml )

        print( '\nGenerating paramter yaml at ' + yml ) 
        print( 'Modify the yaml file and run the script without -generateyaml parameter to load the updated yaml' )
    
        fout = open( yml, "w+" )

        str = ''
        str += '''
# Syntax:
#
# "functions:" [optional]
#     List of functions
#
#     "fun_name: <name>"
#         Name of the function
#
#     "ret_type: <name>"
#         Name of the function#
#
#     "params:"
#         List of params
#
#         "name: <parameter name>"
#
#         "type: <datatype>"
#
#         "inout: <in/out/inout>"
#             if the parameter is in or out or inout param.
#
#         "pointertype: <array/string/value/pointer>"
#             string - if a char* is a string
#             array - if the pointer points to the first element of an array. arraysizeparam should be populated for array to get logged.
#             value - if the pointer is used to pass a value. Logger will show the value at the address.
#             pointer - just an address. Logger will log the address.
#
#         "arraysizeparam: <arraysize parameter name>"
#             if the param is a pointer type and it is an array of that type; which parameter denotes the size of that array. this parameter is a must for pointertype = array else the parameter will not be logged
#
#         "arrayelementstride: <No of bytes of each of the elements of the array>"
#             if the param is a void pointer type and it is an array of that type; this paramenter tells the number of bytes of each of the element of the array. Hex values will be logged.
#
#==========================================================================

'''
        fout.write( str )
        fout.write( yaml.dump(funcs, Dumper=MyDumper, sort_keys=False) )
        fout.close()
        exit(0)
    else:
        print( '\nReading yaml from ' + yml )

    with open( yml ) as f:
        data = yaml.load(f, Loader=SafeLoader)

    return data


def AutoGen():

    if( len(sys.argv) > 3 ):
        print( 'Usage: python LatticeAutoGen.py <Full path to header> [-generateyaml]' )
        exit(-1)

    #header_file = os.path.join('C:\\', 'NNS','Backup','VmVare','LatticeExamplev3','LatticeExamplev3','lib','lattice.h')
    header_file = sys.argv[1]
    if not os.path.exists(header_file):
        print( 'File not found - ' + header_file )
        print( 'Usage: python LatticeAutoGen.py <Full path to header> [-generateyaml]' )
        exit(-1)

    if not os.path.isabs( header_file ):
        print( 'Path is not absolute.. ' )
        print( 'Usage: python LatticeAutoGen.py <Full path to header> [-generateyaml]' )
        exit(-1)

    header_dir = os.path.dirname( header_file );
    header_name = os.path.splitext(os.path.basename(header_file))[0]

    # TODO: Base lib path and name should be customized.
    base_lib = os.path.join( header_dir, '..', 'build', 'lib', 'Debug', header_name + '_orig.dll')
    base_lib = base_lib.replace('\\','\\\\')

    autogen_dir = os.path.join('.','lib')
    if not os.path.exists(autogen_dir):
        os.makedirs(autogen_dir)
    output_file = os.path.join( autogen_dir,header_name + '.c' )

    shutil.copy( header_file, os.path.join( autogen_dir ) )

    funcs = parse_file( header_file )

    force_gen_yaml = 0
    if ( len(sys.argv) == 3 ): 
        force_gen_yaml = ( sys.argv[2] == '-generateyaml')
        if not force_gen_yaml:
            print( 'Invalid Arg..' )
            print( 'Usage: python LatticeAutoGen.py <Full path to header> [-generateyaml]' )
            exit( -1 )


    funcs = generate_func_params_yaml( funcs, autogen_dir, header_name, force_gen_yaml )

    #parse_yaml( )

    generate_code( funcs, header_dir, header_name, base_lib, output_file )
    generate_pre_post_code( funcs, header_dir, header_name, base_lib, output_file, '_pre' )
    generate_pre_post_code( funcs, header_dir, header_name, base_lib, output_file, '_post' )

    print( 'Done.' )


if __name__ == "__main__":
    main()