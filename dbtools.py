import inspect


def orm(cursor, dto_type):
    # the following line retrieve the argument names of the constructor
    args : list[str] = list(inspect.signature(dto_type.__init__).parameters.keys())

    # the first argument of the constructor will be 'self', it does not correspond
    # to any database field, so we can ignore it.
    args : list[str] = args[1:]

    # gets the names of the columns returned in the cursor
    col_names = [column[0] for column in cursor.description]

    # map them into the position of the corresponding constructor argument
    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


class Dao(object):
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type

        # dto_type is a class, its __name__ field contains a string representing the name of the class.
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        column_names = ','.join(ins_dict.keys())
        params = list(ins_dict.values())
        qmarks = ','.join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})' \
            .format(self._table_name, column_names, qmarks)

        self._conn.execute(stmt, params)

    def find_all(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {}'.format(self._table_name))
        return orm(c, self._dto_type)
    
    def find(self, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())

        stmt = 'SELECT * FROM {} WHERE {}' \
        .format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        c = self._conn.cursor()
        c.execute(stmt, params)
        return orm(c, self._dto_type)

    def delete(self, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())

        stmt = 'DELETE FROM {} WHERE {}' \
            .format(self._table_name,' AND '.join([col + '=?' for col in column_names]))
            
    # This method is used to update the table
    def update(self, id, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())
        params.append(id)

        stmt = 'UPDATE {} SET {} WHERE id = ?' \
            .format(self._table_name, ', '.join([col + '=?' for col in column_names]))

        self._conn.cursor().execute(stmt, params)
        
    def get_primary_key_column(self) -> str:
        query = f"PRAGMA table_info({self._table_name})"
        cursor = self._conn.cursor()
        cursor.execute(query)
        columns = cursor.fetchall()
        for column in columns:
            if column[5] == 1:  # The 6th column (index 5) is the primary key flag
                return column[1]  # The 2nd column (index 1) is the column name
        return None
        
    # This method is used to sort the table by a specific field, and return the data
    def __str__(self):
        c = self._conn.cursor()
        # In case called From activities table
        if self._table_name == 'activities':
            c.execute('SELECT * FROM {} ORDER BY {}'.format(self._table_name, "date"))
            data = c.fetchall()
            return '\n'.join([str(row) for row in data])
        # In case called From any other table
        else:
            primary_key_column = self.get_primary_key_column()
            if primary_key_column:
                c.execute('SELECT * FROM {} ORDER BY {}'.format(self._table_name, primary_key_column))
                data = c.fetchall()
                return '\n'.join([str(row) for row in data])
            # In case the table does not have a primary key
            else:
                c.execute('SELECT * FROM {}'.format(self._table_name))
                data = c.fetchall()
                return '\n'.join([str(row) for row in data])
        
        
        
