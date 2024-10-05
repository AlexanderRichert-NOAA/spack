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

    variant("aqm", default=False, description="Use coupled AQM")

    depends_on("mpi")
    depends_on("ufs-weather-model app=ATM +32bit +ccpp_32bit +inline_post")
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
    depends_on("ufs-weather-model ccpp_suites=FV3_GFS_v16", when="+aqm")
    depends_on("ufs-utils")
    depends_on("upp")
    depends_on("gsi gsi_mode=Regional enkf_mode=FV3REG")

    root_cmakelists_dir = "sorc"

    resource(name="gsi", git="https://github.com/NOAA-EMC/GSI", commit="529b6ea", destination="sorc", placement="gsi")

    def cmake_args(self):
        args = [
          self.define("BUILD_UFS", False),
          self.define("BUILD_UFS_UTILS", False),
          self.define("BUILD_UPP", False),
          self.define("BUILD_GSI", True),
          self.define("BUILD_RRFS_UTILS", False),
          self.define("BUILD_AQM_UTILS", False),
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
        env.set("FV3_EXEC_FP", self.spec["ufs-weather-model"].prefix.bin.ufs_weather_model)
        env.set("UFS_UTILS_DIR", self.spec["ufs-utils"].prefix)
        env.set("CHGRES_CUBE_EXE", self.spec["ufs-utils"].prefix.bin.chgres_cube)
        env.set("MAKE_HGRID_EXE", self.spec["ufs-utils"].prefix.bin.make_hgrid)
        env.set("MAKE_SOLO_MOSAIC_EXE", self.spec["ufs-utils"].prefix.bin.make_solo_mosaic)
        env.set("FILTER_TOPO_EXE", self.spec["ufs-utils"].prefix.bin.filter_topo)
        env.set("FVCOM_TO_FV3_EXE", self.spec["ufs-utils"].prefix.bin.fvcom_to_FV3)
        env.set("GLOBAL_EQUIV_RESOL_EXE", self.spec["ufs-utils"].prefix.bin.global_equiv_resol)
        env.set("OROG_EXE", self.spec["ufs-utils"].prefix.bin.orog)
        env.set("OROG_GSL_EXE", self.spec["ufs-utils"].prefix.bin.orog_gsl)
        env.set("REGIONAL_ESG_GRID", self.spec["ufs-utils"].prefix.bin.regional_esg_grid)
        env.set("SFC_CLIMO_GEN", self.spec["ufs-utils"].prefix.bin.sfc_climo_gen)
        env.set("SHAVE", self.spec["ufs-utils"].prefix.bin.shave)
        env.set("UPP_EXE", join_path(self.spec["upp"].prefix.bin, "upp.x"))
