# SIMPLE IMPLEMENTATION

from abc import ABC, abstractmethod


class ObserverInf(ABC):
    @abstractmethod
    def update(self, temp: float):
        pass


class Subject(ABC):
    @abstractmethod
    def add(self, obj: ObserverInf):
        pass

    @abstractmethod
    def remove(self, obj: ObserverInf):
        pass

    @abstractmethod
    def notify(self):
        pass

    @abstractmethod
    def set_data(self, temp: float):
        pass


class WeatherStation(Subject):
    def __init__(self):
        self.observers_set = set()
        self.temperature = 0.0

    def add(self, observer: ObserverInf):
        self.observers_set.add(observer)

    def remove(self, observer: ObserverInf):
        if observer in self.observers_set:
            self.observers_set.remove(observer)

    def notify(self):
        for observer in self.observers_set:
            observer.update(self.temperature)

    def set_data(self, temp: float):
        print(f"\n🌡️ WeatherStation: New Temperature = {temp}°C")
        self.temperature = temp
        self.notify()


class ObserverConcrete(ObserverInf):
    def update(self, temp: float):
        print(f"📢 Observer received temperature update: {temp}°C")


if __name__ == "__main__":
    station = WeatherStation()

    observer1 = ObserverConcrete()
    observer2 = ObserverConcrete()

    station.add(observer1)
    station.add(observer2)

    station.set_data(23.4)
    station.set_data(54.4)

    station.remove(observer1)
    station.set_data(30.2)
