# -*- coding: utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.uniter_functions.base_function import FUninterpretedFunction


@register_formula('boolean')
class FBoolean(FUninterpretedFunction):
    def __init__(self):
        super(FBoolean, self).__init__(operands=['BOOLEAN'])
