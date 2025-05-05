# -*- coding:utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.base_expression import FBaseExpression
from veri_eql.formulas.expressions.predicates.base_predicate import FBasePredicate


@register_formula('is_not_true')
class FIsNotTruePredicate(FBasePredicate):
    def __init__(self, operand: FBaseExpression):
        super(FIsNotTruePredicate, self).__init__(
            operator=None,
            operands=[operand],
        )

    @property
    def value(self):
        return self.operands[0]

    def __str__(self):
        return f'{self.operands[0]}_IS_NOT_TRUE'
