# -*- coding: utf-8 -*-

from verieql.formulas import register_formula
from verieql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('boolean')
class FBoolean(FUninterpretedFunction):
    def __init__(self):
        super(FBoolean, self).__init__(operands=['BOOLEAN'])
