cmake_minimum_required( VERSION 3.5.1 )

project( sensor )

find_package( Threads )
include_directories( include )
file( GLOB SOURCES "src/*" )
set( CMAKE_RUNTIME_OUTPUT_DIRECTORY "../bin" )
set( CMAKE_CXX_STANDARD 11 )

add_executable( testSensor ${SOURCES} )
target_link_libraries( testSensor ${CMAKE_THREAD_LIBS_INIT} )
