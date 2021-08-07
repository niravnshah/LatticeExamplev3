#[[ Need to change the project name as the base library is a shared runtime lib now ]]
add_library(lattice_orig SHARED lattice.c)
target_include_directories(lattice_orig INTERFACE 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)
set_target_properties(lattice_orig PROPERTIES PUBLIC_HEADER lattice.h)
add_compile_definitions(DLL_EXPORT)
install(TARGETS lattice_orig
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION bin
)
install(FILES lattice.h DESTINATION include)
