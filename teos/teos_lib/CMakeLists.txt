set( LIB_NAME "teoslib" )

set( CONFIG_JSON "config.json" )
set( TEST_ADDRESS "tokenika")
set( TEST_HTTP_ADDRESS "eos-testapi.tokenika.io:8888" )

## BEGIN DEPENDENCIES ########################################################

set( Boost_USE_STATIC_LIBS ON )
set( Boost_USE_MULTITHREADED ON )
set( Boost_USE_STATIC_RUNTIME OFF )
set( BOOST_ROOT "$ENV{U_HOME}/opt/boost" )

find_package(Boost 1.67 REQUIRED COMPONENTS 
  thread  
  date_time   
  filesystem  
  system
  program_options
  chrono
  regex
  iostreams
)
if( Boost_FOUND )
  message( STATUS "Boost found.
  Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}" )
else( Boost_FOUND )
  message ( STATUS "Boost not found. set environment variables:
  BOOST_INCLUDEDIR (where is boost directory, usualy %BOOST_ROOT%)" )
endif( Boost_FOUND )

find_package(LLVM 4.0 REQUIRED CONFIG)
if( LLVM_FOUND )
  message( STATUS "LLVM found.
  LLVM_INCLUDE_DIR: ${LLVM_INCLUDE_DIR}
  LLVM_LIBRARY_DIR: ${LLVM_LIBRARY_DIR}")
else( LLVM_FOUND )
  message ( STATUS "LLVM not found. set environment variable:
  LLVM_ROOT_DIR (for example, %C_INCLUDE%/LLVM_4_0_1")
endif( LLVM_FOUND )
llvm_map_components_to_libnames(LLVM_LIBS support core passes mcjit native DebugInfoDWARF)

set(teoslib_src ${CMAKE_SOURCE_DIR}/../teos_lib)

if( NOT ECC_IMPL STREQUAL openssl )
  find_package(Secp256k1 REQUIRED)
  find_package(GMP REQUIRED)
endif()


file( GLOB HEADERS "include/teoslib/*.hpp" 
  "include/teoslib/command/*.hpp" "include/teoslib/control/*hpp" )
file( GLOB SRC "*cpp" "command/*.cpp" "control/*.cpp" )

add_library(${LIB_NAME} STATIC
  ${HEADERS}
  ${SRC}
  )

target_include_directories( ${LIB_NAME} 
  PRIVATE
    ${Boost_INCLUDE_DIRS}
  PUBLIC
    include
)

if( NOT EXISTS "${CMAKE_SOURCE_DIR}/${CONFIG_JSON}")
  file(WRITE "${CMAKE_SOURCE_DIR}/${CONFIG_JSON}" "{\n\n}")
endif()

configure_file (
  "config.h.in"
  "${CMAKE_SOURCE_DIR}/teos/include/teos/config.h"
)

configure_file (
  "config.h.in"
  "${CMAKE_SOURCE_DIR}/teos_lib/include/teoslib/config.h"
)

install ( TARGETS ${LIB_NAME} DESTINATION lib )
install( DIRECTORY include DESTINATION include )
install( FILES ${CONFIG_JSON_PATH} DESTINATION bin )
