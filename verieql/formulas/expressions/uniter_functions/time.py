# -*- coding: utf-8 -*-

from verieql.formulas import register_formula
from verieql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('time')
class FTime(FUninterpretedFunction):
    def __init__(self, value):
        self.EXPR = value
        super(FTime, self).__init__(operands=['TIME', self.EXPR])
