cmake_minimum_required(VERSION 3.15)
project(dataloading_optimizations)

if(COMMAND cmake_policy)
    cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lz")

option(ENABLE_STATIC "Build static (.a) library" ON)

find_package(ZLIB REQUIRED)

include_directories(${ZLIB_INCLUDE_DIRS})

include_directories(../cnpy)
include_directories(.)
include_directories(../fast-cpp-csv-parser)

add_executable(dataloading_optimizations
        ../cnpy/cnpy.h
        main.cc
        ../fast-cpp-csv-parser/csv.h)

set(THREADS_PREFER_PTHREAD_FLAG ON)

find_package(Threads REQUIRED)

target_link_libraries(dataloading_optimizations Threads::Threads)
