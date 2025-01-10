from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'myApp'

    def ready(self):
        import myApp.signals