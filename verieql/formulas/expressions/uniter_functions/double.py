# -*- coding: utf-8 -*-

from verieql.formulas import register_formula
from verieql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('double')
class FDouble(FUninterpretedFunction):
    def __init__(self):
        super(FDouble, self).__init__(operands=['DOUBLE'])
