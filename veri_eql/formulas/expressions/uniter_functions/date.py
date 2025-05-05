# -*- coding: utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('date')
class FDate(FUninterpretedFunction):
    def __init__(self, value):
        self.EXPR = value
        super(FDate, self).__init__(operands=['DATE', self.EXPR])
