import json
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

CONFIG_DIR = os.path.expanduser("~/.gmailpurge")
TOKEN_PATH = os.path.join(CONFIG_DIR, "token.json")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")


def save_config(credentials_path):
    """Save GmailPurge configuration."""

    os.makedirs(CONFIG_DIR, exist_ok=True)

    with open(CONFIG_PATH, "w") as config:
        json.dump(
            {"credentials_path": credentials_path},
            config,
            indent=2
        )

    os.chmod(CONFIG_PATH, 0o600)


def load_config():
    """Load GmailPurge configuration."""

    if not os.path.exists(CONFIG_PATH):
        return None

    with open(CONFIG_PATH, "r") as config:
        return json.load(config)


def authenticate(credentials_path=None):
    """Authenticate the user with Google OAuth."""

    os.makedirs(CONFIG_DIR, exist_ok=True)

    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            TOKEN_PATH,
            SCOPES
        )

    if creds and creds.valid:
        return creds

    if credentials_path is None:
        config = load_config()

        if config:
            credentials_path = config.get("credentials_path")

    if not credentials_path:
        raise FileNotFoundError(
            "Google OAuth credentials are not configured."
        )

    credentials_path = os.path.expanduser(credentials_path)

    if not os.path.isfile(credentials_path):
        raise FileNotFoundError(
            f"Credentials file not found: {credentials_path}"
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path,
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    with open(TOKEN_PATH, "w") as token:
        token.write(creds.to_json())

    os.chmod(TOKEN_PATH, 0o600)

    save_config(credentials_path)

    return creds
