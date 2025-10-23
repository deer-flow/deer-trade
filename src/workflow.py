import logging
from src.graph import build_graph
from src.config import load_yaml_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default level is INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def enable_debug_logging():
    """Enable debug level logging for more detailed execution information."""
    logging.getLogger("src").setLevel(logging.DEBUG)


logger = logging.getLogger(__name__)

# Create the graph
config = load_yaml_config()
graph = build_graph(config.get("SELECTED_ANALYSTS"))


if __name__ == "__main__":
    print(graph.get_graph(xray=True).draw_mermaid())
