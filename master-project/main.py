import threading
import time
from tkinter import *
from project import app
class SharedState:
    def __init__(self):
        self._lock = threading.Lock()
        self.running = True
        self._click_count = 0
    def record_click(self):
        # this gets called from the Flask thread to record a click
        with self._lock:
            self._click_count += 1
    def clicked(self):
        # this gets called from the GUI thread to 'get' a click
        with self._lock:
            if self._click_count > 0:
                self._click_count -= 1
                return True
            return False
    def stop(self):
        # called from either side to stop running
        with self._lock:
            self._running = False
def webserver(shared_state):
    app.app.config['SHARED'] = shared_state
    # It isn't safe to use the reloader in a thread
    app.app.run(host='127.0.0.1', debug=True, use_reloader=False)

def main():
    shared_state = SharedState()
    ui_thread = threading.Thread(target=webserver, args=(shared_state,))
    ui_thread.start()

    while shared_state.running:
        time.sleep(0.1)
        window=Tk()
# add widgets here

        window.title('Hello Python')
        window.geometry("300x200+10+20")
        window.mainloop()
    ui_thread.join()

if __name__ == '__main__':
    main()