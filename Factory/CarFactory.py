import json

from Models.CarModel import CarModel


class CarFactory:
    cars = []

    def __init__(self):
        self.cars = []
        with open('cars.json') as json_file:
            data = json.load(json_file)
            for row in data:
                car = CarModel(row['plate_id'], row['brand'], row['model'], row['fuel_cost'], row['price_per_hour'],
                               row['price_per_day'], row['price_per_week'], row['available'])

                if car.available == 1:
                    self.cars.append(car)

    def get_car(self, plate_id):
        for car in self.cars:
            if car.plate_id == plate_id:
                return car
        return None

    def get_catalogue(self):
        if len(self.cars) == 0:
            return "The catalogue is empty."

        message = "Catalogue:\n"
        for car in self.cars:
            message += self.get_description(car)
        return message

    @staticmethod
    def get_description(car: CarModel):
        return "%s: %s %s with a fuel cost of %s/100.\n" \
               "Price per hour: $%s\n" \
               "Price per day: $%s\n" \
               "Price per week: $%s\n" \
               "\n" % (car.plate_id, car.brand, car.model, car.fuel_cost, car.price_per_hour, car.price_per_day,
                       car.price_per_week)
