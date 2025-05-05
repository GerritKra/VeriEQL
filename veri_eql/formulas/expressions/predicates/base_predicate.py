# -*- coding: utf-8 -*-


from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.expression import FExpression


@register_formula('base_predicate')
class FBasePredicate(FExpression):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
