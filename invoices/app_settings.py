from django.conf import settings

PAYMENT_CORP = getattr(settings, "PAYMENT_CORP", 1639878825)

def discord_bot_active():
    return 'aadiscordbot' in settings.INSTALLED_APPS
