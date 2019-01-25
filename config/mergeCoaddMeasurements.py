# A filter priority list is needed for merging.  The one in obs_subaru
# uses physical filter names, but that doesn't seem to work in Gen3:
#  KeyError: "Field with name 'merge_peak_HSC-I2' not found"
# Because of that, use the abstract filter names here.

config.priorityList = ['i', 'r']
