# -*- coding: utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('time')
class FTime(FUninterpretedFunction):
    def __init__(self, value):
        self.EXPR = value
        super(FTime, self).__init__(operands=['TIME', self.EXPR])
