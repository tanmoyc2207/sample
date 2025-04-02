import sys
import os

# Ensure src is in Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the function to run CrewAI
from latest_ai.crew import run_crew

if __name__ == "__main__":
    pr_number = input("Enter GitHub PR number to review: ")
    
    # Run the CrewAI system
    run_crew(int(pr_number))
