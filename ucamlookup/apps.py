from django.apps import AppConfig


class UCamLookupConfig(AppConfig):
    name = 'ucamlookup'
    verbose_name = 'University of Cambridge Django Lookup app'

    def ready(self):
        super(UCamLookupConfig, self).ready()
        import ucamlookup.signals  # noqa: F401
