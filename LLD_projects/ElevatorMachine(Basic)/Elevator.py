from Direction import Direction
from threading import Condition, Lock
from Request import Request
import time


class Elevator:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity  # maximum no of requests
        self.current_floor = 1
        self.current_direciton = Direction.UP
        self.requests = []
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def add_request(self, request):
        with self.lock:
            if len(self.requests) < self.capacity:
                self.requests.append(request)
                print(
                    f"Elevator {self.id} added request from source : {request.source_floor} to : {request.destination_floor}"
                )
                self.condition.notify_all()
            else:
                print("Capacity reached of Elevator {self.id}")

    def get_next_request(self) -> Request:
        with self.lock:
            while not self.requests:
                self.condition.wait()
            return self.requests.pop(0)

    def process_requests(self):
        while True:
            request = self.get_next_request()
            self.process_request(request)

    def process_request(self, request: Request):
        start_floor = self.current_floor
        end_floor = request.destination_floor

        if start_floor < end_floor:
            self.current_direction = Direction.UP
            for i in range(start_floor, end_floor + 1):
                self.current_floor = i
                print(f"Elevator {self.id} reached floor {self.current_floor}")
                time.sleep(1)  # Simulating elevator movement
        elif start_floor > end_floor:
            self.current_direction = Direction.DOWN
            for i in range(start_floor, end_floor - 1, -1):
                self.current_floor = i
                print(f"Elevator {self.id} reached floor {self.current_floor}")
                time.sleep(1)  # Simulating elevator movement

    def run(self):
        self.process_requests()
