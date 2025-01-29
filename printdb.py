from persistence import *

# Print all Activities
def printActivites():
    print ("Activities")
    for activity in repo.activities.get_Data_Before_Print():
        print(activity)

# Print all Branches
def printBranches():
    print ("Branches")
    for branch in repo.branches.get_Data_Before_Print():
        print(branch)

# Print all Employees
def printEmployees():
    print ("Employees")
    for employee in repo.employees.get_Data_Before_Print():
        print(employee)

# Print all Products
def printProducts():
    print ("Products")
    for product in repo.products.get_Data_Before_Print():
        print(product)

# Print all Suppliers
def printSuppliers():
    print ("Suppliers")
    for supplier in repo.suppliers.get_Data_Before_Print():
        print(supplier)

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