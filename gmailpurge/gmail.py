from googleapiclient.discovery import build


def create_gmail_service(credentials):
    """Create an authenticated Gmail API service."""
    return build("gmail", "v1", credentials=credentials)


def search_messages(gmail, query):
    """Return all Gmail messages matching the search query."""

    messages = []
    page_token = None

    while True:
        result = gmail.users().messages().list(
            userId="me",
            q=query,
            maxResults=500,
            pageToken=page_token
        ).execute()

        messages.extend(result.get("messages", []))

        page_token = result.get("nextPageToken")

        if not page_token:
            break

    return messages


def move_to_trash(gmail, messages):
    """Move messages to Gmail Trash in batches."""

    for i in range(0, len(messages), 1000):
        ids = [
            message["id"]
            for message in messages[i:i + 1000]
        ]

        gmail.users().messages().batchModify(
            userId="me",
            body={
                "ids": ids,
                "addLabelIds": ["TRASH"]
            }
        ).execute()
