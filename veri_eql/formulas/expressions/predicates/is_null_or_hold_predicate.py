# -*- coding:utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.base_expression import FBaseExpression
from veri_eql.formulas.expressions.operator import FOperator
from veri_eql.formulas.expressions.predicates.base_predicate import FBasePredicate


@register_formula('is_null_or_hold')
class FIsNullOrHoldPredicate(FBasePredicate):
    """
    only work for else clauses in if/case
    """

    def __init__(self, operand: FBaseExpression):
        super(FIsNullOrHoldPredicate, self).__init__(
            operator=FOperator('eq'),
            operands=[operand],
        )

    @property
    def value(self):
        return self.operands[0]

    def __str__(self):
        return f'{self.operands[0]}_IS_NULL_OR_HOLD'
