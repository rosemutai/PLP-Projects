# Base class: Smartphone
class Smartphone:
    def __init__(self, brand, model, battery_life):
        self.brand = brand
        self.model = model
        self.battery_life = battery_life
    
    def call(self, contact):
        return f"{self.brand} {self.model} is calling {contact}..."
    
    def charge(self, hours):
        self.battery_life += hours
        return f"{self.brand} {self.model} charged. Battery life: {self.battery_life} hours."
    
    def __str__(self):
        return f"{self.brand} {self.model} (Battery: {self.battery_life} hrs)"


class GamingSmartphone(Smartphone):
    def __init__(self, brand, model, battery_life, cooling_system):
        super().__init__(brand, model, battery_life)
        self.cooling_system = cooling_system
    
    def play_game(self, game, hours):
        self.battery_life -= hours * 2
        return f"Playing {game} for {hours} hours... Battery left: {self.battery_life} hrs."
    
    def __str__(self):
        return f"{self.brand} {self.model} [Gaming Edition] - Cooling: {self.cooling_system}, Battery: {self.battery_life} hrs"


