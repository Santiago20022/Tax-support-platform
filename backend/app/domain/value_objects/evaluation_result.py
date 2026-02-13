from enum import Enum


class ObligationResult(str, Enum):
    APPLIES = "applies"
    DOES_NOT_APPLY = "does_not_apply"
    NEEDS_MORE_INFO = "needs_more_info"
    CONDITIONAL = "conditional"
