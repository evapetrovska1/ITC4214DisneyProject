from django.contrib import messages

# DEFINE WELCOME FUNCTION FOR EACH USER

def welcome_user(request):
    if not request.user.is_authenticated:
        return {'welcome_message': None}

    # Look for a fresh success message from messages framework
    welcome = None
    for msg in messages.get_messages(request):
        if msg.tags and 'success' in msg.tags:
            welcome = msg.message
            break

    # If no success message, just say "Welcome back"
    if not welcome:
        welcome = f"Welcome back, {request.user.get_username()}!"

    return {'welcome_message': welcome}