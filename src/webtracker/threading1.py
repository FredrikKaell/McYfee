"""
Module for threading
Scope of this module is to create a function to easy run functions on multiple threads
"""

import threading
from typing import Callable

class RunMultiple:
    """
    A class for running multiple functions concurrently using threads.
    
    The first function (`main_func`) is executed in a non-daemon thread,
    ensuring it can complete even if the main program exits.
    Additional functions (`*args`) are executed in daemon threads,
    which will be terminated when the main program finishes.
    
    Parameters:
        main_func (Callable): The main function to be run in a separate thread.
        *args (Callable): Additional functions to be run concurrently in daemon threads.
        
    Methods:
        start_threads():
            Starts all threads for specified functions.
    """

    def __init__(self, main_func : Callable, *args : Callable):
        self.main_func = main_func
        self.funcs = args
        self.threads = []

    def start_threads(self):
        """
        Starts all threads for specified functions.
        """
        try:
            thread = threading.Thread(target=self.main_func)
            self.threads.append(thread)
            thread.start()
        except (TypeError, RuntimeError) as e:
            print(f"Error setting main thread: {e}")

        for func in self.funcs:
            try:
                thread = threading.Thread(target=func, daemon=True)
                self.threads.append(thread)
                thread.start()
            except (TypeError, RuntimeError) as e:
                print(f"Error starting thread for {func} : {e}")
