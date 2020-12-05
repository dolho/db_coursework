class Router:

    def __init__(self, controller):
        self.controller = controller
        self.routes = {}

    def register_command(self, command: str, function):
        self.routes[command] = function

    def handle_command(self, input):
        try:
            parts = input.split("/")
            command = parts[0] + '/' + parts[1] + '/'
            func = self.routes.get(command)
            if func:
                func()
            else:
                print(f'Command {input} not found')
        except IndexError as e:
            print("Incorrect command format. Maybe you've forgotten / "
                  "at the end?")