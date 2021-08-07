#include "lattice.h"

#include <stdio.h>
#include <string.h>

void simple()
{
    printf("[Base] simple()\n");
}

int single_int(int a)
{
    int ret = a + 5;
    printf("[Base] single_int(%d) -> %d\n", a, ret);
    return ret;
}

int multiple_ints(int a, int b, int c)
{
    int ret = a + b - c + 12;
    printf("[Base] multiple_ints(%d, %d, %d) -> %d\n", a, b, c, ret);
    return ret;
}

int different_ints(size_t s, uint32_t u, char c)
{
    int ret = s + 4 * u - 64 * c + 1024;
    printf("[Base] different_ints(%zu, %u, %d) -> %d\n", s, (unsigned int)u, (int)c, ret);
    return ret;
}

int output_int(int a, int b, int* out)
{
    int sum = a + b;
    int dif = a - b;
    printf("[Base] output_int(%d, %d) -> %d, %d\n", a, b, sum, dif);
    
    *out = dif;
    return sum;
}

lattice_error_t single_string(const char* s)
{
    int ret = strcmp(s, "hello");
    printf("[Base] single_string(%s) -> %d\n", s, ret);
    return ret;
}

lattice_error_t multiple_strings(const char* sa, const char* sb, const char* sc)
{
    int ret = (strcmp(sa, "hello") != 0) && (strcmp(sb, sc) != 0);
    printf("[Base] multiple_strings(%s, %s, %s) -> %d\n", sa, sb, sc, ret);
    return ret;
}

lattice_error_t modify_string(char* s)
{
    printf("[Base] modify_string(%s) -> ", s);
    
    for (char* c = s; *c != '\0'; ++c) {
        if ((*c > 96) && (*c < 123))
        {
            *c -= 32;
        }
    }
    
    printf("%s\n", s);
    return 0;
}

lattice_error_t single_buffer(const void *buf, size_t len)
{
    printf("[Base] single_buffer(%p, %zu)\n", buf, len);

    if (buf == NULL) {
        return -1;
    }
    else if (len == 0) {
        return -2;
    }
    else if (len > 1024) {
        return -3;
    }
    
    return 0;
}

lattice_error_t modify_buffer(int a, void *buf, size_t len)
{
    printf("[Base] modify_buffer(%p, %zu)\n", buf, len);

    if (buf == NULL) {
        return -1;
    }
    else if (len == 0) {
        return -2;
    }
    
    char* c = (char*)buf;
    for (size_t i = 0; i < len; ++i)
    {
        c[i] = (a + i) & 0xff;
    }

    return 0;
}

/* These are not buffers, but just pointers to random memory, and never read or written to */
lattice_error_t just_pointers(const void* pa, void* pb)
{
    printf("[Base] just_pointers(%p, %p)\n", pa, pb);
    return 0;
}

lattice_error_t kitchen_sink(int a, const char* name, char* out_name, const void* buf, void* out_buf, size_t len)
{
    printf("[Base] kitchen_sink(%d, %s, %p, %zu)\n", a, name, buf, len);

    if (name != NULL && out_name != NULL) {
        const char* c = name;
        char* o = out_name;
        for (c = name, o = out_name; *c != '\0' && *o != '\0'; ++c, ++o)
        {
            if ((*c > 96) && (*c < 123)) {
                *o = *c - 32;
            } else if ((*c > 64) && (*c < 91)) {
                *o = *c + 32;
            } else {
                *o = *c;
            }
        }
    }

    printf("[Base] kitchen_sink: %s -> %s\n", name, out_name);
    
    if (buf != NULL && out_buf != NULL && len != 0) {
        const char* bc = (const char*)buf;
        char* bo = (char*)out_buf;
        for (size_t i = 0; i < len; ++i) {
            bo[i] = (bc[i] + a) & 0xFF;
        }
    }
    
    return 0;
}

