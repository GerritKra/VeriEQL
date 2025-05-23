# -*- coding: utf-8 -*-

from formulas import register_formula
from formulas.expressions.base_expression import FBaseExpression
from formulas.expressions.predicates.base_predicate import FBasePredicate


@register_formula('last_value_predicate')
class FLastValuePredicate(FBasePredicate):
    def __init__(self, expression: FBaseExpression):
        super(FLastValuePredicate, self).__init__(
            operator=None,
            operands=[expression],
        )

    def __str__(self):
        return f'LAST_VALUE_{self.operands[0]}'
