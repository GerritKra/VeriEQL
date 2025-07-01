# -*- coding: utf-8 -*-

from verieql.formulas import register_formula
from verieql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('integer')
class FInteger(FUninterpretedFunction):
    def __init__(self):
        super(FInteger, self).__init__(operands=['INTEGER'])
