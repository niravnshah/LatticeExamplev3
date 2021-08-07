#ifndef LATTICE_H
#define LATTICE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* A generic error type, 0 means success, nonzero values indicate an error */
typedef int lattice_error_t;
    
void simple();

int single_int(int a);
int multiple_ints(int a, int b, int c);
int different_ints(size_t s, uint32_t u, char c);
int output_int(int a, int b, int* out);

lattice_error_t single_string(const char* s);
lattice_error_t multiple_strings(const char* sa, const char* sb, const char* sc);

/* Modifies the string, but not past its strlen() */
lattice_error_t modify_string(char* s);

/* Takes a read-only input buffer buf with size len */
lattice_error_t single_buffer(const void *buf, size_t len);

/* Fills an output buffer buf up to size len */
lattice_error_t modify_buffer(int a, void *buf, size_t len);

/* These are not buffers, but just pointers to random memory, and never read or written to */
lattice_error_t just_pointers(const void* pa, void* pb);

/*
 * The output string out_name will be modified, but not past its strlen(). 
 * The buffers buf and out_buf will be read and written into, but not past len
 */
lattice_error_t kitchen_sink(int a, const char* name, char* out_name, const void* buf, void* out_buf, size_t len);

#ifdef __cplusplus
}
#endif

#endif // LATTICE_H
