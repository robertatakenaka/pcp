# coding=utf-8

import sqlite3
import utils


class SQL(object):

    def __init__(self, db_filename):
        self.db_filename = db_filename

    def create_db(self, schema_filename):
        with sqlite3.connect(self.db_filename) as conn:
            print 'Creating schema'
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

    def insert_data(self, csv_filename, table_name, fields):
        conn = sqlite3.connect(self.db_filename)
        _fields = ', '.join(fields)

        for row in open(csv_filename, 'r').readlines():
            if not isinstance(row, unicode):
                row = row.decode('utf-8')
            row = row.strip()
            items = row.split('\t')

            if len(items) == len(fields):
                _values = []
                for item in items:
                    if not '"' in item:
                        _values.append('"' + item.replace('  ', ' ').strip() + '"')
                    elif not "'" in item:
                        _values.append("'" + item.replace('  ', ' ').strip() + "'")
                    else:
                        _values.append('`' + item.replace('  ', ' ').strip() + '`')
                instruction = 'insert into ' + table_name + ' (' + _fields + ') ' + ' values (' + ', '.join(_values) + ')'
                utils.debugging(instruction)
                conn.execute(instruction + '\n')
                conn.commit()
        conn.close()

    def query(self, expr):
        results = []
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(expr)
                for row in cursor.fetchall():
                    results.append(row)
            except Exception as e:
                utils.debugging('ERROR: query')
                utils.debugging(expr)
                utils.debugging(e)
        conn.close()
        return results

    def query_one(self, expr):
        results = []
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(expr)
            results = cursor.fetchone()
        conn.close()
        return results

    def get_select_statement(self, table_name, fields, where_expr=None):
        if where_expr is None:
            where_expr = ''
        else:
            where_expr = ' where ' + where_expr
        expr = 'select ' + ', '.join(fields) + ' from ' + table_name + where_expr
        return expr

    def format_expr(self, labels, values, connector=' OR '):
        expr = []
        for i in range(0, len(labels)):
            if values[i] is not None:
                if not isinstance(values[i], unicode):
                    values[i] = values[i].decode('utf-8')
                expr.append(labels[i] + '="' + values[i] + '"')
        return connector.join(expr)

