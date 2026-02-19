#!/usr/bin/env python3
"""
Demo 02 - Step 3: Secure RAG Application

Build a Retrieval-Augmented Generation app with secure credentials.
"""

from pathlib import Path

if not Path(".avp_vault.enc").exists():
    print("❌ Vault not found. Run 01_setup_credentials.py first.")
    exit(1)

print("=" * 60)
print("SECURE RAG APPLICATION WITH AVP")
print("=" * 60)
print()

from avp_langchain import AVPCredentialProvider

# Load credentials
print("Loading credentials from AVP...")
credentials = AVPCredentialProvider(".avp_vault.enc", workspace="langchain")
available = credentials.list()

if "anthropic_api_key" not in available and "openai_api_key" not in available:
    print("❌ No API keys found. Run 01_setup_credentials.py")
    exit(1)

print("✅ Credentials loaded")
print()

# Build RAG components
print("Building RAG pipeline...")
print()

try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    # Create LLM with AVP credentials
    if "anthropic_api_key" in available:
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            api_key=credentials.get("anthropic_api_key"),
            max_tokens=500
        )
        print("  ✅ LLM: Claude 3 Haiku")
    else:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=credentials.get("openai_api_key"),
            max_tokens=500
        )
        print("  ✅ LLM: GPT-3.5 Turbo")

    # Simulated document store (in real app, use vector DB)
    documents = {
        "avp": """
        Agent Vault Protocol (AVP) is an open standard for secure credential
        management in AI agent systems. It provides 7 core operations: DISCOVER,
        AUTHENTICATE, STORE, RETRIEVE, DELETE, LIST, and ROTATE. AVP supports
        multiple backends including file-based encryption, OS keychain, and
        hardware security keys.
        """,
        "security": """
        AVP protects against common credential theft vectors including infostealer
        malware, environment variable leaks, and accidental git commits. By
        encrypting credentials at rest and providing session-based access, AVP
        ensures that even if an attacker gains filesystem access, they cannot
        read the stored secrets without the master key.
        """,
        "backends": """
        AVP supports four backend types: Memory (for testing), File (encrypted
        with AES-256-GCM or Fernet), Keychain (OS-native secure storage), and
        Hardware (USB security keys like NexusClaw). Each backend offers different
        security/convenience tradeoffs.
        """
    }

    def retrieve(query: str) -> str:
        """Simple keyword-based retrieval."""
        query_lower = query.lower()
        context_parts = []
        for key, doc in documents.items():
            if key in query_lower or any(word in doc.lower() for word in query_lower.split()):
                context_parts.append(doc.strip())
        return "\n\n".join(context_parts) if context_parts else "No relevant documents found."

    print("  ✅ Document store: 3 documents about AVP")

    # RAG prompt
    rag_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert on the Agent Vault Protocol (AVP).
Answer questions based on the provided context. Be concise and accurate.
If the context doesn't contain the answer, say so.

Context:
{context}"""),
        ("user", "{question}")
    ])

    # Build RAG chain
    rag_chain = (
        {"context": lambda x: retrieve(x["question"]), "question": lambda x: x["question"]}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    print("  ✅ RAG chain: built")
    print()

    # Interactive Q&A
    print("=" * 60)
    print("ASK QUESTIONS ABOUT AVP")
    print("=" * 60)
    print()
    print("Type your questions (or 'quit' to exit):")
    print()

    sample_questions = [
        "What is AVP?",
        "How does AVP protect against malware?",
        "What backends does AVP support?"
    ]

    print("Sample questions:")
    for i, q in enumerate(sample_questions, 1):
        print(f"  {i}. {q}")
    print()

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not question:
            continue
        if question.lower() in ["quit", "exit", "q"]:
            break

        # Check if user entered a number for sample question
        if question.isdigit() and 1 <= int(question) <= len(sample_questions):
            question = sample_questions[int(question) - 1]
            print(f"  → {question}")

        print()
        print("Thinking...")
        response = rag_chain.invoke({"question": question})
        print()
        print(f"AVP Expert: {response}")
        print()

except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Run: pip install -r requirements.txt")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    credentials.close()

print()
print("Session ended. Credentials securely released.")
