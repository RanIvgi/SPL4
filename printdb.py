from persistence import *

# Print all Activities
def printActivites():
    print ("Activities")
    repo.activities.print_all()

# Print all Branches
def printBranches():
    print ("Branches")
    repo.branches.print_all()

# Print all Employees
def printEmployees():
    print ("Employees")
    repo.employees.print_all()

# Print all Products
def printProducts():
    print ("Products")
    repo.products.print_all()

# Print all Suppliers
def printSuppliers():
    print ("Suppliers")
    repo.suppliers.print_all()

# Print Employees Report format
def printEmployeesReport():
    print ("Employees Report")
    print ("ID, Name, Salary, Branch")
    repo.employees.print_all()

def main():
    print ("Printing the database")
    printActivites()
    printBranches()
    printEmployees()
    printProducts()
    printSuppliers()
    

if __name__ == '__main__':
    main()