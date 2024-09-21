from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from prometheus_client import Counter, Histogram
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the app, database, and migration objects
db = SQLAlchemy()
migrate = Migrate()

# Prometheus metrics initialization
dns_lookup_total = Counter(
    'dns_lookup_total',
    'Total number of DNS lookups'
)

dns_lookup_success = Counter(
    'dns_lookup_success',
    'Number of successful DNS lookups'
)

dns_lookup_failure = Counter(
    'dns_lookup_failure',
    'Number of failed DNS lookups'
)

dns_lookup_duration = Histogram(
    'dns_lookup_duration_seconds',
    'DNS lookup duration in seconds'
)


def create_app(config=None):
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Load configuration from a config file
    app.config.from_object(
        'config.Config'
    )

    # Apply custom config (for testing, etc.)
    if config:
        app.config.update(config)
    # Initialize the database and migration with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints for routes
    from app.routes.health import health_blueprint
    from app.routes.lookup import lookup_blueprint
    from app.routes.validate import validate_blueprint
    from app.routes.history import history_blueprint
    from app.routes.status import status_blueprint

    app.register_blueprint(health_blueprint)
    app.register_blueprint(lookup_blueprint)
    app.register_blueprint(validate_blueprint)
    app.register_blueprint(history_blueprint)
    app.register_blueprint(status_blueprint)

    # Register the metrics blueprint
    from app.metrics import metrics_blueprint
    app.register_blueprint(metrics_blueprint)

    return app
