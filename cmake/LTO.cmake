macro(find_lto lang)
  if(ENABLE_LTO AND NOT LTO_${lang}_CHECKED)
    if(${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION} VERSION_LESS 3.9)
      cmake_policy(SET CMP0054 NEW)
      message(STATUS "Checking for LTO Compatibility")
      if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU"
           AND NOT CMAKE_GCC_AR
           OR NOT CMAKE_GCC_RANLIB
           OR NOT CMAKE_GCC_NM
        )
          find_program(
            CMAKE_GCC_AR
            NAMES "${_CMAKE_TOOLCHAIN_PREFIX}gcc-ar" "${_CMAKE_TOOLCHAIN_PREFIX}gcc-ar-${_version}"
            DOC "gcc provided wrapper for ar which adds the --plugin option"
          )
          find_program(
            CMAKE_GCC_RANLIB
            NAMES "${_CMAKE_TOOLCHAIN_PREFIX}gcc-ranlib"
                  "${_CMAKE_TOOLCHAIN_PREFIX}gcc-ranlib-${_version}"
            DOC "gcc provided wrapper for ranlib which adds the --plugin option"
          )
          # Not needed, but at least stay coherent
          find_program(
            CMAKE_GCC_NM
            NAMES "${_CMAKE_TOOLCHAIN_PREFIX}gcc-nm" "${_CMAKE_TOOLCHAIN_PREFIX}gcc-nm-${_version}"
            DOC "gcc provided wrapper for nm which adds the --plugin option"
          )
          mark_as_advanced(CMAKE_GCC_AR CMAKE_GCC_RANLIB CMAKE_GCC_NM)
          set(CMAKE_LTO_AR ${CMAKE_GCC_AR})
          set(CMAKE_LTO_RANLIB ${CMAKE_GCC_RANLIB})
          set(CMAKE_LTO_NM ${CMAKE_GCC_NM})
        endif()
        if("${CMAKE_CXX_COMPILER_ID}" MATCHES "Clang")
          set(CMAKE_LTO_AR ${CMAKE_AR})
          set(CMAKE_LTO_RANLIB ${CMAKE_RANLIB})
          set(CMAKE_LTO_NM ${CMAKE_NM})
        endif()
        if(CMAKE_LTO_AR AND CMAKE_LTO_RANLIB)
          set(__lto_flags -flto)

          if(NOT CMAKE_${lang}_COMPILER_VERSION VERSION_LESS 4.7)
            list(APPEND __lto_flags -fno-fat-lto-objects)
          endif()
          if(NOT DEFINED CMAKE_${lang}_PASSED_LTO_TEST)
            set(__output_dir "${CMAKE_PLATFORM_INFO_DIR}/LtoTest1${lang}")
            file(MAKE_DIRECTORY "${__output_dir}")
            set(__output_base "${__output_dir}/lto-test-${lang}")
            execute_process(
              COMMAND ${CMAKE_COMMAND} -E echo "void foo() {}"
              COMMAND ${CMAKE_${lang}_COMPILER} ${__lto_flags} -c -xc - -o "${__output_base}.o"
              RESULT_VARIABLE __result
              ERROR_QUIET OUTPUT_QUIET
            )
            if("${__result}" STREQUAL "0")
              execute_process(
                COMMAND ${CMAKE_LTO_AR} cr "${__output_base}.a" "${__output_base}.o"
                RESULT_VARIABLE __result
                ERROR_QUIET OUTPUT_QUIET
              )
            endif()
            if("${__result}" STREQUAL "0")
              execute_process(
                COMMAND ${CMAKE_LTO_RANLIB} "${__output_base}.a"
                RESULT_VARIABLE __result
                ERROR_QUIET OUTPUT_QUIET
              )
            endif()
            if("${__result}" STREQUAL "0")
              execute_process(
                COMMAND ${CMAKE_COMMAND} -E echo "void foo(); int main() {foo();}"
                COMMAND ${CMAKE_${lang}_COMPILER} ${__lto_flags} -xc - -x none "${__output_base}.a"
                        -o "${__output_base}"
                RESULT_VARIABLE __result
                ERROR_QUIET OUTPUT_QUIET
              )
            endif()
            if("${__result}" STREQUAL "0")
              set(__lto_found TRUE)
            endif()
            set(CMAKE_${lang}_PASSED_LTO_TEST
                ${__lto_found}
                CACHE INTERNAL "If the compiler passed a simple LTO test compile"
            )
          endif()
          if(CMAKE_${lang}_PASSED_LTO_TEST)
            message(STATUS "Checking for LTO Compatibility - works")
            set(LTO_${lang}_SUPPORT
                TRUE
                CACHE BOOL "Do we have LTO support ?"
            )
            set(LTO_COMPILE_FLAGS
                -flto
                CACHE STRING "Link Time Optimization compile flags"
            )
            set(LTO_LINK_FLAGS
                -flto
                CACHE STRING "Link Time Optimization link flags"
            )
          else()
            message(STATUS "Checking for LTO Compatibility - not working")
          endif()
        endif()
      elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
        message(STATUS "Checking for LTO Compatibility - works (assumed for clang)")
        set(LTO_${lang}_SUPPORT
            TRUE
            CACHE BOOL "Do we have LTO support ?"
        )
        set(LTO_COMPILE_FLAGS
            -flto
            CACHE STRING "Link Time Optimization compile flags"
        )
        set(LTO_LINK_FLAGS
            -flto
            CACHE STRING "Link Time Optimization link flags"
        )
      elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
        message(STATUS "Checking for LTO Compatibility - works")
        set(LTO_${lang}_SUPPORT
            TRUE
            CACHE BOOL "Do we have LTO support ?"
        )
        set(LTO_COMPILE_FLAGS
            /GL
            CACHE STRING "Link Time Optimization compile flags"
        )
        set(LTO_LINK_FLAGS
            -LTCG:INCREMENTAL
            CACHE STRING "Link Time Optimization link flags"
        )
      else()
        message(STATUS "Checking for LTO Compatibility - compiler not handled by module")
      endif()
      mark_as_advanced(LTO_${lang}_SUPPORT LTO_COMPILE_FLAGS LTO_LINK_FLAGS)

      set(LTO_${lang}_CHECKED
          TRUE
          CACHE INTERNAL ""
      )
      if(CMAKE_GCC_AR
         AND CMAKE_GCC_RANLIB
         AND CMAKE_GCC_NM
      )
        set(CMAKE_AR
            ${CMAKE_GCC_AR}
            CACHE FILEPATH "Forcing gcc-ar instead of ar" FORCE
        )
        set(CMAKE_NM
            ${CMAKE_GCC_NM}
            CACHE FILEPATH "Forcing gcc-nm instead of nm" FORCE
        )
        set(CMAKE_RANLIB
            ${CMAKE_GCC_RANLIB}
            CACHE FILEPATH "Forcing gcc-ranlib instead of ranlib" FORCE
        )
      endif()
    endif(${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION} VERSION_LESS 3.9)
  endif(ENABLE_LTO AND NOT LTO_${lang}_CHECKED)
  if(ENABLE_LTO)
    if(${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION} VERSION_LESS 3.9)
      if(LTO_${lang}_SUPPORT)
        if(NOT TARGET __enable_lto_tgt)
          add_library(__enable_lto_tgt INTERFACE)
        endif()
        target_compile_options(__enable_lto_tgt INTERFACE ${LTO_COMPILE_FLAGS})
        target_link_libraries(__enable_lto_tgt INTERFACE ${LTO_LINK_FLAGS})
        macro(target_enable_lto _target _build_configuration)
          if(${_build_configuration} STREQUAL "optimized" OR ${_build_configuration} STREQUAL
                                                             "debug"
          )
            target_link_libraries(${_target} PRIVATE ${_build_configuration} __enable_lto_tgt)
          else()
            target_link_libraries(${_target} PRIVATE __enable_lto_tgt)
          endif()
        endmacro()
      else()
        set(__IPO_SUPPORTED TRUE)
      endif()
    else()
      cmake_policy(SET CMP0069 NEW)
      include(CheckIPOSupported)
      check_ipo_supported(RESULT __IPO_SUPPORTED OUTPUT output)
      if(NOT __IPO_SUPPORTED)
        message(STATUS "IPO is not supported or broken.")
      else()
        message(STATUS "IPO is supported")
      endif()
    endif()
    if(__IPO_SUPPORTED)
      macro(target_enable_lto _target _build_configuration)
        if(NOT ${_build_configuration} STREQUAL "debug")
          set_target_properties(${_target} PROPERTIES INTERPROCEDURAL_OPTIMIZATION TRUE)
        endif()
        if(${_build_configuration} STREQUAL "optimized")
          set(__enable_debug_lto FALSE)
        else()
          set(__enable_debug_lto TRUE)
        endif()
        get_property(DEBUG_CONFIGURATIONS GLOBAL PROPERTY DEBUG_CONFIGURATIONS)
        if(NOT DEBUG_CONFIGURATIONS)
          set(DEBUG_CONFIGURATIONS DEBUG) # This is what is done by CMAKE internally... since
                                          # DEBUG_CONFIGURATIONS is empty by default
        endif()
        foreach(config IN LISTS DEBUG_CONFIGURATIONS)
          set_target_properties(
            ${_target} PROPERTIES INTERPROCEDURAL_OPTIMIZATION_${config} ${__enable_debug_lto}
          )
        endforeach()
      endmacro()
    endif()
  endif()
  if(NOT COMMAND target_enable_lto)
    macro(target_enable_lto _target _build_configuration)

    endmacro()
  endif()
endmacro()
