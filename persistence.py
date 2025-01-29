import sqlite3
import atexit
from dbtools import Dao, orm
 
# Data Transfer Objects:
class Employee(object):
    def __init__(self, id, name, salary, branche):
        self.id = id
        self.name = name
        self.salary = salary
        self.branche = branche
 
class Supplier(object):
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

class Branche(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

class Activitie(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date
 
 
#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        self.branches = Dao(Branche, self._conn)
        self.suppliers = Dao(Supplier, self._conn)
        self.products = Dao(Product, self._conn)
        self.employees = Dao(Employee, self._conn)
        self.activities = Dao(Activitie, self._conn)
 
    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
    
    # return the data from the tables for the employees
    # report: Name, Salary, Working location, total sales income
    def create_EmployeesReport(self):
        query = """
        SELECT employees.name, employees.salary, branches.location, 
               IFNULL(SUM(products.price * ABS(activities.quantity)), 0) AS total_sales_income
        FROM employees
        LEFT JOIN branches ON employees.branche = branches.id
        LEFT JOIN activities ON employees.id = activities.activator_id
        LEFT JOIN products ON activities.product_id = products.id
        GROUP BY employees.id
        ORDER BY employees.name;
        """
        report = self.execute_command(query)
        return report
    
    # return the data from the tables for the activities
    # report: date of activity, item description, quantity, name of seller, and the name of the supplier
    def create_ActivitiesReport(self):
        query = """
        SELECT activities.date, products.description, activities.quantity, employees.name, suppliers.name
        FROM activities
        JOIN products ON activities.product_id = products.id
        LEFT JOIN employees ON activities.activator_id = employees.id
        LEFT JOIN suppliers ON activities.activator_id = suppliers.id
        ORDER BY activities.date;
        """
        report = self.execute_command(query)
        return report
        
# singleton
repo = Repository()
atexit.register(repo._close)