# This is not a full standalone CMake configuration for the hello world
# example.
#
# To build it outside the PoDoFo source tree, you must set your build system
# make the PoDoFo headers available and must link to the PoDoFo library
# and any libraries it depends on (see the README,
#     "5. Using PoDoFo in Your Application") .
#
# Note that you don't need the headers for PoDoFo's dependencies in your
# header search path.
project(podofo_test CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

ADD_EXECUTABLE(podofo_test CreationTest.cpp)

TARGET_LINK_LIBRARIES(podofo_test ${CONAN_LIBS})

if (WIN32)
    TARGET_LINK_LIBRARIES(podofo_test "Ws2_32.lib")
endif(WIN32)

if (UNIX)
	TARGET_LINK_LIBRARIES(podofo_test pthread fontconfig)
endif(UNIX)

SET_TARGET_PROPERTIES(podofo_test PROPERTIES COMPILE_FLAGS "${PODOFO_CFLAGS}")
INCLUDE_DIRECTORIES(${PoDoFo_SOURCE_DIR})
