import logging
from re import _pattern_type

from bbpyp.common.util.collection_util import CollectionUtil

CollectionUtil.add_types_to_deepcopy_direct_assignment_list(logging.Logger, _pattern_type)
