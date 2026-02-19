"""
AVP-CrewAI Integration

Credential management for multi-agent CrewAI applications.
"""

import getpass
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from avp import AVPClient
from avp.backends import FileBackend


class AVPCredentialManager:
    """
    Credential manager for CrewAI that uses AVP for secure storage.

    Features:
    - Workspace isolation per agent/crew
    - Credential access auditing
    - Hot credential rotation
    - Multi-provider support

    Usage:
        manager = AVPCredentialManager(".avp_vault.enc")
        llm = manager.get_llm("researcher-workspace")
    """

    def __init__(
        self,
        vault_path: str = ".avp_vault.enc",
        password: Optional[str] = None
    ):
        self.vault_path = Path(vault_path)
        self._client: Optional[AVPClient] = None
        self._sessions: Dict[str, str] = {}  # workspace -> session_id
        self._audit_log: list = []

        if password is None:
            if not self.vault_path.exists():
                raise FileNotFoundError(f"Vault not found: {vault_path}")
            password = getpass.getpass("Enter vault password: ")

        self._password = password
        self._connect()

    def _connect(self):
        """Connect to the AVP vault."""
        backend = FileBackend(str(self.vault_path), self._password)
        self._client = AVPClient(backend)

    def _get_session(self, workspace: str) -> str:
        """Get or create a session for a workspace."""
        if workspace not in self._sessions:
            session = self._client.authenticate(workspace=workspace)
            self._sessions[workspace] = session.session_id
            self._log_access(workspace, "session_created")
        return self._sessions[workspace]

    def _log_access(self, workspace: str, action: str, credential: str = None):
        """Log credential access for auditing."""
        self._audit_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "workspace": workspace,
            "action": action,
            "credential": credential
        })

    def get(self, workspace: str, name: str) -> str:
        """
        Get a credential from a specific workspace.

        Args:
            workspace: The workspace/agent namespace
            name: Credential name

        Returns:
            The credential value
        """
        session_id = self._get_session(workspace)
        result = self._client.retrieve(session_id, name)
        self._log_access(workspace, "retrieve", name)
        return result.value.decode()

    def set(self, workspace: str, name: str, value: str, labels: dict = None):
        """
        Store a credential in a specific workspace.

        Args:
            workspace: The workspace/agent namespace
            name: Credential name
            value: Credential value
            labels: Optional metadata labels
        """
        session_id = self._get_session(workspace)
        self._client.store(session_id, name, value.encode(), labels=labels)
        self._log_access(workspace, "store", name)

    def rotate(self, workspace: str, name: str, new_value: str):
        """Rotate a credential with version tracking."""
        session_id = self._get_session(workspace)
        self._client.rotate(session_id, name, new_value.encode())
        self._log_access(workspace, "rotate", name)

    def list_credentials(self, workspace: str) -> list:
        """List all credentials in a workspace."""
        session_id = self._get_session(workspace)
        result = self._client.list_secrets(session_id)
        return [s.name for s in result.secrets]

    def get_llm(self, workspace: str, provider: str = "auto"):
        """
        Get an LLM instance with credentials from the specified workspace.

        Args:
            workspace: Workspace to get credentials from
            provider: "anthropic", "openai", or "auto" (detect from available keys)

        Returns:
            A LangChain LLM instance
        """
        available = self.list_credentials(workspace)

        if provider == "auto":
            if "anthropic_api_key" in available:
                provider = "anthropic"
            elif "openai_api_key" in available:
                provider = "openai"
            else:
                raise ValueError(f"No API keys found in workspace '{workspace}'")

        if provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            api_key = self.get(workspace, "anthropic_api_key")
            return ChatAnthropic(
                model="claude-3-haiku-20240307",
                api_key=api_key,
                max_tokens=500
            )

        elif provider == "openai":
            from langchain_openai import ChatOpenAI
            api_key = self.get(workspace, "openai_api_key")
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=api_key,
                max_tokens=500
            )

        else:
            raise ValueError(f"Unknown provider: {provider}")

    def get_audit_log(self) -> list:
        """Get the credential access audit log."""
        return self._audit_log.copy()

    def print_audit_log(self):
        """Print the audit log in a readable format."""
        print("\nCredential Access Audit Log:")
        print("-" * 60)
        for entry in self._audit_log:
            cred = entry.get("credential", "")
            cred_str = f" ({cred})" if cred else ""
            print(f"  {entry['timestamp']} | {entry['workspace']:20} | {entry['action']}{cred_str}")
        print("-" * 60)

    def close(self):
        """Close all sessions and the vault connection."""
        if self._client:
            self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
