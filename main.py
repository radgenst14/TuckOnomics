"""
This is the main entry point for the application. It initializes the necessary components and starts the application.
"""

from core import Orchestrator

def main():
    orchestrator = Orchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()