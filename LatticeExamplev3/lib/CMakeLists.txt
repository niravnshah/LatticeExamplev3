add_library(lattice lattice.c)
target_include_directories(lattice INTERFACE 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)
set_target_properties(lattice PROPERTIES PUBLIC_HEADER lattice.h)

install(TARGETS lattice
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION bin
)
install(FILES lattice.h DESTINATION include)
