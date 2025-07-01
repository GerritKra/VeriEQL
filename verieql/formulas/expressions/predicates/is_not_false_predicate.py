# -*- coding:utf-8 -*-

from verieql.formulas import register_formula
from verieql.formulas.expressions.base_expression import FBaseExpression
from verieql.formulas.expressions.predicates.base_predicate import FBasePredicate


@register_formula('is_not_false')
class FIsNotFalsePredicate(FBasePredicate):

    def __init__(self, operand: FBaseExpression):
        super(FIsNotFalsePredicate, self).__init__(
            operator=None,
            operands=[operand],
        )

    @property
    def value(self):
        return self.operands[0]

    def __str__(self):
        return f'{self.operands[0]}_IS_NOT_FALSE'
