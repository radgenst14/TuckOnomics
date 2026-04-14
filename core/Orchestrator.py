
class Orchestrator:
    # Menu String
    menu = ("TuckOnomics Menu:\n"
    "1) Add new position\n"
    "q) Quit\n"
    "Enter Selection... ")

    # List of valid menu options
    valid_menu_inputs = ["1", "q"]

    def __init__(self) -> None:
        pass

    def menu_input(self) -> str:
        while True:
            opt = input(self.menu)
            if opt in self.valid_menu_inputs:
                return opt
    
    def run(self):
        db = input("Welcome to TuckOnomics\n"
                   "What database would you like to access... ")
        print()

        while True:
            opt = self.menu_input()

            if opt == "1":
                pass
            
            elif opt == "q":
                break


