import logging
import re

from bbpyp.common.util.collection_util import CollectionUtil

# Since Python 3.7, re.Pattern was introduced to expose the type of
# compiled regular expression objects. Prior to this change, compiled
# regular expression objects were not deeply copyable.
#
# see: https://bugs.python.org/issue30397
pattern_type = re.Pattern if hasattr(re, 'Pattern') else type(re.compile(''))
CollectionUtil.add_types_to_deepcopy_direct_assignment_list(logging.Logger, pattern_type)
