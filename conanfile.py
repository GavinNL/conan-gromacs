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
    sha256 = "ac18cbf4ae9a22a22516351f5b5ce01dbd8cf0f4faaf36523c6ed2539ed4dcff"


    homepage = "http://www.gromacs.org/"

    ftp_address   = "ftp.gromacs.org"
    filename      = "gromacs-{0}.tar.gz".format(version)
    ftp_file_path = "pub/gromacs/{}".format(filename)

#    url_file_path = "ftp://ftp.gromacs.org/pub/contrib/xdrfile-1.1.4.tar.gz"
#    url_file_path = "ftp://ftp.gromacs.org/pub/contrib/xdrfile-{0}.tar.gz".format(version)
    #url_file_path = "{0}/archive/v{1}.tar.gz".format(homepage, version)
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
#        print("Downloading: " + self.url_file_path)
        tools.ftp_download(self.ftp_address, self.ftp_file_path)
#        tools.get(self.url_file_path, sha256=self.sha256)
        #tools.check_sha256(self.file_name, self.sha256)
        tools.untargz(self.filename)
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
            self.cpp_info.libs = ["gromacs_d"]
        else:
            self.cpp_info.libs = ["gromacs"]
        #self.env_info.ALSA_CONFIG_DIR = os.path.join(self.package_folder, "share", "alsa")
