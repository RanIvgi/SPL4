import math
from persistence import *

import sys

# Check if the product is available in the products table
def Check_If_Can_Buy(product_id : int, quantity : int):
    product = repo.products.find(id = product_id)
    if product:
        if product[0].quantity >= abs(quantity):
            return True
        else:
            return False
    else:
        return False

def main(args : list[str]):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            # Check if the action is buy
            if (int(splittedline[1]) < 0):
                # Check if the product is available
                if Check_If_Can_Buy(int(splittedline[0]), int(splittedline[1])):
                    # Insert the action to the activities table
                    repo.activities.insert(Activitie(int(splittedline[0]), int(splittedline[1]), int(splittedline[2]), splittedline[3]))
                    # Update the data base by subtracting the quantity from the product
                    product = repo.products.find(id = int(splittedline[0]))
                    newQuantity = product[0].quantity + int(splittedline[1])
                    repo.products.update(int(splittedline[0]), quantity = newQuantity)
            # Check if the action is supply
            elif (int(splittedline[1]) > 0):
                # Insert the action to the activities table
                repo.activities.insert(Activitie(int(splittedline[0]), int(splittedline[1]), int(splittedline[2]), splittedline[3]))
                # Update the data base by adding the quantity to the product
                product = repo.products.find(id = int(splittedline[0]))
                newQuantity = product[0].quantity + int(splittedline[1])
                repo.products.update(int(splittedline[0]), quantity = newQuantity)
            else:
                print("Quantity is 0")
                pass

if __name__ == '__main__':
    main(sys.argv)