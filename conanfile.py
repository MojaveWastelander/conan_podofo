from conans import ConanFile, CMake
from conans.tools import unzip, replace_in_file, download
import os
import shutil

class PoDoFoConan(ConanFile):
    name = "podofo"
    generators = "cmake"
    version = "0.9.4"
    settings = "os", "compiler", "build_type", "arch"
    options = {"enable_optional" : [True, False]}
    default_options = "enable_optional=False"
    exports = ["./cmake*"]
    license = "GPL2 or later"
    url = "http://podofo.sourceforge.net/index.html"
    
    def source(self):
        zip_file = "podofo-%s.tar.gz" % self.version
        download("http://sourceforge.net/projects/podofo/files/podofo/{0}/podofo-{0}.tar.gz/download".format(self.version), zip_file)
        unzip(zip_file)
            
    def requirements(self):
        self.requires("freetype/2.6.3@lasote/stable")
        self.requires("OpenSSL/1.0.2h@lasote/stable")
        self.requires("zlib/1.2.8@lasote/stable")
        self.requires("libpng/1.6.23@lasote/stable")
        self.requires("libjpeg-turbo/1.4.2@lasote/stable")
        self.requires("libtiff/4.0.6@bilke/stable")        
        
        if self.options.enable_optional:
            self.requires("cppunit/0.1@Coderdreams/testing")

    def build(self):
        replace_lines = '''PROJECT(PoDoFo CXX)
        
enable_language(C)        
include(../conanbuildinfo.cmake)
conan_basic_setup()
'''   
        folder_name = "podofo-%s" % self.version
        # add conan dependencies
        replace_in_file("%s/CMakeLists.txt" % folder_name, "PROJECT(PoDoFo)", replace_lines)
        
        # custom libcryto findlibcryto is based on looking for OpenSSL first
        replace_in_file("%s/CMakeLists.txt" % folder_name, "FIND_PACKAGE(OpenSSL)", "")
        replace_in_file("%s/CMakeLists.txt" % folder_name, "FIND_PACKAGE(LIBCRYPTO)", """FIND_PACKAGE(OpenSSL)
FIND_PACKAGE(LIBCRYPTO)""")
        
        # update search path with conan/cmake paths as well
        replace_in_file("%s/CMakeLists.txt" % folder_name, 'SET(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules")', 'SET(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules" ${CMAKE_MODULE_PATH})')

        # temp fix for msvc
        replace_in_file("%s/CMakeLists.txt" % folder_name, 'CHECK_TYPE_SIZE("__uint64"  SZ___UINT64)', 'CHECK_TYPE_SIZE("__int64"  SZ___UINT64)')
        
        cmake = CMake(self.settings)
        print("Compiler: %s %s" % (self.settings.compiler, self.settings.compiler.version))
        print("Arch: %s" % self.settings.arch)    

        # replace included FindXXX with updated ones or those already provided by conan
        shutil.rmtree("./%s/cmake" % folder_name)
        shutil.copytree("cmake", "./%s/cmake" % folder_name)
        
        self.run('cmake -DPODOFO_BUILD_LIB_ONLY=TRUE %s/%s %s' % (self.conanfile_directory, folder_name, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)


    def package(self):
        folder_name = "podofo-%s" % self.version
        self.copy("*", dst="include", src="%s/src" % folder_name)
        self.copy("*", dst="include/src", src="%s/src" % folder_name)
        self.copy("*", dst="include/podofo", src="%s/podofo" % folder_name)
        self.copy("podofo_config.h", dst="include", src=".")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.a", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["podofo"]
