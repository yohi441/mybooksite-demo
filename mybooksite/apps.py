from django.apps import AppConfig



class MybooksiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mybooksite'

    def ready(self):
        from mybooksite import signals