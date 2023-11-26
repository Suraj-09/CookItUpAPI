class Ingredient:
    def __init__(self):

        #ingredients initialisation 
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

        # set the parameters to default
        self.parsed = False
        self.ignore = False
        self.current = []

    # ingredients output format
    def __str__(self):
        return (
            f"Full: {self.full}".ljust(100) +
            f"\nparsed: {self.parsed}".ljust(18) +
            f"ignore: {self.ignore}".ljust(15) +
            f"Quantity: {self.quantity:.2f}".ljust(20) +
            f"Measure: {self.measure}".ljust(30) +
            f"Name: {self.name}".ljust(30) +            
            f"\nSplit Name: {self.split_name}".ljust(50) +
            f"Nutrition: {self.nutrition}".ljust(25)
        )
