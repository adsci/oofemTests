cmake_minimum_required(VERSION 3.13)
project(oofemTests)
include(CMakePrintHelpers)

set (OOFEM_PATH "" CACHE FILEPATH "Path to OOFEM executable")

enable_testing()
file (GLOB_RECURSE testCase RELATIVE "${CMAKE_SOURCE_DIR}/cases/" "${CMAKE_SOURCE_DIR}/cases/*.in")
foreach (case ${testCase})
    get_filename_component(dir ${case} DIRECTORY)
    get_filename_component(name ${case} NAME)
    if (${name} STREQUAL "deepbeamFE2disp04.in" OR ${name} STREQUAL "deepbeamFE2dispslip02.in")
            add_test(NAME "${case}" WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/cases/${dir}" COMMAND ${OOFEM_PATH} "-f" ${name} -ksp_type preonly -pc_type lu -pc_factor_mat_solver_type mumps )
    else ()
        add_test(NAME "${case}" WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/cases/${dir}" COMMAND ${OOFEM_PATH} "-f" ${name} )
    endif ()
endforeach()