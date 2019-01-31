import os.path
from lsst.utils import getPackageDir
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

config.measurement.load(os.path.join(getPackageDir("obs_subaru"), "config", "apertures.py"))
config.measurement.load(os.path.join(getPackageDir("obs_subaru"), "config", "kron.py"))
config.measurement.load(os.path.join(getPackageDir("obs_subaru"), "config", "convolvedFluxes.py"))
config.measurement.load(os.path.join(getPackageDir("obs_subaru"), "config", "hsm.py"))
config.load(os.path.join(getPackageDir("obs_subaru"), "config", "cmodel.py"))

config.match.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.match.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
config.match.refObjLoader.load(os.path.join(getPackageDir("obs_subaru"), "config", "filterMap.py"))

config.doWriteMatchesDenormalized = True

config.measurement.plugins["base_PixelFlags"].masksFpCenter.append("BRIGHT_OBJECT")
config.measurement.plugins["base_PixelFlags"].masksFpAnywhere.append("BRIGHT_OBJECT")

config.measurement.plugins.names |= ["base_InputCount"]

config.match.refObjLoader.load(os.path.join(getPackageDir("obs_subaru"), "config", "hsc",
                                            "filterMap.py"))

import lsst.obs.subaru.filterFraction
config.measurement.plugins.names.add("subaru_FilterFraction")
