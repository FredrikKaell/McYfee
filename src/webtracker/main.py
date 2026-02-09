from webtracker.ui.cli import main_menu 
from webtracker.core import tracker
from webtracker.config import colors

def logo():
    logo = r"""
    $$\      $$\         $$\     $$\  $$$$$$\                     
    $$$\    $$$ |        \$$\   $$  |$$  __$$\                    
    $$$$\  $$$$ | $$$$$$$\\$$\ $$  / $$ /  \__|$$$$$$\   $$$$$$\  
    $$\$$\$$ $$ |$$  _____|\$$$$  /  $$$$\    $$  __$$\ $$  __$$\ 
    $$ \$$$  $$ |$$ /       \$$  /   $$  _|   $$$$$$$$ |$$$$$$$$ |
    $$ |\$  /$$ |$$ |        $$ |    $$ |     $$   ____|$$   ____|
    $$ | \_/ $$ |\$$$$$$$\   $$ |    $$ |     \$$$$$$$\ \$$$$$$$\ 
    \__|     \__| \_______|  \__|    \__|      \_______| \_______|
    Monitoring concept by Youseff, Fredrik, Elvira and Emil for web                                                          
    """
    print(logo)

# Lets decide together what to do with this.

def menuoptions():
    print("-"*60)
    print("Choose one option!")
    print("-"*60)
    print("1. User menu")
    print("2. Run tracker service once.")
    print("3. Run tracker service as deamon.")
    print("0. Exit")
    print("-"*60)


def run(): 

    selection = 0

    while True:
        try:
            logo()
            menuoptions()
            selection = int(input())


            if selection < 0 or selection > 4:
                print("-"*60)
                print("Invalid selection, try again!")
                print("-"*60)
                continue

            elif selection == 1:
                main_menu()
                selection = 0

            elif selection == 2:
                tracker(daemon=False)
                selection = 0

            elif selection == 3:
                tracker(daemon=True)
                selection = 0

            elif selection == 0:
                break



        except ValueError:
            print("-"*60)
            print("Invalid selection, try again!")
            print("-"*60)
            continue

        except KeyboardInterrupt:
            print(f"Application was stopped with keyboard interrupt.")
            return

        except Exception as err:
            print(err)


if __name__ == "__main__":
    try:
        run()
    
    except KeyboardInterrupt:
        print(f"Application was stopped with keyboard interrupt.")

    except Exception as err:
        print(f"Application stopped with following: {err}")
