from django.apps import AppConfig


class NotificacoesConfig(AppConfig):
    name = 'notificacoes'

    # def ready(self):
    #     super(AppConfig, self).ready()
    #     # this is for backwards compability
    #     import notifications.signals
    #     notifications.notify = notifications.signals.notify