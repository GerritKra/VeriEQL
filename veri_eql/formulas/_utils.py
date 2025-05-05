# -*- coding: utf-8 -*-

from typing import (
    Sequence,
)

from veri_eql.formulas.columns import (
    FAttribute,
    AggregationType,
)
from veri_eql.formulas.expressions import (
    FIfPredicate,
    FCasePredicate,
)
from veri_eql.formulas.expressions.base_expression import FBaseExpression
from veri_eql.formulas.expressions.digits import FDigits


def require_tuples_func(expr: FBaseExpression):
    if isinstance(expr, FAttribute):
        if expr.EXPR is None:
            # 1) a pure attribute or 2) attribute is NULL for empty table
            return expr.require_tuples
        if isinstance(expr.EXPR, FDigits):
            return False
        else:
            return require_tuples_func(expr.EXPR)
    elif isinstance(expr, AggregationType):
        return True
    # elif isinstance(expr, FRound):
    #     return require_tuples_func(expr.EXPR)
    # elif isinstance(expr, UninterFunctionType):
    #     return require_tuples_func(expr[1])
    elif isinstance(expr, FCasePredicate):
        outs = [
            require_tuples_func(clause)
            for clause in expr.when_clauses + expr.then_clauses + [expr.else_clause]
        ]
        return sum(outs) > 0
    elif isinstance(expr, FIfPredicate):
        return sum([require_tuples_func(operand) for operand in expr[1:]]) > 0
    elif isinstance(expr, Sequence | FBaseExpression):
        for operand in expr:
            if require_tuples_func(operand):
                return True
        return False
    else:
        return False
