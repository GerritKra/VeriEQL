# -*- coding: utf-8 -*-

import argparse
import json
from constants import DIALECT
from environment import Environment


class SQLEquivalenceChecker:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Führt eine SQL-Äquivalenzprüfung durch.")
        self._add_arguments()

    def _add_arguments(self):
        self.parser.add_argument("sql1", type=str, help="Erste SQL-Anfrage")
        self.parser.add_argument("sql2", type=str, help="Zweite SQL-Anfrage")
        self.parser.add_argument("schema", type=str, help="Schema als JSON-String (z.B. '{\"TABLE\": {\"COL\": \"INT\"}}')")
        self.parser.add_argument("--row_num", type=int, default=2, help="Anzahl der Zeilen für die Datenbank (Standard: 2)")
        self.parser.add_argument("--constraints", type=str, default=None, help="Constraints als JSON-String (z.B. '[{\"primary\": ...}]')")
        self.parser.add_argument("--output_file", type=str, default=None, help="Datei, in der das Ergebnis gespeichert wird (Standard: Ausgabe in der Kommandozeile).")


        self.parser.add_argument("--generate_code", dest='generate_code', action='store_true', help="Generiere SQL-Code und Ausgaben")
        self.parser.add_argument("--no_generate_code", dest='generate_code', action='store_false', help="Generiere keinen SQL-Code")
        self.parser.set_defaults(generate_code=True)

        self.parser.add_argument("--timer", dest='timer', action='store_true', help="Zeige Zeitaufwand")
        self.parser.add_argument("--no_timer", dest='timer', action='store_false', help="Zeige keinen Zeitaufwand")
        self.parser.set_defaults(timer=True)

        self.parser.add_argument("--show_counterexample", dest='show_counterexample', action='store_true', help="Zeige Gegenbeispiel")
        self.parser.add_argument("--no_show_counterexample", dest='show_counterexample', action='store_false', help="Zeige kein Gegenbeispiel")
        self.parser.set_defaults(show_counterexample=True)

        self.parser.add_argument("--dialect", type=str, default=DIALECT.MYSQL,
                                 choices=[DIALECT.ALL, DIALECT.MYSQL, DIALECT.MARIADB, DIALECT.PSQL, DIALECT.POSTGRESQL, DIALECT.ORACLE],
                                 help=f"SQL-Dialekt (Standard: {DIALECT.MYSQL})")

    def _parse_args(self):
        return self.parser.parse_args()

    def _main_logic(self, sql1, sql2, schema, ROW_NUM=2, constraints=None, output_file=None, **kwargs):
        with Environment(**kwargs) as env:
            for k, v in schema.items():
                env.create_database(attributes=v, bound_size=ROW_NUM, name=k)
            env.add_constraints(constraints)
            env.save_checkpoints()
            if env._script_writer is not None:
                env._script_writer.save_checkpoints()

            # Für Dateiausgabe
            result_output = []

            # Analyse ausführen und Ergebnis speichern
            result = env.analyze(sql1, sql2, out_file="test/test.py")

            if env.show_counterexample and env.counterexample:
                if output_file:
                    result_output.append(env.counterexample)
                else:
                    print(env.counterexample)

            if env.traversing_time is not None:
                time_cost = f"Time cost: {env.traversing_time + env.solving_time:.2f}"
            if output_file:
                result_output.append(time_cost)
            else:
                print(time_cost)

            if result == True:
                equiv_result = "\033[1;32;40m>>> Equivalent! \033[0m" if not output_file else ">>> Equivalent!"
            else:
                equiv_result = "\033[1;31;40m>>> Non-Equivalent! Found a counterexample! \033[0m" if not output_file else ">>> Non-Equivalent! Found a counterexample!"

            if output_file:
                result_output.append(equiv_result)

                # Verzeichnis erstellen, falls es nicht existiert
                import os
                os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)

                # Ergebnisse in Datei schreiben
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(result_output))
            else:
                print(equiv_result)


            if env.traversing_time is not None:
                print(f"Time cost: {env.traversing_time + env.solving_time:.2f}")
            if result == True:
                print("\033[1;32;40m>>> Equivalent! \033[0m")
            else:
                print("\033[1;31;40m>>> Non-Equivalent! Found a counterexample! \033[0m")

    def run(self):
        args = self._parse_args()

        try:
            parsed_schema = json.loads(args.schema)
        except json.JSONDecodeError:
            print("Fehler: Ungültiges JSON-Format für das Schema.")
            exit(1)

        parsed_constraints = None
        if args.constraints:
            try:
                parsed_constraints = json.loads(args.constraints)
            except json.JSONDecodeError:
                print("Fehler: Ungültiges JSON-Format für die Constraints.")
                exit(1)

        self._main_logic(
            sql1=args.sql1,
            sql2=args.sql2,
            schema=parsed_schema,
            ROW_NUM=args.row_num,
            constraints=parsed_constraints,
            generate_code=args.generate_code,
            timer=args.timer,
            show_counterexample=args.show_counterexample,
            dialect=args.dialect,
            output_file=args.output_file
        )


if __name__ == '__main__':
    checker = SQLEquivalenceChecker()
    checker.run()

    # sql1, sql2 = [
    #     "SELECT S.CUSTOMERKEY FROM SALES AS S",
    #     "SELECT S.CUSTOMERKEY+1 FROM SALES AS S WHERE EXISTS (SELECT SALES.CUSTOMERKEY FROM CUSTOMER JOIN SALES ON CUSTOMER.CUSTOMERKEY = SALES.CUSTOMERKEY WHERE SALES.CUSTOMERKEY != S.CUSTOMERKEY)",
    # ]
    # # Customer: CustomerKey [PK]
    # # Sales: (CustomerKey [FK], OrderDateKey [FK]) [PK], ShipDate, DueDate
    # # Date: DateKey [PK]
    # schema = {
    #     "CUSTOMER": {"CUSTOMERKEY": "INT"},
    #     "SALES": {"CUSTOMERKEY": "INT", "ORDERDATEKEY": "INT", "SHIPDATE": "DATE", "DUEDATE": "DATE"},
    #     "DATE": {"DATEKEY": "INT"},
    # }
    # constants = [
    #     # use `__` to replace `.`, e.g., FRIENDSHIP.USER1_ID => FRIENDSHIP__USER1_ID
    #     {"primary": [{"value": "CUSTOMER__CUSTOMERKEY"}]},
    #     {"primary": [{"value": "SALES__CUSTOMERKEY"}, {"value": "SALES__ORDERDATEKEY"}]},
    #     {"primary": [{"value": "DATE__DATEKEY"}]},
    #     {"foreign": [{"value": "SALES__CUSTOMERKEY"}, {"value": "CUSTOMER__CUSTOMERKEY"}]},
    #     {"foreign": [{"value": "SALES__ORDERDATEKEY"}, {"value": "DATE__DATEKEY"}]},
    # ]
    # bound_size = 2
    # # generate_code: generate SQL code and running outputs if you find a counterexample
    # # timer: show time costs
    # # show_counterexample: print counterexample?
    # config = {'generate_code': True, 'timer': True, 'show_counterexample': True, "dialect": DIALECT.MYSQL}
    # # Um die alte main-Funktion direkt aufzurufen (jetzt _main_logic in der Klasse):
    # checker._main_logic(sql1, sql2, schema, ROW_NUM=bound_size, constraints=constants, **config)