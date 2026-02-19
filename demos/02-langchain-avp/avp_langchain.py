"""
AVP-LangChain Integration

A credential provider that integrates AVP with LangChain applications.
"""

import getpass
from pathlib import Path
from typing import Optional

from avp import AVPClient
from avp.backends import FileBackend, MemoryBackend


class AVPCredentialProvider:
    """
    Credential provider for LangChain that uses AVP for secure storage.

    Usage:
        credentials = AVPCredentialProvider(".avp_vault.enc")
        api_key = credentials.get("anthropic_api_key")
    """

    def __init__(
        self,
        vault_path: str = ".avp_vault.enc",
        password: Optional[str] = None,
        workspace: str = "langchain"
    ):
        """
        Initialize the credential provider.

        Args:
            vault_path: Path to the AVP vault file
            password: Vault password (will prompt if not provided)
            workspace: AVP workspace name
        """
        self.vault_path = Path(vault_path)
        self.workspace = workspace
        self._client: Optional[AVPClient] = None
        self._session_id: Optional[str] = None

        # Get password
        if password is None:
            if not self.vault_path.exists():
                raise FileNotFoundError(
                    f"Vault not found: {vault_path}. "
                    "Run 01_setup_credentials.py first."
                )
            password = getpass.getpass("Enter vault password: ")

        self._password = password
        self._connect()

    def _connect(self):
        """Connect to the AVP vault."""
        backend = FileBackend(str(self.vault_path), self._password)
        self._client = AVPClient(backend)
        session = self._client.authenticate(workspace=self.workspace)
        self._session_id = session.session_id

    def get(self, name: str) -> str:
        """
        Retrieve a credential from the vault.

        Args:
            name: Name of the credential (e.g., "anthropic_api_key")

        Returns:
            The credential value as a string

        Raises:
            KeyError: If credential not found
        """
        try:
            result = self._client.retrieve(self._session_id, name)
            return result.value.decode()
        except Exception as e:
            raise KeyError(f"Credential '{name}' not found in vault: {e}")

    def set(self, name: str, value: str) -> None:
        """
        Store a credential in the vault.

        Args:
            name: Name of the credential
            value: The credential value
        """
        self._client.store(self._session_id, name, value.encode())

    def delete(self, name: str) -> bool:
        """
        Delete a credential from the vault.

        Args:
            name: Name of the credential

        Returns:
            True if deleted, False if not found
        """
        result = self._client.delete(self._session_id, name)
        return result.deleted

    def list(self) -> list[str]:
        """
        List all credential names in the vault.

        Returns:
            List of credential names
        """
        result = self._client.list_secrets(self._session_id)
        return [secret.name for secret in result.secrets]

    def rotate(self, name: str, new_value: str) -> None:
        """
        Rotate a credential (update with version tracking).

        Args:
            name: Name of the credential
            new_value: New credential value
        """
        self._client.rotate(self._session_id, name, new_value.encode())

    def close(self):
        """Close the vault connection."""
        if self._client:
            self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# Convenience function for quick access
def get_credential(name: str, vault_path: str = ".avp_vault.enc") -> str:
    """
    Quick way to get a single credential.

    Usage:
        api_key = get_credential("anthropic_api_key")
    """
    with AVPCredentialProvider(vault_path) as provider:
        return provider.get(name)
