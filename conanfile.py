from conans import ConanFile, tools, CMake
import os

#
# This is the conan recipe for libcci. This recipe is for the older
# version of cci which does not use Cmake or Git. The source is
# downloaded from ftp.
#
#
# This will need to be modified for the newer versions which use git
#
class gromacsConan(ConanFile):
    name = "gromacs"
    version = "2018.7"
    sha256 = "070fcd3e8a24e51479449aa2c823648d7161edb292431d841f2e67c1db6f36a2"


    homepage = "http://www.gromacs.org/"

    url_file_path = "http://ftp.gromacs.org/pub/gromacs/gromacs-{0}.tar.gz".format(version)
    filename      = "gromacs-{0}.tar.gz".format(version)

    generators = "cmake"

    license = "LGPL"
    url = "https://github.com/GavinNL/conan-gromacs"

    description = "GROMACS is a versatile package to perform molecular dynamics"

    options = { "shared": [True, False],
                "fPIC": [True, False],
                "precision": ["double", "single"]
                }

    default_options = { 'shared': True,
                        'fPIC': True,
                        'precision': 'single'
                        }

    settings = "os", "compiler", "build_type", "arch"
    build_policy = "missing"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    #requires = (
    #    "fftw/3.3.8@bincrafters/stable"
    #)

    def configure(self):
        pass
        #del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(self.url_file_path, sha256=self.sha256)
        os.rename("gromacs-{0}".format(self.version), self._source_subfolder)


    def _configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["GMX_BUILD_OWN_FFTW"] = True  # no need to build examples for conan package
        #cmake.definitions["DECAF_BUILD_EXAMPLES"] = False  # no need to build examples for conan package
        #cmake.definitions["DECAF_BUILD_TESTS"] = False  # no need to run tests for conan package
        #cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["GMX_DOUBLE"] = True if self.options.precision=="double" else False
        #print( self.deps_cpp_info["boost_serialization"].lib_paths )
        cmake.configure(build_folder=self._build_subfolder, source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        #self.copy(pattern="FindDecaf.cmake", dst="", src=os.path.join(self._source_subfolder,"cmake"))
        cmake = self._configure_cmake()
        cmake.install()
#    def package(self):
#        self.copy("*COPYING*", dst="licenses")

    def package_info(self):
        if self.options.precision=="double":
            self.cpp_info.libs = ["gromacs_d", "m", "dl"]
        else:
            self.cpp_info.libs = ["gromacs", "m", "dl"]
        #self.env_info.ALSA_CONFIG_DIR = os.path.join(self.package_folder, "share", "alsa")
