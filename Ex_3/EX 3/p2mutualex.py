import threading
import time
import random
from queue import PriorityQueue

class RicartAgrawala:
    def __init__(self, pid, total_processes):
        self.pid = pid
        self.processes = total_processes
        self.lock = threading.Lock()
        self.reply_count = 0
        self.requesting_CS = False
        self.timestamp = 0
        self.request_queue = PriorityQueue()

    def request_cs(self):
        self.requesting_CS = True
        self.timestamp += 1
        print(f"Process {self.pid} requests to enter the CS")
        for i in range(self.processes):
            if self.pid != i:
                self.send_message(i)
        while self.reply_count < self.processes - 1:
            time.sleep(1)
        self.enter_cs()

    def send_message(self, target_pid):
        print(f"Process {self.pid} sends message to {target_pid} at timestamp {self.timestamp}")
        processes[target_pid].receive_message(self)

    def receive_message(self, sender):
        with self.lock:
            self.timestamp = max(self.timestamp, sender.timestamp) + 1
            print(f"Process {self.pid} received message from {sender.pid}")
            if not self.requesting_CS or (sender.timestamp, sender.pid) < (self.timestamp, self.pid):
                self.send_reply(sender)
            else:
                self.request_queue.put((sender.timestamp, sender))

    def send_reply(self, recipient):
        print(f"Process {self.pid} replies to {recipient.pid}")
        recipient.receive_reply(self)

    def receive_reply(self, _):
        self.reply_count += 1

    def enter_cs(self):
        print(f"Process {self.pid} enters the CS at timestamp {self.timestamp}")
        time.sleep(random.uniform(0.5, 1.5))
        self.exit_cs()

    def exit_cs(self):
        self.reply_count = 0
        self.requesting_CS = False
        print(f"Process {self.pid} exits the CS at timestamp {self.timestamp}")
        while not self.request_queue.empty():
            _, process = self.request_queue.get()
            self.send_reply(process)

def process_action(process):
    process.request_cs()
    time.sleep(random.uniform(0.5, 1.5))

num_processes = 5
processes = [RicartAgrawala(i, num_processes) for i in range(num_processes)]
threads = [threading.Thread(target=process_action, args=(p,)) for p in processes]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
