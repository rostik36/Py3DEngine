import sys
import os

# Add `core` to Python's module search path
sys.path.append(os.path.join(os.path.dirname(__file__), "core"))

from core.engine import Engine


if __name__ == "__main__":
    # Initialize engine
    engine = Engine()
    
    engine.init()
    
    engine.run()