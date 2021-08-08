
### AutoGen

cd AutoGen

python LatticeAutoGen.py <Full path to the header file> [-generateyaml]

cd ..


### Customization

On the first run of the script, the script generates the lattice_func_params.yaml under AutoGen/lib folder.

This yaml file should be modified to provide more details about various function parameter. esp, providing specialization of pointer type. More detail is provided in the existing yaml file.

On every modification of the lattice.h header, the python script should be run with -generateyaml option to generate new yaml.

The existing yaml will be renamed as lattice_func_params_old.yaml at the same location for reference.

After appropriate yaml modification, run the script without -generateyaml parameter to generate the interpose implementation.


### Build

mkdir build

cd build

cmake ..

cmake --build .


### Assumptions

- header file contains only function declarations and not function definitions.

- No macro usage in function definitions

- Header file is syntactically correct

- all function defintions have the parameter name given
    This is taken to avoid extensive C code parsing for user defined data types.
    
- no default arguments

- Any user defined data types would be either defined in the lattice.h or the definition would be part of any of the included headers.

- Any included file having relative path may not work

