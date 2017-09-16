INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PHYSEC physec)

FIND_PATH(
    PHYSEC_INCLUDE_DIRS
    NAMES physec/api.h
    HINTS $ENV{PHYSEC_DIR}/include
        ${PC_PHYSEC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PHYSEC_LIBRARIES
    NAMES gnuradio-physec
    HINTS $ENV{PHYSEC_DIR}/lib
        ${PC_PHYSEC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PHYSEC DEFAULT_MSG PHYSEC_LIBRARIES PHYSEC_INCLUDE_DIRS)
MARK_AS_ADVANCED(PHYSEC_LIBRARIES PHYSEC_INCLUDE_DIRS)

