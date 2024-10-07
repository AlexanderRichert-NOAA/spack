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
        if self.spec.satisfies("+uwm"):
            env.set("FV3_EXEC_FP", self.spec["ufs-weather-model"].prefix.bin.ufs_weather_model)
        if self.spec.satisfies("+ufs_utils"):
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
        if self.spec.satisfies("+upp"):
            env.set("UPP_EXE", join_path(self.spec["upp"].prefix.bin, "upp.x"))
        if self.spec.satisfies("+gsi"):
            env.set("GSI_EXE", join_path(self.spec["gsi"].prefix.bin, "gsi.x"))
            env.set("ENKF_EXE", join_path(self.spec["gsi"].prefix.bin, "enkf.x"))
            env.set("NC_DIAG_CAT_EXE", join_path(self.spec["gsi-ncdiag"].prefix.bin, "nc_diag_cat.x"))
        if self.spec.satisfies("+rrfs_utl"):
            env.set("ADJUST_SOILTQ_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "adjust_soiltq.exe"))
            env.set("ENS_MEAN_RECENTER_P2DIO_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "ens_mean_recenter_P2DIO.exe"))
            env.set("FV3LAM_NONVARCLDANA_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "fv3lam_nonvarcldana.exe"))
            env.set("PROCESS_IMSSNOW_FV3LAM_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "process_imssnow_fv3lam.exe"))
            env.set("PROCESS_LARCCLD_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "process_larccld.exe"))
            env.set("PROCESS_LIGHTNING_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "process_Lightning.exe"))
            env.set("PROCESS_METARCLD_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "process_metarcld.exe"))
            env.set("PROCESS_NSSL_MOSAIC_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "process_NSSL_mosaic.exe"))
            env.set("PROCESS_PM_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "process_pm.exe"))
            env.set("PROCESS_UPDATESST_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "process_updatesst.exe"))
            env.set("REF2TTEN_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "ref2tten.exe"))
            env.set("RRFS_BUFR_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "rrfs_bufr.exe"))
            env.set("RRFS_SNDP_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "rrfs_sndp.exe"))
            env.set("RRFS_STNMLIST_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "rrfs_stnmlist.exe"))
            env.set("UPDATE_BC_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "update_bc.exe"))
            env.set("UPDATE_GVF_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "update_GVF.exe"))
            env.set("UPDATE_ICE_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "update_ice.exe"))
            env.set("USE_RAPHRRR_SFC_EXE", join_path(self.spec["rrfs-utl"].prefix.bin, "use_raphrrr_sfc.exe"))
        if self.spec.satisfies("+aqm"):
            env.set("GEFS2LBC_PARA", self.spec["aqm-utils"].prefix.bin.gefs2lbc_para)
