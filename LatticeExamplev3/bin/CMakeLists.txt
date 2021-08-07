add_executable(latticeexample main.c)
target_link_libraries(latticeexample lattice)

install(TARGETS latticeexample RUNTIME DESTINATION bin)
