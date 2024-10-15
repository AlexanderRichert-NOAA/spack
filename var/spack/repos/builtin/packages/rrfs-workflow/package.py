# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RrfsWorkflow(CMakePackage):
    """This package provides the Rapid Refresh Forecast System (RRFS) workflow."""

    homepage = "https://gsl.noaa.gov/focus-areas/unified_forecast_system/rrfs"
    git = "https://github.com/AlexanderRichert-NOAA/rrfs-workflow"

    maintainers("AlexanderRichert-NOAA")

    version("dev-sci", branch="dev-sci-spackify")

    variant("uwm", default=True, description="Use UFS Weather Model")
    variant("ufs_utils", default=True, description="Use UFS utilities")
    variant("upp", default=True, description="Use UPP")
    variant("gsi", default=True, description="Use GSI")
    variant("rrfs_utl", default=True, description="Use RRFS utilities")
    variant("aqm", default=True, description="Use coupled AQM")

    depends_on("mpi")
    with when("+uwm"):
        depends_on("ufs-weather-model +32bit +ccpp_32bit +inline_post")
        ccpp_suites = [
            "FV3_HRRR",
            "FV3_HRRR_gf",
            "FV3_HRRR_gf_nogwd",
            "FV3_RAP",
            "FV3_GFS_v15_thompson_mynn_lam3km",
            "FV3_RRFS_v1beta",
            "FV3_GFS_v16",
            "RRFSens_phy1",
            "RRFSens_phy2",
            "RRFSens_phy3",
            "RRFSens_phy4",
            "RRFSens_phy5",
            "RRFS_sas",
            "RRFS_sas_nogwd",
        ]
        depends_on("ufs-weather-model ccpp_suites=%s" % ",".join(ccpp_suites), when="~aqm")
        depends_on("ufs-weather-model app=ATMAQ ccpp_suites=FV3_GFS_v16", when="+aqm")
    depends_on("ufs-utils", when="+ufs_utils")
    depends_on("upp", when="+upp")
    depends_on("gsi +gsi +enkf gsi_mode=Regional enkf_mode=FV3REG", when="+gsi")
    depends_on("gsi-ncdiag", when="+gsi")
    depends_on("rrfs-utl", when="+rrfs_utl")
    depends_on("aqm-utils", when="+aqm")

    root_cmakelists_dir = "sorc"

    def cmake_args(self):
        args = [
          self.define("BUILD_UFS", False),
          self.define("BUILD_UFS_UTILS", False),
          self.define("BUILD_UPP", False),
          self.define("BUILD_GSI", False),
          self.define("BUILD_RRFS_UTILS", False),
          self.define("BUILD_AQM_UTILS", False),
          self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
          self.define("CMAKE_Fortran_COMPILER", self.spec["mpi"].mpifc),
        ]
        return args

    def install(self, spec, prefix):
        install_tree("doc", prefix.doc)
        install_tree("fix", prefix.fix)
        install_tree("jobs", prefix.fix)
        install_tree("parm", prefix.parm)
        install_tree("scripts", prefix.scripts)
        install_tree("tests", prefix.tests)
        install_tree("ush", prefix.ush)
        install_tree("versions", prefix.versions)

    def setup_run_environment(self, env):
        if self.spec.satisfies("+ufs_utils"):
            env.set("UFS_UTILS_DIR", self.spec["ufs-utils"].prefix)
