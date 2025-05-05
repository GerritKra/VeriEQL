# -*- coding: utf-8 -*-


from typing import (
    Sequence,
)

from veri_eql.formulas import register_formula
from veri_eql.formulas.tuples.base_tuple import FBaseTuple
from veri_eql.formulas.tuples.tuple import FTuple


@register_formula('orderby_tuple')
class FOrderByTuple(FTuple):
    def __init__(self,
                 tuples: Sequence[FBaseTuple | FTuple],
                 keys: Sequence[str],
                 ascending_flags: Sequence[bool] = None,
                 name: str = None,
                 ):
        self.keys = keys
        self.ascending_flags = ascending_flags
        super(FOrderByTuple, self).__init__(tuples, None, name)
        self.attributes = tuples.attributes

    def __str__(self):
        return f'{self.name} := OrderBy({self.fathers}, {[(key, "ASC" if asc else "DESC") for key, asc in zip(self.keys, self.ascending_flags)]})'
