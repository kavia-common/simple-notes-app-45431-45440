from flask_smorest import Blueprint
from flask.views import MethodView

# Keep the name as-is for backward compatibility in tags, but fix internal description
blp = Blueprint("Healt Check", __name__, url_prefix="/", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    def get(self):
        """Health check endpoint."""
        return {"message": "Healthy"}
