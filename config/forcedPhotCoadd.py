import os.path

from lsst.utils import getPackageDir
from lsst.meas.base import CircularApertureFluxAlgorithm

# apertures.py

# Set up aperture photometry
# 'config' should be a SourceMeasurementConfig

config.measurement.plugins.names |= ["base_CircularApertureFlux"]
# Roughly (1.0, 1.4, 2.0, 2.8, 4.0, 5.7, 8.0, 11.3, 16.0, 22.6 arcsec) in diameter: 2**(0.5*i)
# (assuming plate scale of 0.168 arcsec pixels)
config.measurement.plugins["base_CircularApertureFlux"].radii = [3.0, 4.5, 6.0, 9.0, 12.0, 17.0, 25.0, 35.0, 50.0, 70.0]

# Use a large aperture to be independent of seeing in calibration
config.measurement.plugins["base_CircularApertureFlux"].maxSincRadius = 12.0

# kron.py

# Enable Kron mags
# 'config' is a SourceMeasurementConfig

try:
    import lsst.meas.extensions.photometryKron
    config.measurement.plugins.names |= ["ext_photometryKron_KronFlux"]
except ImportError:
    print("Cannot import lsst.meas.extensions.photometryKron: disabling Kron measurements")

# convolvedFluxes

try:
    import lsst.meas.extensions.convolved  # noqa: Load flux.convolved algorithm
except ImportError as exc:
    print("Cannot import lsst.meas.extensions.convolved (%s): disabling convolved flux measurements" % (exc,))
else:
    config.measurement.plugins.names.add("ext_convolved_ConvolvedFlux")
    config.measurement.plugins["ext_convolved_ConvolvedFlux"].seeing.append(8.0)

# cmodel.py

try:
    import lsst.meas.modelfit
    config.measurement.plugins.names |= ["modelfit_DoubleShapeletPsfApprox", "modelfit_CModel"]
    config.measurement.slots.modelFlux = 'modelfit_CModel'
    config.catalogCalculation.plugins['base_ClassificationExtendedness'].fluxRatio = 0.985
except (KeyError, ImportError):
    print("Cannot import lsst.meas.modelfit: disabling CModel measurements")

# forcedPhotCoadd remainder

config.measurement.slots.gaussianFlux = None

config.measurement.plugins['base_PixelFlags'].masksFpCenter.append('BRIGHT_OBJECT')
config.measurement.plugins['base_PixelFlags'].masksFpAnywhere.append('BRIGHT_OBJECT')

config.catalogCalculation.plugins.names = ["base_ClassificationExtendedness"]
config.measurement.slots.psfFlux = "base_PsfFlux"

def doUndeblended(config, algName, fluxList=None):
    """Activate undeblended measurements of algorithm

    Parameters
    ----------
    algName : `str`
        Algorithm name.
    fluxList : `list` of `str`, or `None`
        List of flux columns to register for aperture correction. If `None`,
        then this will be the `algName` appended with `_instFlux`.
    """
    if algName not in config.measurement.plugins:
        return
    if fluxList is None:
        fluxList = [algName + "_instFlux"]
    config.measurement.undeblended.names.add(algName)
    config.measurement.undeblended[algName] = config.measurement.plugins[algName]
    for flux in fluxList:
        config.applyApCorr.proxies["undeblended_" + flux] = flux


doUndeblended(config, "base_PsfFlux")
doUndeblended(config, "ext_photometryKron_KronFlux")
doUndeblended(config, "base_CircularApertureFlux", [])  # No aperture correction for circular apertures
doUndeblended(config, "ext_convolved_ConvolvedFlux",
              config.measurement.plugins["ext_convolved_ConvolvedFlux"].getAllResultNames())
# Disable registration for apCorr of undeblended convolved; apCorr will be done through the deblended proxy
config.measurement.undeblended["ext_convolved_ConvolvedFlux"].registerForApCorr = False
