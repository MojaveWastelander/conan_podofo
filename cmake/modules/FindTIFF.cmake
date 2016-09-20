# - Find TIFF library
# Find the native TIFF includes and library
# This module defines
#  TIFF_INCLUDE_DIR, where to find tiff.h, etc.
#  TIFF_LIBRARIES, libraries to link against to use TIFF.
#  TIFF_FOUND, If false, do not try to use TIFF.
# also defined, but not for general use are
#  TIFF_LIBRARY, where to find the TIFF library.

find_path(TIFF_INCLUDE_DIR NAMES tiff.h PATHS ${CONAN_INCLUDE_DIRS_LIBTIFF})
find_library(TIFF_LIBRARY NAMES ${CONAN_LIBS_LIBTIFF} PATHS ${CONAN_LIB_DIRS_LIBTIFF})

MESSAGE("** TIFF ALREADY FOUND BY CONAN!")
SET(TIFF_FOUND TRUE)
MESSAGE("** FOUND TIFF:  ${TIFF_LIBRARY}")
MESSAGE("** FOUND TIFF INCLUDE:  ${TIFF_INCLUDE_DIR}")

set(TIFF_INCLUDE_DIRS ${TIFF_INCLUDE_DIR})
set(TIFF_LIBRARIES ${TIFF_LIBRARY})

mark_as_advanced(TIFF_LIBRARY TIFF_INCLUDE_DIR)