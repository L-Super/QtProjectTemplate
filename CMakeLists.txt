cmake_minimum_required(VERSION 3.26)

project(QtProjectTemplate)

set(CMAKE_CXX_STANDARD 17)

option(BUILD_TEST "Build the demo" OFF)

# Set application version. For more details, see src/version.h.in
set(VERSION_MAJOR 1)
set(VERSION_MINOR 0)
set(VERSION_PATCH 0)

message(STATUS "This application's version is ${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}")

add_subdirectory(src)

if (BUILD_TEST)
    add_subdirectory(tests)
endif ()