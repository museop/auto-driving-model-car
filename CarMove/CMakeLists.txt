cmake_minimum_required( VERSION 3.5.1 )
project( carMove )
set(CMAKE_BUILD_TYPE Release)

include_directories( include )

file( GLOB SOURCES "*.cpp" )

add_library(carMove SHARED ${SOURCES})

