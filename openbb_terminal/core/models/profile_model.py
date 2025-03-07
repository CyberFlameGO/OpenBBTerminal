from typing import Dict

from pydantic.dataclasses import dataclass


@dataclass(config=dict(validate_assignment=True, frozen=True))
class ProfileModel:
    """Data model for profile."""

    token_type: str = ""
    token: str = ""
    uuid: str = ""
    email: str = ""
    username: str = ""

    def load_user_info(self, session: dict, email: str):
        """Load user info from login info.

        Parameters
        ----------
        session : dict
            The login info.
        email : str
            The email.
        """
        self.token_type = session.get("token_type", "")
        self.token = session.get("access_token", "")
        self.uuid = session.get("uuid", "")
        self.email = email
        self.username = self.email[: self.email.find("@")]

    def get_uuid(self) -> str:
        """Get uuid.

        Returns
        -------
        str
            The uuid.
        """
        return self.uuid

    def get_token(self) -> str:
        """Get token.

        Returns
        -------
        str
            The token.
        """
        return self.token

    def get_session(self) -> Dict[str, str]:
        """Get session info.

        Returns
        -------
        Dict[str, str]
            The session info.
        """
        return {
            "token_type": self.token_type,
            "access_token": self.token,
            "uuid": self.uuid,
        }

    def get_auth_header(self) -> str:
        """Get auth header.

        Returns
        -------
        str
            The auth header, e.g. "Bearer <token>".
        """
        return f"{self.token_type.title()} {self.token}"
