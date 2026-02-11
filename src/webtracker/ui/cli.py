"""
Module for creating the menu interface for the user
"""
import tldextract
import json
from webtracker.database import database as db
from webtracker.scraper import parse
from .selections import change_monitor_status, add_monitor, create_report



def check_existing_selectors(url):
    print(url)
    domain = tldextract.extract(url)
    print(domain)
    selectors = db.fetch_selectors(domain.domain)
    if not selectors:
        return False
    return selectors

def get_selector_by_id(selectors : list[dict], id : int):
    for selector in selectors:
        if selector['id'] == id:
            return selector
        
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
        print("5. Check selector")
        print("6. Exit")

        print("="*30)

        option = input("Option: ")

        print("="*30)

        if option == "1":
            add_monitor()

        elif option == "2":
            while True:
                print("1. Activate scraper")
                print("2. Deactivate scraper")
                option_2 = input("Option: ")
                if option_2 == "1":
                    change_monitor_status(False)
                    break
                elif option_2 == "2":
                    change_monitor_status(True)
                    break
                else:
                    print("Unknown selection. Please choose another.")

        elif option == "3":
            monitors = db.fetch_monitors(True)
            for monitor in monitors:
                last_extracted_value = json.loads(monitor['last_extracted_value'])
                print(f"Name: {monitor['name']}. Last known price: {last_extracted_value['current']}. Threshold: {monitor['threshold_value']}")
                print("-"*30)
               

        elif option == "4":
            create_report()
            
        elif option == "5":
            print("Check selector!")
            url = input("URL: ")
            css_selector = input("CSS Selector: ")
            data = {
                "xpath" : None,
                "css_selector" : css_selector
            }
            
            res = parse(url, data)
            print("-"*30)
            print("Following respons was returned")
            print(res)
            
        elif option == "6":
            return

        else:
            print("Unknown selection. Please choose another.")

if __name__ == "__main__":
    main_menu()
