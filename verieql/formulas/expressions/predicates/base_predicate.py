# -*- coding: utf-8 -*-


from verieql.formulas import register_formula
from verieql.formulas.expressions.expression import FExpression


@register_formula('base_predicate')
class FBasePredicate(FExpression):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
