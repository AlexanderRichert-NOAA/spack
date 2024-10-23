# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCfgrib(PythonPackage):
    """Python interface to map GRIB files to the NetCDF Common Data Model
    following the CF Convention using ecCodes."""

    homepage = "https://github.com/ecmwf/cfgrib"
    pypi = "cfgrib/cfgrib-0.9.8.5.tar.gz"

    license("Apache-2.0")

    version("0.9.10.4", sha256="b490078192aa13ec89c77296110355521442325866b16a996f4b3cf421542909")
    version("0.9.9.0", sha256="6ff0227df9c5ee34aa7d6ab1f7af3fbe6838523a8a9891c74040b419b03ad289")
    version("0.9.8.5", sha256="07c224d7ac823a1df5738b96b9d3621515538f51f67e55044f9cc8ec1668e1bd")

    # Warning: can create infinite dependency loop with xarray+io ^cfgrib+xarray
    variant("xarray", default=False, description="Add xarray support")

    depends_on("py-setuptools", type="build")
    depends_on("py-attrs@19.2:", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-eccodes@0.9.8:", when="@0.9.10:", type=("build", "run"))
    depends_on("py-eccodes", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-xarray@0.15:", when="@0.9.10:+xarray", type=("build", "run"))
    depends_on("py-xarray@0.12:", when="+xarray", type=("build", "run"))

    # Historical dependencies
    depends_on("py-pytest-runner", when="@0.9.8.5", type="build")
    depends_on("py-cffi", when="@0.9.8.5", type=("build", "run"))

    @property
    def import_modules(self):
        modules = ["cfgrib"]

        if "+xarray" in self.spec:
            modules.append("cf2cdm")

        return modules
