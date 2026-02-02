"""
Module for creating the menu interface for the user
"""

def main_menu():
    """
    Function for generating menu to interact with user.
    """
    while True:
        print("="*30)
        print("Welcome to McYfee Scraper")
        print("Please select option")
        print("="*30)
        print("1. Add scraper")
        print("2. Activate / Deactivate scraper")
        print("3. Activate / Deactivate notification")
        print("4. Generate report")
        print("5. Exit")

        print("="*30)

        option = input("Option: ")

        print("="*30)

        if option == "1":
            name = input("Name: ")
            url = input("URL: ")
            xpath = input("Please enter XPAth (leave empty if not applicable): ")
            css_selector = input("Please enter CSS Selector (leave empty if not applicable): ")
            notification = input("Activate notification (0/1): ")
            threshold = input("Please enter threshold value: ")
            interval = input("Enter interval (minutes): ")
            print("-"*30)
            print(f"Name: {name}")
            print(f"URL: {url} - XPath: {xpath} - CSS Selector: {css_selector}")
            print(f"Notification active? {notification}")
            print(f"Interval: {interval}")
            print(f"Threshold: {threshold}")
            print("-"*30)

        elif option == "2":
            while True:
                print("1. Activate scraper")
                print("2. Deactivate scraper")
                option_2 = input("Option: ")
                if option_2 == "1":
                    print("Showing deactivated scrapers")
                    break
                if option_2 == "1":
                    print("Showing deactivated scrapers")
                    break
                else:
                    print("Unknown selection. Please choose another.")

        elif option == "3":
            while True:
                print("1. Activate notification")
                print("2. Deactivate notification")
                option_3 = input("Option: ")
                if option_3 == "1":
                    print("Showing deactivated notifications")
                    break
                if option_3 == "1":
                    print("Showing deactivated notifications")
                    break
                else:
                    print("Unknown selection. Please choose another.")

        elif option == "4":
            print("Generating report...")

        elif option == "5":
            return

        else:
            print("Unknown selection. Please choose another.")

if __name__ == "__main__":
    main_menu()
