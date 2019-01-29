import sys
from lsst.daf.butler import Butler
butler = Butler(sys.argv[1], run=sys.argv[2])
skyMapRef = butler.registry.find(collection="shared/ci_hsc", datasetType="deepCoadd_skyMap", skymap="ci_hsc")
butler.registry.associate(butler.collection, [skyMapRef])
