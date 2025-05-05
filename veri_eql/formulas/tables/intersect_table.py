# -*- coding: utf-8 -*-

from typing import Sequence

from veri_eql.formulas import register_formula
from veri_eql.formulas.tables.base_table import FBaseTable
from veri_eql.formulas.tables.distinct_table import _distinct
from veri_eql.formulas.tables.intersect_all_table import FIntersectAllTable


@register_formula('intersect')
class FIntersectTable(FBaseTable):
    def __init__(self,
                 scope,
                 tables: Sequence[FBaseTable],
                 name: str = None,
                 ):
        father_table = FIntersectAllTable(scope, tables)
        table = _distinct(
            scope,
            table=father_table,
            condition=[None, father_table.attributes],
        )
        name = name or '_IntersectAll_'.join(t.name for t in tables)
        super(FIntersectTable, self).__init__(table, name)
        scope.register_database(name, self)
        self.fathers = [father_table]
        self.root = [t.root for t in tables]
