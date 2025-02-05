from persistence import *

# Print all Activities
def printActivites():
    print ("Activities")
    print (repo.activities.__str__())

# Print all Branches
def printBranches():
    print ("Branches")
    print (repo.branches.__str__())

# Print all Employees
def printEmployees():
    print ("Employees")
    print (repo.employees.__str__())

# Print all Products
def printProducts():
    print ("Products")
    print (repo.products.__str__())

# Print all Suppliers
def printSuppliers():
    print ("Suppliers")
    print (repo.suppliers.__str__())

# Print Employees Report format
def printEmployeesReport():
    print ("Employees report")
    report = repo.create_EmployeesReport()
    for row in report:
        print(" ".join(map(str, row)))

# Print Activities Report format
def printActivitiesreport():
    print ("Activities report")
    report = repo.create_ActivitiesReport()
    for row in report:
        print(row)

def main():
    printActivites()
    print()
    printBranches()
    print()
    printEmployees()
    print()
    printProducts()
    print()
    printSuppliers()
    print()
    printEmployeesReport()
    print()
    printActivitiesreport()
    

if __name__ == '__main__':
    main()