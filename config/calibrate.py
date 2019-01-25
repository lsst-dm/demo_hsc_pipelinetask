import os
from lsst.utils import getPackageDir
from lsst.meas.algorithms import ColorLimit
from lsst.meas.astrom import MatchOptimisticBConfig
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

ObsConfigDir = os.path.join(getPackageDir("obs_subaru"), "config")

bgFile = os.path.join(ObsConfigDir, "background.py")
config.detection.background.load(bgFile)

config.astrometry.matcher.numBrightStars = 150

# Set to match defaults curretnly used in HSC production runs (e.g. S15B)
config.catalogCalculation.plugins['base_ClassificationExtendedness'].fluxRatio = 0.95

config.photoCal.applyColorTerms = True
config.photoCal.photoCatName = "ps1_pv3_3pi_20170110"
HscObsConfigDir = os.path.join(getPackageDir("obs_subaru"), "config", "hsc")
config.photoCal.colorterms.load(os.path.join(HscObsConfigDir, 'colorterms.py'))
colors = config.photoCal.match.referenceSelection.colorLimits
colors["g-r"] = ColorLimit(primary="g_flux", secondary="r_flux", minimum=0.0)
colors["r-i"] = ColorLimit(primary="r_flux", secondary="i_flux", maximum=0.5)
config.photoCal.match.referenceSelection.doMagLimit = True
config.photoCal.match.referenceSelection.magLimit.fluxField = "i_flux"
config.photoCal.match.referenceSelection.magLimit.maximum = 22.0

for refObjLoader in (config.astromRefObjLoader,
                     config.photoRefObjLoader,
                     ):
    refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
    refObjLoader.load(os.path.join(getPackageDir("obs_subaru"), "config", "filterMap.py"))
    refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"

for refObjLoader in (config.astromRefObjLoader, config.photoRefObjLoader):
    refObjLoader.load(os.path.join(HscObsConfigDir, "filterMap.py"))

# Demand astrometry and photoCal succeed
config.requireAstrometry = True
config.requirePhotoCal = True

config.doWriteMatchesDenormalized = True

# Detection
config.detection.isotropicGrow = True

config.measurement.load(os.path.join(ObsConfigDir, "apertures.py"))
config.measurement.load(os.path.join(ObsConfigDir, "kron.py"))
config.measurement.load(os.path.join(ObsConfigDir, "hsm.py"))

# Deblender
config.deblend.maxFootprintSize=0
config.deblend.maskLimits["NO_DATA"] = 0.25 # Ignore sources that are in the vignetted region
config.deblend.maxFootprintArea = 10000

config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]

config.astrometry.wcsFitter.numRejIter = 3
config.astrometry.wcsFitter.order = 3

matcher = config.astrometry.matcher
matcher.sourceSelector.active.sourceFluxType = 'Psf'
matcher.maxRotationDeg = 1.145916
matcher.maxOffsetPix = 250
if isinstance(matcher, MatchOptimisticBConfig):
    matcher.allowedNonperpDeg = 0.2
    matcher.maxMatchDistArcSec = 2.0
config.measurement.plugins["base_Jacobian"].pixelScale = 0.168
