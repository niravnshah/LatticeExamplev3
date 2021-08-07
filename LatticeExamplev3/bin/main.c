#include <stdio.h>
#include <stdlib.h>

#include <lattice.h>

int main(int argc, char *argv[])
{
    simple();
    printf("[Test] simple\n");
    
    int ret;

    ret = single_int(4);
    printf("[Test] single_int: %d\n", ret);

    ret = multiple_ints(4, 14, 20);
    printf("[Test] multiple_ints: %d\n", ret);

    ret = different_ints(1024 * 1024, 256, 'u');
    printf("[Test] different_ints: %d\n", ret);

    int sum = 0, dif = 0;
    sum = output_int(100, 7, &dif);
    printf("[Test] output_int: %d, %d\n", sum, dif);
    
    ret = single_string("Hello, world!");
    printf("[Test] single_string: %d\n", ret);

    ret = multiple_strings("Yabba", "Dabba", "Doo");
    printf("[Test] multiple_strings: %d\n", ret);

    char s[] = "This is a short string.";
    ret = modify_string(s);
    printf("[Test] modify_string: %d, %s\n", ret, s);

    char buf[256];
    ret = single_buffer(buf, 256);
    printf("[Test] single_buffer: %d\n", ret);

    ret = modify_buffer(37, buf, 256);
    printf("[Test] modify_buffer: %d\n", ret);
    
    ret = just_pointers((void*)0x1234abcd, NULL);
    printf("[Test] just_pointers: %d\n", ret);
    
    char in_str[200] = "This is a small sample string.";
    char out_str[200] = "This is a small sample string. Which has another string after it";
    char in_buf[128];
    char out_buf[128];
    for (int c = 0; c < 128; ++c) {
        in_buf[c] = out_buf[c] = c;
    }
    ret = kitchen_sink(7, in_str, out_str, in_buf, out_buf, 64);
    printf("[Test] kitchen_sink: %d, %s, %d\n", ret, out_str, (int)out_buf[65]);

    
    return 0;
}
