from abc import ABC, abstractmethod


class ObserverInf(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def update(self, temp: float, station: str):
        pass


class Subject(ABC):
    def __init__(self, name: str):
        self.name = name

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
    def __init__(self, name: str):
        super().__init__(name)
        self.observers_set = set()
        self.temperature = 0.0

    def add(self, observer: ObserverInf):
        self.observers_set.add(observer)

    def remove(self, observer: ObserverInf):
        if observer in self.observers_set:
            self.observers_set.remove(observer)

    def notify(self):
        for observer in self.observers_set:
            observer.update(self.temperature, self.name)

    def set_data(self, temp: float):
        print(f"\n🌡️ {self.name}: New Temperature = {temp}°C")
        self.temperature = temp
        self.notify()


class ObserverConcrete(ObserverInf):
    def __init__(self, name: str):
        super().__init__(name)

    def update(self, temp: float, station: str):
        print(f"📢 {self.name} received temperature update: {temp}°C from {station}")


if __name__ == "__main__":
    station1 = WeatherStation("KASHMIR")
    station2 = WeatherStation("MASOORI")

    observer1 = ObserverConcrete("BHOPAL")
    observer2 = ObserverConcrete("INDORE")

    station2.add(observer2)
    station1.add(observer1)
    station2.add(observer1)

    station1.set_data(23.4)
    station2.set_data(54.4)

    station1.remove(observer1)
    station1.set_data(30.2)
