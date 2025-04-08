import os
from crewai import Agent, Task, Crew, Process
from latest_ai.tools.github_tool import GitHubTool

from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# ✅ Ensure we create an instance of GitHubTool
github_tool = GitHubTool()

# 📌 Define the AI Agent for Code Review
reviewer_agent = Agent(
    role="GitHub Code Reviewer",
    goal="Maintain enterprise-grade code quality by thoroughly reviewing GitHub pull requests ensuring adherence to internal guidelines, security standards, and architectural patterns.",
    backstory="You are a seasoned software engineer and code quality advocate embedded in a Fortune 500 dev team.You’ve led code audits, mentored engineers, and enforced enterprise-level coding practices",
    memory=True,
    verbose=True,  # Enables memory for better review context
    tools=[github_tool] # ✅ Ensure we pass an instance, not the class
)
# 📌 Define the AI Agent for Code Review
refactor_advisor = Agent(
    role="Refactoring Specialist",
    goal="Suggest improvements and optimizations",
    backstory="An expert in writing cleaner and more efficient code.",
    verbose=True,
    memory=True,  # Enables memory for better review context
   
)
# 📌 Define the Code Review Task
review_task = Task(
    description="""
    You are responsible for reviewing a new Pull Request (PR) on the company's GitHub repository.
    The PR to review is: {pr_number}
    Your task is to:
    - Assess the overall code quality and structure.
    - Ensure adherence to enterprise-level internal coding standards and naming conventions.
    - Detect any potential security issues or anti-patterns.
    - Confirm that the code changes align with existing architectural patterns and business logic.
    - Check for meaningful commit messages and clear documentation (if applicable).

    Your final answer MUST be a structured PR review containing:
    - ✅ Positive Highlights
    - ❌ Issues and Suggestions
    - 🔒 Security Concerns
    - 🏗️ Architectural Observations
    - 💬 Final Recommendation (approve, request changes, or block)

    Be critical, but constructive. Your review is used by senior engineers to make a release decision.
    """,
    expected_output="""
    A markdown-formatted review report with all required sections:
    ✅ Positive Highlights  
    ❌ Issues and Suggestions  
    🔒 Security Concerns  
    🏗️ Architectural Observations  
    💬 Final Recommendation  
    """,
    tools=[github_tool],  # ✅ Pass the instance
    agent=reviewer_agent,
)
# 📌 Define the suggest_improvements_task 
suggest_improvements_task = Task(
    description="""
    You are responsible for providing refactoring recommendations for a newly submitted enterprise-level pull request (PR).

    Your responsibilities include:
    - Identifying inefficient or redundant code patterns.
    - Suggesting performance optimizations (e.g., batch processing, lazy loading, caching).
    - Ensuring the code aligns with SOLID principles and enterprise architecture patterns (like MVC, service layers, etc.).
    - Highlighting opportunities to modularize or decouple components for better testability and maintainability.
    - Checking for unnecessary complexity, nested logic, or poor naming conventions.
    - Looking for repeated logic that can be abstracted into reusable components or services.
    - Evaluating logging and error-handling consistency.

    Pull Request Metadata:
    - PR Number: {pr_number}
    - Code Diff: (fetched via your tools)
    - Coding Guidelines: {enterprise_guidelines}

    Your final output MUST be a structured Markdown report with:
    ## 🔄 Code Improvements
    ## ⚙️ Performance Optimizations
    ## 📐 Architectural Recommendations
    ## 🧹 Cleanup & Formatting Suggestions
    ## ✅ Final Recommendation (Refactor Required / Looks Good / Needs Major Refactoring)
    """,
    expected_output="""
    A structured Markdown report with improvement suggestions, architecture feedback, performance notes, and a final summary call-to-action.
    """,
    agent=refactor_advisor
)
# 📌 Define the Crew (Workflow)
crew = Crew(
    agents=[reviewer_agent,refactor_advisor],
    tasks=[review_task,suggest_improvements_task],
    process=Process.sequential,  # Tasks execute one after another
)

def run_crew(pr_number: int, enterprise_guidelines: str = None):
    print(f"🚀 Running CrewAI for PR #{pr_number}...")

    inputs = {
        "pr_number": pr_number,
        "enterprise_guidelines": (
            f"- Coding Guidelines: {enterprise_guidelines}"
            if enterprise_guidelines else
            "- No specific enterprise coding guidelines provided."
        )
    }
    print(f"🚀 Running CrewAI for PR #{inputs}...")
    result = crew.kickoff(inputs=inputs)
    print("\n📝 CrewAI Review Result:\n", result)


