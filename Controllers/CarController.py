import re
import json
from Factory.CarFactory import CarFactory


class CarController:
    factory = CarFactory()

    def execute_command(self, command):
        if command == 'list':
            self.list()
        elif command == 'rent':
            self.rent()
        elif command == 'stop':
            print('Have a nice day, bye.\n')
        else:
            print('This command does not exist.\n')

    def list(self):
        print(self.factory.get_catalogue())

    def rent(self):
        rent_regex = re.compile(r'^rent\s(?P<plate_id>[A-Z]{2}\s\d{4}\s[A-Z]{2})$')
        rent_time_regex = re.compile(r'^(?P<number>\d+)(?P<type>[hdw])$')
        order = []
        command = ''

        while command != 'cancel':
            command = input('Please enter a command (list, rent XX XXXX XX, cancel, complete): ')
            rent_match = rent_regex.match(command)

            if command == 'list':
                self.list()
            elif command == 'complete':
                completed = self.complete_order(order)
                if completed:
                    self.factory = CarFactory()
                    command = 'cancel'
            elif command == 'cancel':
                print('Order cancelled.\n')
            elif rent_match is not None:
                plate_id = rent_match.group('plate_id')
                car = self.factory.get_car(plate_id)

                if car is None:
                    print('A car with a number "%s" does not exist.\n' % plate_id)
                else:
                    print('You have chosen the following car:\n')
                    print(self.factory.get_description(car))

                    rent_time_match = None
                    rent_time = ''

                    while rent_time_match is None:
                        rent_time = input('Enter how long you wish to rent the car for in the format number|type('
                                          'hours, days, weeks) (6h, 3d, 1w): ')
                        rent_time_match = rent_time_regex.match(rent_time)

                    order_flag = False
                    for order_item in order:
                        if order_item['car'].plate_id == car.plate_id:
                            order_flag = True

                    if order_flag:
                        print('You have already rented this car.')
                    else:
                        order.append({
                            'car': car,
                            'time': rent_time_match,
                        })
                        print('Car "%s" successfully rented for %s.' % (plate_id, rent_time))
            else:
                print('This command does not exist.\n')

    @staticmethod
    def complete_order(order):
        price = 0
        car_plates = []

        for order_item in order:
            car_plates.append(order_item['car'].plate_id)
            number = order_item['time'].group('number')
            number_type = order_item['time'].group('type')

            if number_type == 'h':
                price += int(order_item['car'].price_per_hour) * int(number)
            elif number_type == 'd':
                price += int(order_item['car'].price_per_day) * int(number)
            elif number_type == 'w':
                price += int(order_item['car'].price_per_week) * int(number)

        if len(order) > 3:
            price -= price * 30 / 100

        print('Your total price is $%s.' % price)
        confirm = input('Would you like to complete the order (type "y" for yes and anything else for no): ')

        if confirm != 'y':
            return False

        with open('cars.json') as json_file:
            data = json.load(json_file)
            for row in data:
                if row['plate_id'] in car_plates:
                    row['available'] = 0

        with open('cars.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print('Your order was completed successfully.')
        return True
