import logging

# Set up basic logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # Shows all messages including DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger object
logger = logging.getLogger("todoapp")
