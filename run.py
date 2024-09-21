import logging
import signal
import sys
from app import create_app


# Setup logging for access logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
)


# Graceful shutdown function
def graceful_shutdown(signum, frame):
    logging.info("Gracefully shutting down the server...")
    sys.exit(0)


# Handle Ctrl+C keyboard interrupt
signal.signal(signal.SIGINT, graceful_shutdown)
# Handle kill command
signal.signal(signal.SIGTERM, graceful_shutdown)


# Create the Flask app using the factory function
app = create_app()

if __name__ == '__main__':
    # Start Flask app with access logs and set to run on port 3000
    app.run(debug=True, host='0.0.0.0', port=3000)
