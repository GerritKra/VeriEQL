# -*- coding: utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('varchar')
class FVarchar(FUninterpretedFunction):
    def __init__(self, value):
        self.EXPR = str(value)
        super(FVarchar, self).__init__(operands=['VARCHAR', self.EXPR])

    @property
    def value(self):
        return self[1]
