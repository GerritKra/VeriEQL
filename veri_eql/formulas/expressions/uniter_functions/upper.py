# -*- coding: utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('upper')
class FUpper(FUninterpretedFunction):
    """
    Round(expression, decimals, operation=0)
    uninterpreted function
    """

    def __init__(self):
        super(FUpper, self).__init__(operands=['UPPER'])
