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

    version("7.15.1", tag="7.15.1")

    depends_on("gcc", type="build")

    variant("fismahigh", default=False, description="Apply modifications for FISMA-high compliance")

    def setup_build_environment(self, env):
        nawips = self.build_directory
        env.set("NAWIPS", nawips)
        env.set("EDEX_SERVER", "edex-cloud.unidata.ucar.edu"*self.spec.satisfies("~fismahigh"))
        env.set("USE_GFORTRAN","1")
        env.set("MAKEINC", "Makeinc.common")
        na_os = "linux64"
        env.set("NA_OS", na_os)
        env.set("GEM_COMPTYPE", "gfortran")
        # GEMPAK directory:
        gempak = f"{nawips}/gempak"
        env.set("GEMPAK", gempak)
        env.set("GEMPAKHOME", f"{nawips}/gempak")
        # CONFIGURATION directory
        env.set("CONFIGDIR", f"{nawips}/config")
        # System environmental variables 
        os_root = f"{nawips}/os/$NA_OS"
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

    def patch(self):
        filter_file("make -s distclean \)", " )", "extlibs/zlib/Makefile")
        filter_file('test "\$gcc" -eq 1', 'test 1', 'extlibs/zlib/zlib/configure')
        filter_file('test -z "\$CC"', 'test 1', 'extlibs/zlib/zlib/configure')

    def install(self, spec, prefix):
        install_tree("os/linux64", prefix)
