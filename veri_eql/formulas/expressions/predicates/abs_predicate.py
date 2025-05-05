# -*- coding: utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.base_expression import FBaseExpression
from veri_eql.formulas.expressions.predicates.base_predicate import FBasePredicate


@register_formula('abs_predicate')
class FAbsPredicate(FBasePredicate):
    def __init__(self, expression: FBaseExpression):
        super(FAbsPredicate, self).__init__(
            operator=None,
            operands=[expression],
        )

    def __str__(self):
        return f'ABS_{self.operands[0]}'
