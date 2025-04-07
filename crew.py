import os
from crewai import Agent, Task, Crew, Process
from tools.github_tool import GitHubTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ Ensure we create an instance of GitHubTool
github_tool = GitHubTool()

# 📌 Define the AI Agent for Code Review
reviewer_agent = Agent(
    role="GitHub Code Reviewer",
    goal="Analyze GitHub PRs and provide feedback on code quality and improvements.",
    backstory="An expert software engineer skilled in reviewing PRs, detecting bugs, and ensuring best coding practices.",
    verbose=True,
    memory=True,  # Enables memory for better review context
    tools=[github_tool],  # ✅ Ensure we pass an instance, not the class
)

# 📌 Define the Code Review Task
review_task = Task(
    description=(
        "Fetch details and code changes for PR #{pr_number} from GitHub.\n"
        "Analyze the changes and provide a structured code review, including:\n"
        "- Code quality\n"
        "- Security vulnerabilities\n"
        "- Performance optimizations\n"
        "- Best practices\n"
        "Your final output should be a structured review in markdown format."
    ),
    expected_output="A detailed PR review report in markdown format.",
    tools=[github_tool],  # ✅ Pass the instance
    agent=reviewer_agent,
)

# 📌 Define the Crew (Workflow)
crew = Crew(
    agents=[reviewer_agent],
    tasks=[review_task],
    process=Process.sequential,  # Tasks execute one after another
)

def run_crew(pr_number: int):
    """Function to execute CrewAI for a GitHub PR review."""
    print(f"🚀 Running CrewAI for PR #{pr_number}...")
    result = crew.kickoff(inputs={"pr_number": pr_number})
    print("\n📝 CrewAI Review Result:\n", result)

