class Ingredient:
    def __init__(self):
        self.quantity = 0
        self.measure = ""
        self.name = ""
        self.full = ""
        self.full_name = ""
        self.split_name = []
        self.nutrition = {
            'Calories': 0,
            'Fat': 0,
            'Carbohydrate': 0,
            'Protein': 0
        }
        self.parsed = False
        self.ignore = False
        self.current = []

    # def __str__(self):
    #     return f"qty = {self.quantity:.2f}; unit = {self.unit}; name = {self.name}; full = {self.full}; full_name = {self.full_name}; split_name = {self.split_name}; nutrition = {self.nutrition}"

    def __str__(self):
        return (
            f"Full: {self.full}".ljust(100) +
            f"\nparsed: {self.parsed}".ljust(18) +
            f"ignore: {self.ignore}".ljust(15) +
            f"Quantity: {self.quantity:.2f}".ljust(20) +
            f"Measure: {self.measure}".ljust(30) +
            f"Name: {self.name}".ljust(30) +            
            # f"\nFull Name: {self.full_name}".ljust(40) +
            f"\nSplit Name: {self.split_name}".ljust(50) +
            f"Nutrition: {self.nutrition}".ljust(25)
        )
