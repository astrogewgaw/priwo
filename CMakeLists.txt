cmake_minimum_required(VERSION 3.15...3.27)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/")
include(DynamicVersion)
dynamic_version(PROJECT_PREFIX priwo_)

project(
  priwo
  LANGUAGES CXX
  VERSION ${PROJECT_VERSION}
  DESCRIPTION "I/O for common pulsar/FRB data formats."
)

include(CPM)
include(LTO)
include(Misc)
include(Colors)
include(ConfigSafeGuards)

find_lto(CXX)

CPMAddPackage("gh:TheLartians/PackageProject.cmake@1.8.0")
CPMAddPackage("gh:TheLartians/StaticTypeInfo@1.3.2")

add_library(
  ${PROJECT_NAME}
  ${PROJECT_SOURCE_DIR}/src/base.cc
  ${PROJECT_SOURCE_DIR}/src/sigproc/hdr.cc
  ${PROJECT_SOURCE_DIR}/src/sigproc/tim.cc
  ${PROJECT_SOURCE_DIR}/src/sigproc/fil.cc
  ${PROJECT_SOURCE_DIR}/src/presto/inf.cc
  ${PROJECT_SOURCE_DIR}/src/presto/dat.cc
  ${PROJECT_SOURCE_DIR}/src/presto/fft.cc
  ${PROJECT_SOURCE_DIR}/src/presto/pfd.cc
  ${PROJECT_SOURCE_DIR}/src/tempo/polycos.cc
  ${PROJECT_SOURCE_DIR}/include/priwo/base.h
  ${PROJECT_SOURCE_DIR}/include/priwo/sigproc/hdr.h
  ${PROJECT_SOURCE_DIR}/include/priwo/sigproc/tim.h
  ${PROJECT_SOURCE_DIR}/include/priwo/sigproc/fil.h
  ${PROJECT_SOURCE_DIR}/include/priwo/presto/inf.h
  ${PROJECT_SOURCE_DIR}/include/priwo/presto/dat.h
  ${PROJECT_SOURCE_DIR}/include/priwo/presto/fft.h
  ${PROJECT_SOURCE_DIR}/include/priwo/presto/pfd.h
  ${PROJECT_SOURCE_DIR}/include/priwo/tempo/polycos.h
)
set_target_properties(
  ${PROJECT_NAME}
  PROPERTIES CXX_STANDARD 17
             CXX_EXTENSIONS NO
             CXX_STANDARD_REQUIRED YES
             POSITION_INDEPENDENT_CODE ON
)
target_link_libraries(${PROJECT_NAME})
target_include_directories(
  ${PROJECT_NAME} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                         $<INSTALL_INTERFACE:include/${PROJECT_NAME}-${PROJECT_VERSION}>
)

string(TOLOWER ${PROJECT_NAME}/version.h VERSION_HEADER_LOCATION)
packageProject(
  NAME ${PROJECT_NAME}
  NAMESPACE ${PROJECT_NAME}
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion
  BINARY_DIR ${PROJECT_BINARY_DIR}
  INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include
  VERSION_HEADER "${VERSION_HEADER_LOCATION}"
  INCLUDE_DESTINATION include/${PROJECT_NAME}-${PROJECT_VERSION}
)

set(PYTHON_EXT_NAME core)
find_package(
  Python 3.10 REQUIRED
  COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule
)
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE
  OUTPUT_VARIABLE NB_DIR
)
list(APPEND CMAKE_PREFIX_PATH "${NB_DIR}")
find_package(nanobind CONFIG REQUIRED)
nanobind_add_module(${PYTHON_EXT_NAME} ${PROJECT_SOURCE_DIR}/python/priwo/bind.cc)
target_link_libraries(${PYTHON_EXT_NAME} PRIVATE ${PROJECT_NAME})
install(TARGETS ${PYTHON_EXT_NAME} LIBRARY DESTINATION ${PROJECT_NAME})
