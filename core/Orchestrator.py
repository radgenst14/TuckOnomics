
from db import Database

class Orchestrator:
    # Menu String
    menu = ("TuckOnomics Menu:\n"
    "1) Add new position\n"
    "2) Review\n"
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
        db_name = input("Welcome to TuckOnomics\n"
                   "What database would you like to access... ")

        db =Database(db_name)

        opt = input("If you would like to delete, hit d. Otherwise press enter to continue... ")
        print()

        if opt == "d":
            db.remove_db()
            return
        
        while True:
            opt = self.menu_input()
            print()

            if opt == "1":
                pass
            
            elif opt == "2":
                pass

            elif opt == "q":
                break
            


