cmake_minimum_required(VERSION 3.15)
project(dataloading_optimizations)

if (COMMAND cmake_policy)
    cmake_policy(SET CMP0003 NEW)
endif (COMMAND cmake_policy)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lz")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -DDEBUG")

add_compile_options("$<$<CONFIG:DEBUG>:-DDEBUG>")

option(ENABLE_STATIC "Build static (.a) library" ON)

find_package(ZLIB REQUIRED)

include_directories(${ZLIB_INCLUDE_DIRS})

include_directories(../cnpy)
include_directories(.)
include_directories(../fast-cpp-csv-parser)

add_library(cnpy SHARED ../cnpy/cnpy.cpp ../global.cc)
target_link_libraries(cnpy ${ZLIB_LIBRARIES})

add_executable(main
        ../cnpy/cnpy.h
        ../fast-cpp-csv-parser/csv.h
        global.h
        parse.h
        get_criteo_ad_data.h
        process_one_file.h
        process_criteo_ad_data.h
        concat_criteo_ad_data.h
        get_criteo_ad_data.cc
        process_one_file.cc
        process_criteo_ad_data.cc
        concat_criteo_ad_data.cc
        global.cc
        main.cc)

set(THREADS_PREFER_PTHREAD_FLAG ON)

find_package(Threads REQUIRED)

target_link_libraries(main Threads::Threads cnpy)
