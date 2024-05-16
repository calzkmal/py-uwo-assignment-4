"""
CS1026A 2023
Assignment 04
Calzy Akmal Indyramdhani
251397118
cindyram@uwo.ca
December 8, 2023
"""

# Definition of the Product class
class Product:
    # Initialize product attributes
    def __init__(self, name, price, category):
        self._name = name
        self._price = price
        self._category = category

    # Define how products are classified
    def __eq__(self, other): 
        if isinstance(other, Product):
            if ((self._name == other._name and self._price == other._price) and (self._category == other._category)):
                return True
            else:
                return False
        else:
            return False

    # Getter method for product name
    def get_name(self):
        return self._name

    # Getter method for product price
    def get_price(self):
        return self._price

    # Getter method for product category
    def get_category(self):
        return self._category

    # Implement string representation
    def __repr__(self):
        rep = 'Product(' + self._name + ',' + str(self._price) + ',' + self._category + ')'
        return rep

# Definition of the Inventory class
class Inventory:
    # Initialize the inventory
    def __init__(self):
        self._inventoryData = {}

    # Add a new product to the inventory
    def add_to_productInventory(self, productName, productPrice, productQuantity):
        self._inventoryData[productName] = {
            'price': productPrice,
            'quantity': productQuantity
        }

    # Add quantity to an existing product in the inventory
    def add_productQuantity(self, nameProduct, addQuantity):
        if nameProduct in self._inventoryData:
            self._inventoryData[nameProduct]['quantity'] += addQuantity

    # Remove quantity of a product from the inventory
    def remove_productQuantity(self, nameProduct, removeQuantity):
        if nameProduct in self._inventoryData:
            currentQuantity = self._inventoryData[nameProduct]['quantity']
            if currentQuantity >= removeQuantity:
                self._inventoryData[nameProduct]['quantity'] -= removeQuantity
            else:
                self._inventoryData[nameProduct]['quantity'] = 0

    # Get the price of a product from the inventory
    def get_productPrice(self, nameProduct):
        return self._inventoryData[nameProduct]['price']

    # Get the quantity of a product from the inventory
    def get_productQuantity(self, nameProduct):
        return self._inventoryData[nameProduct]['quantity']

    # Display the inventory
    def display_Inventory(self):
        for productName, productInfo in self._inventoryData.items():
            print(f"{productName}, {productInfo['price']}, {productInfo['quantity']}")

# Definition of the ShoppingCart class
class ShoppingCart:
    # Initialize the shopping cart
    def __init__(self, buyerName, inventory):
        self._buyerName = buyerName
        self._inventory = inventory
        self._shoppingCart = {}

    # Add products to the shopping cart
    def add_to_cart(self, nameProduct, requestedQuantity):
        available_quantity = self._inventory.get_productQuantity(nameProduct)

        if available_quantity >= requestedQuantity:
            if nameProduct in self._shoppingCart:
                self._shoppingCart[nameProduct] += requestedQuantity
            else:
                self._shoppingCart[nameProduct] = requestedQuantity
            self._inventory.remove_productQuantity(nameProduct, requestedQuantity)

            return "Filled the order"
        else:
            return "Can not fill the order"

    # Remove products from the shopping cart
    def remove_from_cart(self, nameProduct, requestedQuantity):
        # Check if the product is in the cart
        if nameProduct not in self._shoppingCart:
            return "Product not in the cart"

        # Check if the requested quantity is greater than what is in the cart
        if requestedQuantity > self._shoppingCart[nameProduct]:
            return "The requested quantity to be removed from cart exceeds what is in the cart"

        # Update the shopping cart and put the requested quantity back into the inventory
        self._shoppingCart[nameProduct] -= requestedQuantity
        self._inventory.add_productQuantity(nameProduct, requestedQuantity)

        return "Successful"

    # View the contents of the shopping cart
    def view_cart(self):
        total = 0

        # Loop to display product quantity and processing the total amount 
        for productName, quantity in self._shoppingCart.items():
            price_per_item = self._inventory.get_productPrice(productName)
            total += price_per_item * quantity
            print(f"{productName} {quantity}")

        print(f"Total: {total}")
        print(f"Buyer Name: {self._buyerName}")

# Definition of the Catalog class
class Catalog:
    # Initialize the product catalog
    def __init__(self):
        self._catalogData = []

    # Add a product to the catalog
    def addProduct(self, product):
        self._catalogData.append(product)

    # Categorize products by price and display the counts
    def price_category(self):
        low_prices = set()
        medium_prices = set()
        high_prices = set()

        # Categorizing products through for loop
        for product in self._catalogData:
            price = product.get_price()

            if 0 <= price <= 99:
                low_prices.add(product.get_name())
            elif 100 <= price <= 499:
                medium_prices.add(product.get_name())
            elif price >= 500:
                high_prices.add(product.get_name())
        
        print(f"Number of low price items: {len(low_prices)}")
        print(f"Number of medium price items: {len(medium_prices)}")
        print(f"Number of high price items: {len(high_prices)}")

    # Display the product catalog
    def display_catalog(self):
        for product in self._catalogData:
            print(f"Product: {product.get_name()} Price: {product.get_price()} Category: {product.get_category()}")

# Function to populate an inventory from a file
def populate_inventory(filename):
    try:
        invent = Inventory()

        # Open the file using with open
        with open(filename, 'r') as file:
            for line in file:
                name, price, quantity, _ = line.strip().split(',')
                invent.add_to_productInventory(name, int(price), int(quantity))

        return invent

    # When the file cannot be read
    except IOError:
        print(f"Could not read file: {filename}")
        return None

# Function to populate a catalog from a file
def populate_catalog(filename):
    try:
        catalog = Catalog()

        # Open the file using with open
        with open(filename, 'r') as file:
            for line in file:
                name, price, _, category = line.strip().split(',')
                product = Product(name, int(price), category)
                catalog.addProduct(product)

        return catalog

    # When the file cannot be read
    except IOError:
        print(f"Could not read file: {filename}")
        return None