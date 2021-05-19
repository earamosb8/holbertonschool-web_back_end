#!/usr/bin/env python3
"""
    function safe_first_element with annotations
"""

from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """ first element of a sequence """
    if lst:
        return lst[0]
    else:
        return None
