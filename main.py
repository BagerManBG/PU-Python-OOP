from Controllers.CarController import CarController


def main():
    car_controller = CarController()
    command = ''

    while command != 'stop':
        command = input('Please enter a command (list, rent, stop): ')
        car_controller.execute_command(command)


if __name__ == '__main__':
    main()
