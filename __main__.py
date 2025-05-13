# -*- coding: utf-8 -*-
"""
SQL Equivalence Check Tool

This module provides a command line tool to check two SQL queries for semantic equivalence.
for semantic equivalence. It uses an automatic checking mechanism,
which can generate counterexamples if the queries are not equivalent.
"""

import argparse
import json
from constants import DIALECT
from environment import Environment


class SQLEquivalenceChecker:
    """
    Main class for the SQL equivalence check.

    This class implements the command line tool and its logic for the
    checking the semantic equivalence of two SQL queries.
    """

    def __init__(self):
        """
        Initialises the SQL equivalence checker with an argument parser.
        """
        self.parser = argparse.ArgumentParser(description="Performs an SQL equivalence check.")
        self._add_arguments()

    def _add_arguments(self):
        """
        Adds all command line arguments to the parser.

        Defines the required and optional parameters for the equivalence check.
        """
        self.parser.add_argument("sql1", type=str, help="First SQL request")
        self.parser.add_argument("sql2", type=str, help="Second SQL request")
        self.parser.add_argument("schema", type=str, help="Schema as a JSON string (e.g. '{\"TABLE\": {\"COL\": \"INT\"}}')")
        self.parser.add_argument("--row_num", type=int, default=2, help="Number of rows for the database (default: 2)")
        self.parser.add_argument("--constraints", type=str, default=None, help="Constraints als JSON-String (z.B. '[{\"primary\": ...}]')")
        self.parser.add_argument("--output_file", type=str, default=None, help="File in which the result is saved (default: output in the command line).")


        self.parser.add_argument("--generate_code", dest='generate_code', action='store_true', help="Generate SQL code and outputs")
        self.parser.add_argument("--no_generate_code", dest='generate_code', action='store_false', help="Do not generate SQL code")
        self.parser.set_defaults(generate_code=True)

        self.parser.add_argument("--timer", dest='timer', action='store_true', help="Show time spent")
        self.parser.add_argument("--no_timer", dest='timer', action='store_false', help="Show no time spent")
        self.parser.set_defaults(timer=True)

        self.parser.add_argument("--show_counterexample", dest='show_counterexample', action='store_true', help="Show counterexample")
        self.parser.add_argument("--no_show_counterexample", dest='show_counterexample', action='store_false', help="Do not show a counterexample")
        self.parser.set_defaults(show_counterexample=True)

        self.parser.add_argument("--dialect", type=str, default=DIALECT.MYSQL,
                                 choices=[DIALECT.ALL, DIALECT.MYSQL, DIALECT.MARIADB, DIALECT.PSQL, DIALECT.POSTGRESQL, DIALECT.ORACLE],
                                 help=f"SQL-Dialect (Default: {DIALECT.MYSQL})")

    def _parse_args(self):
        """
        Parses the command line arguments.

        Returns:
            argparse.Namespace: A namespace object with the parsed arguments.
        """
        return self.parser.parse_args()

    @staticmethod
    def _main_logic(sql1, sql2, schema, row_num=2, constraints=None, output_file=None, **kwargs):
        """
        Executes the main logic of the equivalence check.

        This method sets up the test environment, creates a test database with the specified schema,
        applies the constraints and performs the equivalence check.

        Args:
            sql1 (str): The first SQL query.
            sql2 (str): The second SQL query.
            schema (dict): A dictionary that represents the database schema.
            row_num (int, optional): Number of data rows to be generated. The default is 2.
            constraints (list, optional): A list of constraints for the database.
            output_file (str, optional): Path to the output file for the results.
            **kwargs: Additional configuration options for the environment.
        """
        with Environment(**kwargs) as env:
            for k, v in schema.items():
                env.create_database(attributes=v, bound_size=row_num, name=k)
            env.add_constraints(constraints)
            env.save_checkpoints()
            if env._script_writer is not None:
                env._script_writer.save_checkpoints()

            # For file output
            result_output = []

            # Perform analysis and save result
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

            if result:
                equiv_result = "\033[1;32;40m>>> Equivalent! \033[0m" if not output_file else ">>> Equivalent!"
            else:
                equiv_result = "\033[1;31;40m>>> Non-Equivalent! Found a counterexample! \033[0m" if not output_file else ">>> Non-Equivalent! Found a counterexample!"

            if output_file:
                result_output.append(equiv_result)

                # Create directory if it does not exist
                import os
                os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)

                # Write results to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(result_output))
            else:
                print(equiv_result)


            if env.traversing_time is not None:
                print(f"Time cost: {env.traversing_time + env.solving_time:.2f}")
            if result:
                print("\033[1;32;40m>>> Equivalent! \033[0m")
            else:
                print("\033[1;31;40m>>> Non-Equivalent! Found a counterexample! \033[0m")

    def run(self):
        """
        Executes the SQL equivalence checker.

        Parses the command line arguments, validates the input and calls the main logic.
        Terminates the programme with an error code if the input is invalid.
        """
        args = self._parse_args()

        try:
            parsed_schema = json.loads(args.schema)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for the schema.")
            exit(1)

        parsed_constraints = None
        if args.constraints:
            try:
                parsed_constraints = json.loads(args.constraints)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format for the constraints.")
                exit(1)

        self._main_logic(
            sql1=args.sql1,
            sql2=args.sql2,
            schema=parsed_schema,
            row_num=args.row_num,
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

    # Beispielnutzung (auskommentiert)
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