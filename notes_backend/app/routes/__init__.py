"""
Route package initializer.

Ensures route modules are imported so their blueprints can be registered by the app.
"""
# PUBLIC_INTERFACE
def register_all_routes():
    """This function exists for clarity; importing this module loads route blueprints."""
    return True


# Import route modules for side effects (blueprint definitions)
from . import health  # noqa: F401
from . import notes   # noqa: F401
