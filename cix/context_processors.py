def dark_mode(request):
    """Add dark_mode setting to template context."""
    dark_mode_enabled = False
    if request.user.is_authenticated:
        try:
            dark_mode_enabled = request.user.userprofile.dark_mode
        except AttributeError:
            pass
    return {'dark_mode': dark_mode_enabled}
