import threading
import time 

def background_task(name):
    print(f'Task {name} started')
    time.sleep(3)
    print(f'Task {name} finished!')

my_thread = threading.Thread(target=background_task, args=('Download'))

my_thread.start()
print('Main program: Im still running while the task happens in the background')

my_thread.join()
print('Main program: All done.')