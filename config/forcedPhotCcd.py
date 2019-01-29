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


# forcedPhotCoadd remainder

config.measurement.slots.gaussianFlux = None

# We haven't processed all the patches that overlap some of our CCDs
# to save some time.
config.references.skipMissing = True
