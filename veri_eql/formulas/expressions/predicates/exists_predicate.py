# -*- coding: utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.expressions.operator import FOperator
from veri_eql.formulas.expressions.predicates.base_predicate import FBasePredicate


@register_formula('exists_predicate')
class FExistsPredicate(FBasePredicate):
    """
    This predicate may refer to correlated subquery.

    WHERE EXISTS (
        SELECT XX FROM XX
    )
    """

    def __init__(self, clauses):
        super(FExistsPredicate, self).__init__(
            operator=FOperator('exists'),
            operands=[clauses],
        )

    def __str__(self):
        out = str(self.operands[0]).replace('\n', '')
        return f"EXISTS {out}"
