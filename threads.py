import threading

class Thread_handler:
    def __init__(self):
        self.threads = []
        self.events = {}
        self.events['thread_loop'] = threading.Event()
        self.threads.append(threading.Thread(target=self.thread_loop, name='thread_loop'))
        self.threads[0].start()

    def thread_loop(self):
        while True:
            if (self.events['thread_loop'].is_set()):
                self.stop_all_threads()

                for thread in self.threads:
                    if thread.name != 'thread_loop' and thread.is_alive():
                        try:
                            self.threads[0].join(thread)
                        except Exception:
                            pass
                return True

            #for thread in self.threads:
            #    if thread.is_alive():
            #        thread.handled = False
            #    else:
            #        thread.handled = True
            #self.threads = [thread for thread in self.threads if not thread.handled]

    def new_thread(self, function, args=(), name=None):
        self.threads.append(threading.Thread(target=function, args=args, name=name))
        if name:
            self.events[name] = threading.Event()
        self.threads[-1].start()

    def stop_all_threads(self):
        for event in self.events.values():
            event.set()

    def stop_thread(self, name):
        self.events[name].set()

thread_handler = Thread_handler()
