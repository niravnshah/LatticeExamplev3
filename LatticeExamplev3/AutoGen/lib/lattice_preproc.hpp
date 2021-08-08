
// This is a pre/post processing stubs file. The code block will get replaced as it is in the original file.
// The parameters are for reference so that correct code can be written easily.
void simple_pre(  )
{
    // _pre processing of parameters can be done here.

}

void single_int_pre( int a )
{
    // _pre processing of parameters can be done here.
    a += 5;

}

void multiple_ints_pre( int a, int b, int c )
{
    // _pre processing of parameters can be done here.
    a = b+c;

}

void different_ints_pre( size_t s, uint32_t u, char c )
{
    // _pre processing of parameters can be done here.
    printf("size=%d, u = %u, c = %c", s, u, c);

}

void output_int_pre( int a, int b, int* out )
{
    // _pre processing of parameters can be done here.
    a += 3;
    b += 4;

}

void single_string_pre( const char* s )
{
    // _pre processing of parameters can be done here.

}

void multiple_strings_pre( const char* sa, const char* sb, const char* sc )
{
    // _pre processing of parameters can be done here.

}

void modify_string_pre( char* s )
{
    // _pre processing of parameters can be done here.
    
    printf("Reversing the string");
    int start = 0;
    int end = strlen(s) - 1;
    while( start < end )
    {
        char temp = s[start];
        s[start] = s[end];
        s[end] = temp;
        start++;
        end--;
    }
    printf("Reversed string = %s", s);
}

void single_buffer_pre( const void* buf, size_t len )
{
    // _pre processing of parameters can be done here.

}

void modify_buffer_pre( int a, void* buf, size_t len )
{
    // _pre processing of parameters can be done here.

}

void just_pointers_pre( const void* pa, void* pb )
{
    // _pre processing of parameters can be done here.
    printf("This function is going to fail randomly.");

}

void kitchen_sink_pre( int a, const char* name, char* out_name, const void* buf, void* out_buf, size_t len )
{
    // _pre processing of parameters can be done here.
    
    printf("XORing the input buffer with value 0x11\n");
    int i = 0;
    for( ; i < len; i++ )
    {
        *((byte*)out_buf+i) ^= 0x11;
    }
    

    
    printf("\nPrinting the parameters again...\n");
    kitchen_sink_param_logger( a, name, out_name, buf, out_buf, len );

}
