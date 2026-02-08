"""
Module for handling functions that are accessed through CLI menu
"""
import tldextract
from webtracker.database import database as db
from webtracker.utils import input_validator
from webtracker.reports import report_generator

from .helper import check_existing_selectors, get_selector_by_id


def change_monitor_status(active_monitors = True):
    """
    Function for changing status of monitors (activate / deactivate)
    """
    monitors = db.fetch_monitors(active_monitors)

    if active_monitors:
        print("Showing activate monitors")
    else:
        print("Showing deactivated monitors")

    # Check if there are any monitors to activate / deactivate
    if not monitors:
        if active_monitors:
            print("No monitors to activate!")
        else:
            print("No monitors to deactivate!")
        return

    # IDs are used for setting status. List to store allowed IDs
    allowed_ids = [post['id'] for post in monitors]

    # Print monitors whos status can be changed
    for post in monitors:
        print(f"id : {post['id']} - {post['name']}")
    print("Print 'q' to quit current selection")

    while True:
        selection = input("Select id to deactivate: ")
        try:
            if selection == "q":
                return
            if int(selection) in allowed_ids:
                db.set_monitor_status(int(selection), int(not active_monitors))
                return

        except Exception as e:
            print(f"Error: {e}")

        print("Unvalid selection.")

def add_monitor():
    """
    Function for adding monitor
    """
    is_creating_selector = True

    name = input("Name: ")
    url = input("URL: ")

    existing_selectors = check_existing_selectors(url)

    # Check if user wants to use an existing selector.
    if existing_selectors:
        print("There are existing selectors. Would you like to use an existing?")
        while True:
            use_existing_selector = input("Y/n: ")
            if use_existing_selector.lower() == "y":
                is_creating_selector = False
                break
            elif use_existing_selector.lower() == "n":
                break
            else:
                print("Unvalid selection!")

    # If user want to use an existing selector, possible selection are shown
    if not is_creating_selector:
        allowed = [selector['id'] for selector in existing_selectors]

        while True:
            for selector in existing_selectors:
                print(f"Id: {selector['id']} - {selector['name']}")

            print("To create own selector. Type 'q'")
            selection = input("Selection: ")

            if selection == "q":
                is_creating_selector = True
                break
            try:
                if int(selection) in allowed:
                    selected_selector = get_selector_by_id(existing_selectors, int(selection))
                    selector_id = selected_selector['id']
                    break
                else:
                    print("Unvalid selection!")
            except Exception as e:
                print(f"Error: {e}")

    if is_creating_selector or not existing_selectors:
        print("Creating new selector")
        selector_name = input("Name: ")
        css_selector = input("Please enter CSS Selector (leave empty if not applicable): ")
        desc = input("Description: ")

        selector_values = {
            "selector_name" : selector_name,
            "css_selector" : css_selector,
            "url_pattern" : tldextract.extract(url).domain,
            "description" : desc
        }
        data = input_validator.check_user_input(input_validator.CreateSelector, selector_values)

        selector_id = db.create_selector(
            data.selector_name, 
            None, data.css_selector, 
            data.url_pattern, 
            data.description
            )
    threshold = input("Please enter threshold value: ")
    interval = input("Enter interval (minutes): ")

    user_input = {
        "name" : name,
        "url" : url,
        "selector_id" : selector_id,
        "monitor_type" : "price",
        "threshold" : threshold,
        "check_intervall" : interval,
        "is_active" : 1,
        "notification_id" : 1
    }

    monitor_input = input_validator.check_user_input(input_validator.CreateMonitor, user_input=user_input)
    db.create_monitor(
        name=monitor_input.name,
        url=str(monitor_input.url),
        selector_id= monitor_input.selector_id,
        monitor_type=monitor_input.monitor_type,
        threshold=monitor_input.threshold,
        check_interval=monitor_input.check_intervall,
        is_active=monitor_input.is_active,
        notification_id=monitor_input.notification_id
        )

def create_report(monitor_id : int = None, days : int = 30):
    print("Generate report")
    monitor_id = input("Monitor ID:")
    days = input("Number of days to include: ")
    data = {
        "monitor_id" : monitor_id,
        "days" : days
    }

    values = input_validator.check_user_input(input_validator.CreateReport, data)
    report_generator.create_chart(values.monitor_id, values.days)