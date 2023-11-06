cmake_minimum_required(VERSION 3.26)
project(QtProjectTemplate)

set(CMAKE_CXX_STANDARD 17)

option(BUILD_TEST "Build the demo" OFF)

add_subdirectory(src)

if (BUILD_TEST)
    add_subdirectory(tests)
endif ()