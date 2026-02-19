#!/usr/bin/env python3
"""
Demo 03 - Step 2: Basic CrewAI with AVP

Run a simple crew with AVP-managed credentials.
"""

from pathlib import Path

if not Path(".avp_vault.enc").exists():
    print("❌ Vault not found. Run 01_setup_agents.py first.")
    exit(1)

print("=" * 60)
print("CREWAI WITH AVP CREDENTIALS")
print("=" * 60)
print()

from avp_crewai import AVPCredentialManager

# Initialize credential manager
print("Initializing AVP credential manager...")
manager = AVPCredentialManager(".avp_vault.enc")
print("✅ Connected to vault")
print()

# Check available workspaces
workspaces = ["researcher", "writer", "analyst"]
print("Checking agent workspaces...")
for ws in workspaces:
    creds = manager.list_credentials(ws)
    print(f"  • {ws}: {len(creds)} credential(s)")
print()

# Create LLMs for each agent using AVP
print("Creating LLMs with AVP credentials...")
print()

try:
    researcher_llm = manager.get_llm("researcher")
    print("  ✅ Researcher LLM ready")

    writer_llm = manager.get_llm("writer")
    print("  ✅ Writer LLM ready")

    analyst_llm = manager.get_llm("analyst")
    print("  ✅ Analyst LLM ready")
except Exception as e:
    print(f"  ❌ Error: {e}")
    manager.close()
    exit(1)

print()

# Try importing CrewAI
try:
    from crewai import Agent, Task, Crew

    print("Creating CrewAI agents...")
    print()

    researcher = Agent(
        role="Researcher",
        goal="Research and gather information about AI security",
        backstory="Expert researcher specializing in AI security topics",
        llm=researcher_llm,
        verbose=True
    )

    writer = Agent(
        role="Writer",
        goal="Write clear, concise content about technical topics",
        backstory="Technical writer with expertise in security documentation",
        llm=writer_llm,
        verbose=True
    )

    print("  ✅ Researcher agent created")
    print("  ✅ Writer agent created")
    print()

    # Create a simple task
    print("Creating tasks...")
    research_task = Task(
        description="In 2-3 sentences, explain why API key security matters for AI agents.",
        expected_output="A brief explanation of API key security importance",
        agent=researcher
    )

    write_task = Task(
        description="Take the research and write a one-paragraph summary suitable for developers.",
        expected_output="A developer-friendly paragraph about API key security",
        agent=writer
    )

    print("  ✅ Tasks created")
    print()

    # Run the crew
    print("=" * 60)
    print("RUNNING CREW")
    print("=" * 60)
    print()

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        verbose=True
    )

    result = crew.kickoff()

    print()
    print("=" * 60)
    print("CREW OUTPUT")
    print("=" * 60)
    print()
    print(result)

except ImportError:
    print("CrewAI not installed. Demonstrating credential usage without CrewAI...")
    print()

    from langchain_core.prompts import ChatPromptTemplate

    # Simulate agent work with just LangChain
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a {role}. Be concise."),
        ("user", "{task}")
    ])

    print("Simulating Researcher agent...")
    chain = prompt | researcher_llm
    research = chain.invoke({
        "role": "security researcher",
        "task": "In one sentence, why is API key security important?"
    })
    print(f"  Researcher: {research.content}")
    print()

    print("Simulating Writer agent...")
    chain = prompt | writer_llm
    written = chain.invoke({
        "role": "technical writer",
        "task": f"Rewrite this for developers: {research.content}"
    })
    print(f"  Writer: {written.content}")

print()
print("=" * 60)
print("CREDENTIAL ACCESS AUDIT")
print("=" * 60)
manager.print_audit_log()

manager.close()
print()
print("Session complete. All credentials securely released.")
