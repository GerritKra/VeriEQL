# -*- coding: utf-8 -*-

from verieql.formulas import register_formula
from verieql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('lower')
class FLower(FUninterpretedFunction):
    """
    Round(expression, decimals, operation=0)
    uninterpreted function
    """

    def __init__(self):
        super(FLower, self).__init__(operands=['LOWER'])
