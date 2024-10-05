# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gsi(CMakePackage):
    """Gridpoint Statistical Interpolation"""

    homepage = "https://www.example.com"
    url = "gsi"
    git = "https://github.com/NOAA-EMC/GSI"

    maintainers("AlexanderRichert-NOAA")

    license("LGPL-3.0-only", checked_by="AlexanderRichert-NOAA")

    version("develop", branch="develop")

    variant("gsi", default=True)
    variant("enkf", default=True, when="+gsi")
    variant("gsdcloud", default=False)
    variant("mgbf", default=True)
    variant("gsi_mode", default="GFS", values=("GFS", "Regional"), when="+gsi")
    variant("enkf_mode", default="GFS", values=("GFS", "WRF", "NMMB", "FV3REG"), when="+enkf")

    depends_on("mpi")
    depends_on("netcdf-fortran")
    depends_on("bacio")
    depends_on("sigio")
    depends_on("sfcio")
    depends_on("nemsio")
    depends_on("ncio")
    depends_on("sp")
    depends_on("w3emc")
    depends_on("lapack")
    wrfio_enkf_modes = ("WRF", "NMMB", "FV3REG")
    for mode in wrfio_enkf_modes:
        depends_on("wrf-io", when=f"enkf_mode={mode}")
    with when("+gsi"):
        depends_on("gsi-ncdiag")
        depends_on("ip")
        depends_on("bufr@:11")
        depends_on("crtm")
        depends_on("wrf-io", when="gsi_mode=Regional")


    def setup_build_environment(self, env):
        if self.spec.satisfies("+fix"):
            env.set("GSI_BINARY_SOURCE_DIR", join_path(self.stage.source_path, "gsifix"))

    def cmake_args(self):
        using_mkl = self.spec.satisfies("^[virtuals=lapack] intel-oneapi-mkl")
        args = [ 
            self.define_from_variant("BUILD_GSI", "gsi"),
            self.define_from_variant("BUILD_ENKF", "enkf"),
            self.define_from_variant("BUILD_GSDCLOUD", "gsdcloud"),
            self.define_from_variant("BUILD_MGBF", "mgbf"),
            self.define("ENABLE_MKL", using_mkl),
            self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
            self.define("CMAKE_Fortran_COMPILER", self.spec["mpi"].mpifc),
        ]
        return args
