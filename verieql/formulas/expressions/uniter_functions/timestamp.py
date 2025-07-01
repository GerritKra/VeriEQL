# -*- coding: utf-8 -*-

from verieql.formulas import register_formula
from verieql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('timestamp')
class FTimestamp(FUninterpretedFunction):
    def __init__(self, value):
        self.EXPR = str(value)
        super(FTimestamp, self).__init__(operands=['TIMESTAMP', self.EXPR])

    @property
    def value(self):
        return self[1]
