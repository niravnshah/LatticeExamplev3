
// This is a pre/post processing stubs file. The code block will get replaced as it is in the original file.
// The parameters are for reference so that correct code can be written easily.
void simple_post(  )
{
    // _post processing of parameters can be done here.

}

void single_int_post( int a, int ret_value )
{
    // _post processing of parameters can be done here.

}

void multiple_ints_post( int a, int b, int c, int ret_value )
{
    // _post processing of parameters can be done here.

}

void different_ints_post( size_t s, uint32_t u, char c, int ret_value )
{
    // _post processing of parameters can be done here.

}

void output_int_post( int a, int b, int* out, int ret_value )
{
    // _post processing of parameters can be done here.

}

void single_string_post( const char* s, lattice_error_t ret_value )
{
    // _post processing of parameters can be done here.

}

void multiple_strings_post( const char* sa, const char* sb, const char* sc, lattice_error_t ret_value )
{
    // _post processing of parameters can be done here.

}

void modify_string_post( char* s, lattice_error_t ret_value )
{
    // _post processing of parameters can be done here.

}

void single_buffer_post( const void* buf, size_t len, lattice_error_t ret_value )
{
    // _post processing of parameters can be done here.

}

void modify_buffer_post( int a, void* buf, size_t len, lattice_error_t ret_value )
{
    // _post processing of parameters can be done here.

}

void just_pointers_post( const void* pa, void* pb, lattice_error_t ret_value )
{
    // _post processing of parameters can be done here.
    
    if ( ((int)pa % 2) == 1 )
    {
        ret_val = -1;
    }

}

void kitchen_sink_post( int a, const char* name, char* out_name, const void* buf, void* out_buf, size_t len, lattice_error_t ret_value )
{
    // _post processing of parameters can be done here.
    kitchen_sink_param_logger( a, name, out_name, buf, out_buf, len );    
    
    printf("XORing the output buffer with value 0x11\n");
    
    for( int i = 0; i < len; i++ )
    {
        *((byte*)out_buf+i) ^= 0x11;
    }
    
    printf("\nConverting the output string to upper case");
    
    int stringlength = strlen( out_name );
    for(int i = 0; i < len; i++ )
    {
        if( out_name[i] >= 'a' )
            out_name[i] -= ('a'-'A');
    }
    
    /*
    int stringlength = strlen( name );
    printf("\nDoubling the in string name - %s with length = %d" , name, stringlength);
    
    for(i = 0; i < len; i++ )
    {
        *(name+i+stringlength) = *(name+i);
    }
    
    stringlength = strlen( name );
    printf("\nDoubling the in string name - %s with length = %d" , name, stringlength);
    */
}
