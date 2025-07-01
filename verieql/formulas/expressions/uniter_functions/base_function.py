# -*- coding: utf-8 -*-


from typing import Sequence

from verieql.formulas import register_formula
from verieql.formulas.expressions.expression import FExpression


@register_formula('base_function')
class FUninterpretedFunction(FExpression):
    def __init__(self, operands: Sequence):
        super(FUninterpretedFunction, self).__init__(None, operands)

    def __str__(self):
        return '_'.join([str(operand) for operand in self.operands])

    @property
    def func_name(self):
        return self[0]
