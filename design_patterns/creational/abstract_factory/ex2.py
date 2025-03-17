# Notification System with abstract pattern

from abc import ABC, abstractmethod


class AlertNotification(ABC):
    @abstractmethod
    def send_alert_notification(self):
        pass

class RemindNotification(ABC):
    @abstractmethod
    def send_remind_notification(self):
        pass


class EmailAlertNotification(AlertNotification):
    def send_alert_notification(self):
        print("Email alert notification sent")
    

class SmsAlertNotification(AlertNotification):
    def send_alert_notification(self):
        print("SMS alert notification sent")

class PushAlertNotification(AlertNotification):
    def send_alert_notification(self):
        print("Push alert notification sent")


class EmailRemindNotification(RemindNotification):
    def send_remind_notification(self):
        print("Email remind notification sent")

class SmsRemindNotification(RemindNotification):
    def send_remind_notification(self):
        print("SMS remind notification sent")

class PushRemindNotification(RemindNotification):
    def send_remind_notification(self):
        print("Push remind notification sent")


class NotificationFactory(ABC):
    @abstractmethod
    def create_alert_notification(self):
        pass

    @abstractmethod
    def create_remind_notification(self):
        pass


class SmsNotificationFactory(NotificationFactory):
    def create_alert_notification(self):
        return SmsAlertNotification()

    def create_remind_notification(self):
        return SmsRemindNotification()
    

class EmailNotificationFactory(NotificationFactory):
    def create_alert_notification(self):
        return EmailAlertNotification()

    def create_remind_notification(self):
        return EmailRemindNotification()
    

class PushNotificationFactory(NotificationFactory):
    def create_alert_notification(self):
        return PushAlertNotification()

    def create_remind_notification(self):
        return PushRemindNotification()


class Application:
    def __init__(self, factory: NotificationFactory):
        self.factory = factory
        self.alert_notification = factory.create_alert_notification()
        self.remind_notification = factory.create_remind_notification()

    def notify(self):
        self.alert_notification.send_alert_notification()
        self.remind_notification.send_remind_notification()  


if __name__ == '__main__':
    print("App: Launched with SMS Notification Factory.")
    app = Application(SmsNotificationFactory())  
    app.notify()

    print("\nApp: Launched with Email Notification Factory.")
    app = Application(EmailNotificationFactory())  
    app.notify()

        