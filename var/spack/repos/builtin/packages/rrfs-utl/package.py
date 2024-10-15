# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class RrfsUtl(CMakePackage):
    """Rapid Refresh Forecast System (RRFS) utilities"""

    homepage = "https://www.example.com"
    git = "https://github.com/NOAA-GSL/rrfs_utl"

    maintainers("AlexanderRichert-NOAA")

    license("UNKNOWN", checked_by="AlexanderRichert-NOAA")

    version("develop", branch="develop")

    depends_on("fortran", type="build")

    depends_on("mpi")
    depends_on("netcdf-fortran")
    depends_on("jasper")
    depends_on("libpng")
    depends_on("zlib-api")
    depends_on("bacio")
    depends_on("sp")
    depends_on("ip@:4")
    depends_on("g2")
    depends_on("g2tmpl")
    depends_on("w3nco")
    depends_on("w3emc")
    depends_on("bufr")
    depends_on("wrf-io")
    depends_on("gsi-ncdiag")
    depends_on("gsi")

    def patch(self):
        files_stop_patch = [
            "cloudanalysis.fd/get_fv3sar_bk_parallel_mod.f90",
            "rtma_esg_conversion.fd/mod_rtma_regrid.F90",
            "rtma_esg_conversion.fd/rtma_regrid_rll2esg.F90",
            "rtma_esg_conversion.fd/rtma_regrid_esg2rll.F90"
        ]
        for filetopatch in files_stop_patch:
            filter_file(r"stop\(", "stop (", filetopatch)
        filter_file("-fp-model precise -assume byterecl -convert big_endian", "-fconvert=big-endian", "radmon.fd/CMakeLists.txt")
        filter_file("==", ".eqv.", "rtma_minmaxtrh.fd/mintbg.fd/maxmin_ak.f")
        filter_file("==", ".eqv.", "rtma_minmaxtrh.fd/maxtbg.fd/maxmin_ak.f")
        filter_file(r"\(1x,D\)", "(1x,D10.3)", "rtma_esg_conversion.fd/rtma_regrid_esg2rll.F90")

    def setup_dependent_run_environment(self, env, dependent_spec):
        for exe_name in os.listdir(self.prefix.bin):
            env_name = exe_name.replace("-", "_").replace(".", "_").upper()
            env.set(env_name, join_path(self.prefix.bin, exe_name))
