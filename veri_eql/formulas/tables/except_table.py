# -*- coding: utf-8 -*-

from typing import Sequence

from veri_eql.formulas import register_formula
from veri_eql.formulas.tables.base_table import FBaseTable
from veri_eql.formulas.tables.distinct_table import _distinct
from veri_eql.formulas.tables.except_all_table import FExceptAllTable


@register_formula('except')
class FExceptTable(FBaseTable):
    def __init__(self,
                 scope,
                 tables: Sequence[FBaseTable],
                 name: str = None,
                 ):
        father_table = FExceptAllTable(scope, tables)
        table = _distinct(
            scope,
            table=father_table,
            condition=[None, father_table.attributes],
        )
        name = name or '_Except_'.join(t.name for t in tables)
        super(FExceptTable, self).__init__(table, name)
        scope.register_database(name, self)
        self.fathers = [father_table]
        self.root = [t.root for t in tables]
