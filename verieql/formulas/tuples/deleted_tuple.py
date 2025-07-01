# -*- coding: utf-8 -*-

from typing import Sequence

from verieql.formulas import register_formula
from verieql.formulas.tuples.base_tuple import FBaseTuple


@register_formula('deleted_tuple')
class FDeletedTuple(FBaseTuple):
    def __init__(self,
                 name: str,
                 attributes: Sequence = [],
                 ):
        self.fields = []
        self.name = name
        self.attributes = attributes
        self.SORT = None

    def __str__(self):
        return f'DELETED({self.SORT})'
