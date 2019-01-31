import sys
from lsst.daf.butler import Butler
butler = Butler(sys.argv[1], run=sys.argv[2])
for abstract_filter in ["r", "i"]:
    ref = butler.registry.find(collection="shared/ci_hsc", datasetType="brightObjectMask",
                               skymap="ci_hsc", tract=0, patch=69, abstract_filter=abstract_filter)
    butler.registry.associate(butler.collection, [ref])
