# -*- coding:utf-8 -*-

from z3 import (
    ExprRef,
)

from constants import (
    If,
    Not,
    Or,
    And,
    Sum,
    IntVal,
    Z3_0,
    Z3_NULL_VALUE,
)
from formulas import register_formula
from formulas.columns.aggregations.aggregation import (
    FAggregation,
    CONSTANT_TYPE,
)
from formulas.expressions.base_expression import FBaseExpression
from formulas.expressions.expression_tuple import FExpressionTuple
from utils import simplify


@register_formula('agg_stddev_pop')
class FStddevPop(FAggregation):
    def __init__(self, scope, function: str, expression: FBaseExpression = None, **kwargs):
        super(FStddevPop, self).__init__(scope, function, expression, **kwargs)

    def __expr__(self, y_s, group_func=None, **kwargs):
        # STDDEV_POP(constant) => 0, STDDEV_POP(id) => sqrt((i - mean)^2/N)
        if isinstance(y_s, ExprRef):
            y_s = [y_s]
        deleted_func = kwargs.get('deleted_func', self.DELETED_FUNCTION)
        if self.filter_cond is not None and self.DISTINCT:
            prev_filter_conds = []
        value_formulas = []
        count_formulas = []
        for idx, y in enumerate(y_s):
            curr_expr = self(y)
            premise = [deleted_func(y), curr_expr.NULL]
            if self.DISTINCT and idx > 0:
                for i, prev_y in enumerate(y_s[:idx]):
                    prev_expr = self(prev_y)
                    prev_cond = [
                        Not(deleted_func(prev_y)),
                        Not(prev_expr.NULL),
                        curr_expr.VALUE == prev_expr.VALUE,
                    ]
                    if i != 0 and group_func is not None:
                        prev_cond.append(group_func(prev_y))  # distinct tuple should also belong to this group
                    if self.filter_cond is not None:
                        prev_cond.extend(prev_filter_conds)
                    prev_cond = simplify(prev_cond, operator=And)
                    premise.append(prev_cond)
            if group_func is not None:
                premise.append(Not(group_func(y)))
            if self.filter_cond is not None:
                filter_cond = self.filter_cond(y)
                premise.extend([filter_cond.NULL, Not(filter_cond.VALUE)])
                if self.DISTINCT:
                    # for later t2 != t1 if filter condition holds for t1 and t2
                    prev_filter_conds.extend([Not(filter_cond.NULL), filter_cond.VALUE])
            premise = simplify(premise, operator=Or)
            count_formulas.append(premise)
            value_formulas.append(If(premise, Z3_0, self._safe_value(curr_expr.VALUE)))
        if isinstance(self.EXPR, CONSTANT_TYPE):
            VALUE = Z3_0
        else:
            VALUE = (Sum(*[(v - Sum(value_formulas) / Sum(*count_formulas)) ** IntVal('2') for v in value_formulas]) / \
                     Sum(*count_formulas)) ** IntVal('0.5')
        NULL = simplify(count_formulas, operator=And)
        return FExpressionTuple(
            NULL=NULL,
            VALUE=If(
                NULL,  # all DELETED/NULL
                Z3_NULL_VALUE,  # if all DELETED/NULL, its value does not matter
                VALUE,
            ),
        )
