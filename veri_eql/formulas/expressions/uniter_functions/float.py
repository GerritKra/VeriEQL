# -*- coding: utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('float')
class FFloat(FUninterpretedFunction):
    def __init__(self):
        super(FFloat, self).__init__(operands=['FLOAT'])
