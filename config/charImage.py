import os.path

from lsst.utils import getPackageDir
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
from lsst.meas.algorithms import ColorLimit
from lsst.meas.astrom import MatchOptimisticBConfig

ObsConfigDir = os.path.join(getPackageDir("obs_subaru"), "config")

bgFile = os.path.join(ObsConfigDir, "background.py")

config.repair.cosmicray.nCrPixelMax = 1000000
config.repair.cosmicray.cond3_fac2 = 0.4
config.background.load(bgFile)
config.detection.background.load(bgFile)

config.measurePsf.reserve.fraction = 0.2
config.measurePsf.starSelector["objectSize"].sourceFluxField = 'base_PsfFlux_instFlux'

try:
    import lsst.meas.extensions.psfex.psfexPsfDeterminer
    config.measurePsf.psfDeterminer["psfex"].spatialOrder = 2
    config.measurePsf.psfDeterminer["psfex"].psfexBasis = 'PIXEL_AUTO'
    config.measurePsf.psfDeterminer["psfex"].samplingSize = 0.5
    config.measurePsf.psfDeterminer["psfex"].kernelSize = 81
    config.measurePsf.psfDeterminer.name = "psfex"
except ImportError as e:
    print("WARNING: Unable to use psfex: %s" % e)
    config.measurePsf.psfDeterminer.name = "pca"

config.catalogCalculation.plugins['base_ClassificationExtendedness'].fluxRatio = 0.95

config.detection.isotropicGrow = True

config.load(os.path.join(ObsConfigDir, "cmodel.py"))
config.measurement.load(os.path.join(ObsConfigDir, "apertures.py"))
config.measurement.load(os.path.join(ObsConfigDir, "kron.py"))
config.measurement.load(os.path.join(ObsConfigDir, "convolvedFluxes.py"))
config.measurement.load(os.path.join(ObsConfigDir, "hsm.py"))
if "ext_shapeHSM_HsmShapeRegauss" in config.measurement.plugins:
    # no deblending has been done
    config.measurement.plugins["ext_shapeHSM_HsmShapeRegauss"].deblendNChild = ""

config.deblend.maskLimits["NO_DATA"] = 0.25 # Ignore sources that are in the vignetted region
config.deblend.maxFootprintArea = 10000

config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]

if "ext_convolved_ConvolvedFlux" in config.measurement.plugins:
    names = config.measurement.plugins["ext_convolved_ConvolvedFlux"].getAllResultNames()
    config.measureApCorr.allowFailure += names


ObsConfigDir = os.path.join(getPackageDir("obs_subaru"), "config", "hsc")
config.measurePsf.starSelector["objectSize"].widthMin = 0.9
config.measurePsf.starSelector["objectSize"].fluxMin = 4000

matcher = config.ref_match.matcher

matcher.sourceSelector.active.sourceFluxType = 'Psf'
matcher.maxRotationDeg = 1.145916
matcher.maxOffsetPix = 250
if isinstance(matcher, MatchOptimisticBConfig):
    matcher.allowedNonperpDeg = 0.2
    matcher.maxMatchDistArcSec = 2.0

config.measurement.plugins["base_Jacobian"].pixelScale = 0.168
