
### AutoGen

cd AutoGen

python LatticeAutoGen.py <Full path to the header file>

cd ..


### Customization

On the first run of the script, the script generates the lattice_func_params.yaml, lattice_preproc.hpp and lattice_postproc.hpp under AutoGen/lib folder.

This yaml file should be modified to provide more details about various function parameter. esp, providing specialization of pointer type. More detail is provided in the existing yaml file.
This hpp files should be modified to provide pre and post processing work or any function. If nothing to be done, then those functions can be left blank.

On every modification of the lattice.h header, the python script should be run with *-force* option to generate new yaml and hpp files.

The existing yaml and hpp will be renamed as *_old. at the same location for reference.

After appropriate yaml and hpp modification, run the script without -force parameter to generate the interpose implementation.


### AutoGen Again

cd AutoGen

python LatticeAutoGen.py <Full path to the header file>

cd ..


### Build

mkdir build

cd build

cmake ..

cmake --build .


### Run

.\bin\Debug\latticeexample.exe


### CmakeLists changes

The existing lattice lib is converted to SHARED lib so that it can be loaded dynamically
The name of the lib is also changed to lattice_orig so that the interpose layer lib can be generated with lattice name and be linked statically to the latticeexample project without any change to it.
The interpose lib is a static lib with name as lattice.

DLLEXPORT declarations are added in the lattice.h file to have proper function pointers exposed for windows DLL.

### Prerequisites

- Python 3.9
- Cmake


### Assumptions

- The solution is tested to be working with Windows and python 3.9

- header file contains only function declarations and not function definitions.

- No macro usage in function definitions

- Header file is syntactically correct

- all function defintions have the parameter name given
    This is taken to avoid extensive C code parsing for user defined data types.
    
- no default arguments

- Any user defined data types would be either defined in the lattice.h or the definition would be part of any of the included headers.

- Any included file having relative path may not work



### Examples

- Reverse all strings before calling the functions
    Done in modify_string

- Randomly return an error even though the function succeeded
    Done in just_pointers

- XOR input and output buffers against some constant value
    input buffer modification done in single_buffer
    output buffer modification done in modify buffer
    
- Double all strings (append another copy of the string at the end of each string)
    Done in kitchen_sink
    
- Search all buffers for certain patterns (byte sequences that look look like as pointers, integers, or strings) and log them
    Done in single_buffer
    
- Perform search-and-replace on strings
    Done in kitchen_sink