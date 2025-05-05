# -*- coding: utf-8 -*-
from typing import Sequence

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.base_expression import FBaseExpression
from veri_eql.formulas.expressions.operator import FOperator
from veri_eql.formulas.expressions.predicates.base_predicate import FBasePredicate


@register_formula('coalesce_predicate')
class FCoalescePredicate(FBasePredicate):
    def __init__(self, expressions: Sequence[FBaseExpression]):
        super(FCoalescePredicate, self).__init__(
            operator=FOperator('coalesce'),
            operands=expressions,
        )

    def __str__(self):
        return f'{self.operator}_{"_".join(str(operand) for operand in self.operands)}'
