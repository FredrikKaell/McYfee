"""
Module for creating the menu interface for the user
"""

def run():
    is_running = True

    def main_menu():
        nonlocal is_running
        print("-"*30)
        print("Menu:")
        print("-"*30)
        print("1. Check current jobs")
        print("2. Create report")
        print("3. Quit")
        print("-"*30)
        selection = input("Selection: ")

        if selection == "1":
            print("Checking current jobs...")
        elif selection == "2":
            print("Creating report...")
        elif selection == "3":
            is_running = False
        else:
            print("Invalid selection!")
            main_menu()

    def report_menu():
        nonlocal is_running
        print("-"*30)
        print("Create report:")
        print("-"*30)
        print("")
        print("")
        print("")
                
    while is_running:
        main_menu()

if __name__ == "__main__":
    run()
