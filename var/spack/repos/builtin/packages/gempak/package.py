import glob
import os

from spack.package import *


class Gempak(MakefilePackage):
    """GEMPAK/NAWIPSGEMPAK is an analysis, display, and product generation
    package for meteorological data. Originally developed by NCEP for use by the
    National Centers (SPC, TPC, AWC, HPC, OPC, SWPC, etc.) in producing operational
    forecast and analysis products. Members of the Unidata community maintain an
    open-source, non-operational release for use in the geoscience community.
    """

    homepage = "https://www.unidata.ucar.edu/software/gempak/"
    git = "https://github.com/Unidata/gempak"

    # maintainers("AlexanderRichert-NOAA")

    # license("BSD-3-Clause")

    version("7.18.0", tag="7.18.0")
    version("7.15.1", tag="7.15.1")

    parallel = False

    def setup_build_environment(self, env):
        nawips = self.build_directory
        env.set("NAWIPS", nawips)
        env.set("USE_GFORTRAN", "1")
        env.set("MAKEINC", "Makeinc.common")
        na_os = "linux64"
        env.set("NA_OS", na_os)
        # Always use gfortran config and patch for other compilers
        env.set("GEM_COMPTYPE", "gfortran")
        # GEMPAK directory:
        gempak = f"{nawips}/gempak"
        env.set("GEMPAK", gempak)
        env.set("GEMPAKHOME", f"{nawips}/gempak")
        # CONFIGURATION directory
        env.set("CONFIGDIR", f"{nawips}/config")
        # System environmental variables
        os_root = f"{nawips}/os/{na_os}"
        env.set("OS_ROOT", os_root)
        os_bin = f"{os_root}/bin"
        env.set("OS_BIN", os_bin)
        env.set("GEMEXE", os_bin)
        env.set("OS_INC", f"{os_root}/include")
        os_lib = f"{os_root}/lib"
        env.set("OS_LIB", os_lib)
        env.set("GEMLIB", os_lib)
        # Remaining directories used by GEMPAK  (leave as is):
        env.set("GEMPDF", f"{gempak}/pdf")
        env.set("GEMTBL", f"{gempak}/tables")
        env.set("GEMERR", f"{gempak}/error")
        env.set("GEMHLP", f"{gempak}/help")
        env.set("GEMMAPS", f"{gempak}/maps")
        gemnts = f"{gempak}/nts"
        env.set("GEMNTS", gemnts)
        env.set("GEMPARM", f"{gempak}/parm")
        env.set("GEMPTXT", f"{gempak}/txt/programs")
        env.set("GEMGTXT", f"{gempak}/txt/gemlib")
        env.set("NMAP_RESTORE", f"{gemnts}/nmap/restore")
        #  MEL_BUFR environment
        env.set("MEL_BUFR", f"{nawips}/extlibs/melBUFR/melbufr")
        env.set("MEL_BUFR_TABLES", f"{gempak}/tables/melbufr")
        # Add NAWIPS to the X applications resource path.
        env.prepend_path("XUSERFILESEARCHPATH", f"{nawips}/resource/%N")
        # Set PATH to include $OS_BIN and $PYHOME
        env.prepend_path("PATH", os_bin)
        env.prepend_path("PATH", f"{nawips}/bin")
        env.prepend_path("LD_LIBRARY_PATH", os_lib)
        env.set("OS", na_os)

    def build(self, spec, prefix):
        make("everything")

    def patch(self):
        makeinc = "config/Makeinc.linux64_gfortran"
        if self.spec.satisfies("%intel"):
            filter_file(
                "-fno-second-underscore -fno-range-check -fd-lines-as-comments",
                "-assume byterecl -extend-source -fpscomp logicals -nofor-main -assume byterecl",
                makeinc,
            )
        filter_file("^CC = .+", "CC = %s" % self.compiler.cc_names[0], makeinc)
        filter_file("^FC = .+", "FC = %s" % self.compiler.fc_names[0], makeinc)
        filter_file(
            "^(COPT = .+)", r"\1 %s" % " ".join(self.spec.compiler_flags["cflags"]), makeinc
        )
        filter_file(
            "^(FOPT = .+)", r"\1 %s" % " ".join(self.spec.compiler_flags["fflags"]), makeinc
        )
        filter_file(r"make -s distclean \)", " )", "extlibs/zlib/Makefile")
        filter_file(r'test "\$gcc" -eq 1', "test 1", "extlibs/zlib/zlib/configure")
        filter_file(r'test -z "\$CC"', "test 1", "extlibs/zlib/zlib/configure")
        filter_file(".*setenv NAWIPS .*", "", "Gemenviron")
        filter_file(r"\bln -s\b", "ln -s --force", "config/Makeinc.common")
        glob1 = glob.glob("gempak/source/programs/*/*/Makefile")
        glob2 = glob.glob("gempak/source/programs/upc/programs/*/Makefile")
        glob3 = glob.glob("gempak/source/contrib/*/*/Makefile")
        for f in glob1 + glob2 + glob3:
            filter_file(r"^(\$\(PROG[^\)]*\).*)\$\(LIBINC[^\)]*\)", r"\1", f)
        filter_file(
            r"^all : \$\(LIBINC\) \$\(PROG\)",
            "all : $(PROG)",
            "gempak/source/programs/gd/gdcsv/Makefile",
        )

    def install(self, spec, prefix):
        install_tree("os/linux64", prefix)
        install_tree("gempak", prefix.gempak)
        built_exes = os.listdir(self.spec.prefix.bin)
        target_exes = (
            "atest",
            "gdcntr",
            "gddelt",
            "gddiag",
            "gdinfo",
            "gdplot2_nc",
            "gdvint",
            "gpend",
            "nagrib2",
            "snedit",
        )
        missing_exes = [exe for exe in target_exes if exe not in built_exes]
        if missing_exes:
            raise InstallError("Not all executables were installed: %s" % ", ".join(missing_exes))

    def setup_run_environment(self, env):
        env.set("NAWIPS", self.prefix)
        env.set("GEMPAK", self.prefix.gempak)
        env.prepend_path("PATH", self.prefix.bin)
        env.set("GEMEXE", self.prefix.bin)
        env.set("OS_BIN", self.prefix.bin)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
