
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
    *out = a^b + b^a;
    printf("Overriding out = a^b + b^a. out = %d\n", out);
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
    printf("XORing the output buffer with value 0x25\n");
    printf( "Buffer Content before modification\n" );
    printf( "[ " );
    int i = 0;
    for( ;i < len-2; i++ )
        printf( "%x, ", *((byte*)buf+i) );
    if( len > 0 )
        printf( "%x ", *((byte*)buf+i) );
    printf( "]\n" );    
    
    for( int i = 0; i < len; i++ )
    {
        *((byte*)buf+i) ^= 0x25;
    }
    printf( "Buffer Content after modification\n" );
    printf( "[ " );
    i = 0;
    for( ; i < len-2; i++ )
        printf( "%x, ", *((byte*)buf+i) );
    if( len > 0 )
        printf( "%x ", *((byte*)buf+i) );
    printf( "]\n" );
}

void just_pointers_post( const void* pa, void* pb, lattice_error_t ret_value )
{
    // _post processing of parameters can be done here.

    clock_t start_t = clock();
    if ( (start_t % 3) == 1 )
    {
        printf("Original ret_val = %d\n", ret_val );
        ret_val = -1;
        printf("Original ret_val = %d\n", ret_val );
    }
    
}

void kitchen_sink_post( int a, const char* name, char* out_name, const void* buf, void* out_buf, size_t len, lattice_error_t ret_value )
{
    // _post processing of parameters can be done here.

    int i = 0;
    int stringlength = strlen( out_name );
    printf("\nDoubling the in string name - %s with length = %d\n" , out_name, stringlength);
    
    for(i = 0; i < len; i++ )
    {
        *(out_name+i+stringlength) = *(out_name+i);
    }
    *(out_name+ 2*stringlength) = '\0';
    
    stringlength = strlen( out_name );
    printf("\nAfter doubling the in string name - %s with length = %d\n" , out_name, stringlength);
 
    printf("\nConverting the output string to upper case\n");
    stringlength = strlen( out_name );
    for(int i = 0; i < stringlength; i++ )
    {
        if( out_name[i] >= 'a' )
            out_name[i] -= ('a'-'A');
    } 
    printf("out_name = %s\n", out_name);
}
