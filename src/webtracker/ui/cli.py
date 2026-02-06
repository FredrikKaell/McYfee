"""
Module for creating the menu interface for the user
"""
import tldextract
from database import fetch_monitors, set_monitor_status, fetch_selectors, create_selector, create_monitor
from .selections import change_monitor_status

def check_existing_selectors(url):
    print(url)
    domain = tldextract.extract(url)
    print(domain)
    selectors = fetch_selectors(domain.domain)
    if not selectors:
        return False
    return selectors

def get_selector_by_id(selectors : list[dict], id : int):
    for selector in selectors:
        if selector['id'] == id:
            return selector

def add_monitor():
    """
    Function for adding monitor
    """
    is_creating_selector = True

    name = input("Name: ")
    url = input("URL: ")
    existing_selectors = check_existing_selectors(url)
    if existing_selectors:
        print("There are existing selectors. Would you like to use an existing?")
        while True:
            set_selector = input("Y/n: ")
            if set_selector.lower() == "y":
                is_creating_selector = False
                break
            elif set_selector.lower() == "n":
                is_creating_selector = True
                break
            else:
                print("Unvalid input!")

    if not is_creating_selector:
        allowed = []
        while True:
            for selector in existing_selectors:
                print(f"Id: {selector['id']} - {selector['name']}")
                allowed.append(selector['id'])

            print("To create own. Type 'q'")
            selection = input("Selection: ")

            if selection == "q":
                is_creating_selector = True
                break
            try:
                if int(selection) in allowed:
                    selected_selector = get_selector_by_id(existing_selectors, int(selection))
                    break
                else:
                    print("Non-valid input")
            except Exception as e:
                print(f"Error: {e}")

    if is_creating_selector or not existing_selectors:
        print("Creating new selector")
        selector_name = input("Name: ")
        xpath = input("Please enter XPAth (leave empty if not applicable): ")
        css_selector = input("Please enter CSS Selector (leave empty if not applicable): ")
        desc = input("Description: ")

        selected_selector = create_selector(selector_name, css_selector, xpath, tldextract.extract(url).domain, desc)

    notification = input("Activate notification (0/1): ")
    threshold = input("Please enter threshold value: ")
    interval = input("Enter interval (minutes): ")

    create_monitor(name=name, url=url, selector_id=selected_selector['id'], monitor_type='price', threshold=threshold, check_interval=interval, is_active=1)


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
        print("3. List active scrapers")
        print("4. Generate report")
        print("5. Exit")

        print("="*30)

        option = input("Option: ")

        print("="*30)

        if option == "1":
            add_monitor()

            # name = input("Name: ")
            # url = input("URL: ")
            # xpath = input("Please enter XPAth (leave empty if not applicable): ")
            # css_selector = input("Please enter CSS Selector (leave empty if not applicable): ")
            # notification = input("Activate notification (0/1): ")
            # threshold = input("Please enter threshold value: ")
            # interval = input("Enter interval (minutes): ")
            # print("-"*30)
            # print(f"Name: {name}")
            # print(f"URL: {url} - XPath: {xpath} - CSS Selector: {css_selector}")
            # print(f"Notification active? {notification}")
            # print(f"Interval: {interval}")
            # print(f"Threshold: {threshold}")
            # print("-"*30)

        elif option == "2":
            while True:
                print("1. Activate scraper")
                print("2. Deactivate scraper")
                option_2 = input("Option: ")
                if option_2 == "1":
                    deactivate_monitors()
                    break
                elif option_2 == "2":
                    activate_monitors()
                    break
                else:
                    print("Unknown selection. Please choose another.")

        elif option == "3":
            monitors = fetch_monitors(True)
            for monitor in monitors:
                print(f"Name: {monitor['name']}. Last known price: {monitor['last_extracted_value']}. Threshold: {monitor['threshold_value']}")
                print("-"*30)
               

        elif option == "4":
            print("Generating report...")

        elif option == "5":
            return

        else:
            print("Unknown selection. Please choose another.")

if __name__ == "__main__":
    main_menu()
