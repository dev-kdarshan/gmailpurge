import os
import sys

from .auth import authenticate
from .auth import save_config
from .gmail import create_gmail_service
from .gmail import search_messages
from .gmail import move_to_trash


def setup():
    """Run first-time GmailPurge authentication."""

    print("\nGmailPurge Setup")
    print("================\n")

    print("Before continuing, you need a Google Cloud OAuth")
    print("credentials JSON file for a Desktop application.\n")

    print("If you do not have one yet, follow these steps:\n")

    print("1. Open Google Cloud Console:")
    print("   https://console.cloud.google.com/\n")

    print("2. Create a new Google Cloud project or select an existing one.\n")

    print("3. Enable the Gmail API:")
    print("   APIs & Services -> Library -> Gmail API -> Enable\n")

    print("4. Configure the OAuth consent screen:")
    print("   Google Auth Platform -> Branding / Audience")
    print("   Add your Google account as a test user if required.\n")

    print("5. Create an OAuth Client:")
    print("   Google Auth Platform -> Clients -> Create Client")
    print("   Application type: Desktop app\n")

    print("6. Download the OAuth credentials JSON file.\n")

    print("The downloaded file is usually located in your Downloads folder.")
    print("For example:")
    print("   ~/Downloads/client_secret_123456.json\n")

    print("Google's official Gmail API guide:")
    print("https://developers.google.com/workspace/gmail/api/quickstart/python\n")

    print("Once you have downloaded the JSON file, enter its path below.\n")

    credentials_path = input(
        "Enter path to your Google OAuth credentials JSON: "
    ).strip()

    credentials_path = os.path.expanduser(credentials_path)

    if not os.path.isfile(credentials_path):
        print("\nCredentials file not found.")
        print("Please check the path and try again.")
        return

    print("\nStarting Google authorization...\n")

    try:
        authenticate(credentials_path)

        save_config(credentials_path)

        print("\nGmail authorization successful.")
        print("GmailPurge is ready to use.")
        print("Run: gmailpurge\n")

    except Exception as error:
        print(f"\nAuthentication failed: {error}")

def run():
    """Run the GmailPurge cleanup workflow."""

    print("\nGmailPurge")
    print("==========\n")

    try:
        credentials = authenticate()
        gmail = create_gmail_service(credentials)

    except Exception as error:
        print(f"{error}")
        print("\nRun: gmailpurge setup")
        return

    query = input("Enter Gmail search query: ").strip()

    if not query:
        print("\nNo search query entered. Cancelled.")
        return

    print("\nSearching Gmail...")

    try:
        messages = search_messages(gmail, query)

    except Exception as error:
        print(f"\nGmail search failed: {error}")
        return

    print(f"\nFound {len(messages)} messages matching:")
    print(f"  {query}")

    if not messages:
        print("\nNothing to move.")
        return

    answer = input(
        "\nMove ALL of these messages to Trash? "
        "Type YES to continue: "
    )

    if answer != "YES":
        print("\nCancelled. Nothing was changed.")
        return

    try:
        move_to_trash(gmail, messages)

        print(
            f"\nDone. Moved {len(messages)} messages to Trash."
        )

    except Exception as error:
        print(f"\nOperation failed: {error}")


def main():
    if len(sys.argv) > 1:

        command = sys.argv[1].lower()

        if command == "setup":
            setup()
            return

        if command in ("--help", "-h"):
            print("""
GmailPurge - Gmail bulk cleanup CLI

Usage:
  gmailpurge setup       Configure GmailPurge authentication
  gmailpurge             Search and move Gmail messages to Trash
  gmailpurge --help      Show this help message
  gmailpurge --version   Show version
""")
            return

        if command in ("--version", "-v"):
            from . import __version__
            print(f"GmailPurge {__version__}")
            return

        print(f"Unknown command: {sys.argv[1]}")
        print("Run 'gmailpurge --help' for usage.")
        return

    run()
