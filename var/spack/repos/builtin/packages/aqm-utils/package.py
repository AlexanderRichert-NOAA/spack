# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AqmUtils(CMakePackage):
    """Air Quality Model (AQM) utilities)"""

    homepage = "https://github.com/NOAA-EMC/AQM-utils"
    git = "https://github.com/NOAA-EMC/AQM-utils"

    maintainers("AlexanderRichert-NOAA")

    license("UNKNOWN", checked_by="AlexanderRichert-NOAA")

    version("develop", branch="develop")

    variant("post_stat", default=True)
    variant("openmp4", default=False, description="Patch code to only use OpenMP v4.x-compatible functions")

    depends_on("mpi")
    depends_on("netcdf-fortran")
    depends_on("g2")
    depends_on("w3emc")
    depends_on("w3nco")
    depends_on("bacio")
    depends_on("nemsio")
    with when("+post_stat"):
        depends_on("libpng")
        depends_on("zlib-api")
        depends_on("bufr")
        depends_on("jasper")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_POST_STAT", "post_stat"),
            self.define("CMAKE_INSTALL_BINDIR", "bin")
        ]
        return args

    @when("+openmp4")
    def patch(self):
        filter_file(r"^.+omp_get_num_teams.+$", "", "lib/lib.f90/print_omp_info.f90")
        filter_file(r"^.+omp_get_max_teams.+$", "", "lib/lib.f90/print_omp_info.f90")
        filter_file(r"^.+omp_display_env.+$", "", "lib/lib.f90/print_omp_info.f90")
