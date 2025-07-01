# -*- coding: utf-8 -*-

from typing import Sequence

from verieql.errors import NotSupportedError
from verieql.formulas import register_formula
from verieql.formulas.expressions.base_expression import FBaseExpression
from verieql.formulas.expressions.operator import FOperator
from verieql.formulas.expressions.predicates.base_predicate import FBasePredicate
from verieql.formulas.expressions.predicates.not_in_condition import _fuzzy_check


@register_formula('in_predicate')
class FInPredicate(FBasePredicate):
    def __init__(self, attributes: Sequence[FBaseExpression], table):
        super(FInPredicate, self).__init__(
            operator=FOperator('in'),
            operands=[attributes, table],
        )
        from verieql.formulas.tables import (
            FBaseTable,
            FProjectionTable,
            FGroupByTable,
            FLimitTable,
            FOrderByTable,
        )

        if isinstance(table, FBaseTable):
            # group by + order + limit
            groupby_table = table
            if isinstance(groupby_table, FProjectionTable):
                groupby_table = groupby_table.fathers[0]
            if isinstance(groupby_table, FLimitTable):
                groupby_table = groupby_table.fathers[0]
            if isinstance(groupby_table, FOrderByTable):
                groupby_table = groupby_table.fathers[0]
            if isinstance(groupby_table, FGroupByTable) and \
                    _fuzzy_check(table.attributes, groupby_table.groupby_keys[0]):
                raise NotSupportedError(
                    f"{self.__class__.__name__} contains a table with fuzzy attributes of GroupBy.")

        self.require_tuples = any(getattr(opd, 'require_tuples', False) for opd in attributes)

    def __str__(self):
        return f'{self.operands[0]}_{self.operator}_{self.operands[1].name}'
