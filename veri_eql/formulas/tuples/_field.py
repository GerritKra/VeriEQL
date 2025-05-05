# -*- coding:utf-8 -*-

from veri_eql.formulas import register_formula
from veri_eql.formulas.base_formula import BaseFormula
from veri_eql.formulas.columns.attribute import FAttribute
from veri_eql.formulas.expressions import (
    FSymbol,
    FOperator,
    FExpression,
)


@register_formula('field')
class FField(FExpression):
    """
    Field := FAttribute == FSymbol
    """

    def __init__(self, attr: str | FAttribute, value: str | BaseFormula):
        attr = FAttribute(attr) if isinstance(attr, str) else attr
        value = FSymbol(value) if isinstance(value, str) else value
        super(FField, self).__init__(FOperator('eq'), [attr, value])

    def __str__(self):
        return super(FField, self).__str__()

    def __repr__(self):
        return self.__str__()

    @property
    def attribute(self):
        return self.operands[0]

    @property
    def value(self):
        return self.operands[1]
