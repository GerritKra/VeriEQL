# -*- coding: utf-8 -*-

from verieql.formulas import register_formula
from verieql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('float')
class FFloat(FUninterpretedFunction):
    def __init__(self):
        super(FFloat, self).__init__(operands=['FLOAT'])
