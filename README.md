# GmailPurge — Gmail Bulk Cleanup Automation

A reusable command-line tool for bulk Gmail cleanup using Google Cloud OAuth, the Gmail API, Python, and Linux.

## Why I Built This

Gmail is great for searching emails, but cleaning up hundreds or thousands of messages manually can be tedious.

I ran into this problem while dealing with a large number of unwanted emails. Gmail's interface requires repetitive selection and deletion when working with large result sets, which makes bulk cleanup unnecessarily time-consuming.

Instead of repeating the same manual operation, I built **GmailPurge** as a practical automation solution.

The goal was not to invent a new email product. The goal was to solve a real-life problem using cloud APIs, secure authentication, Linux, and Python automation.

---

## Project Overview

GmailPurge allows a user to:

1. Authenticate with their own Google Cloud OAuth application.
2. Enter any Gmail search query supported by Gmail.
3. Retrieve all matching messages through the Gmail API.
4. Display the number of matching messages.
5. Require explicit confirmation before making changes.
6. Move all confirmed messages to Gmail Trash using the Gmail API.

The tool is intentionally **generic**. Search criteria are provided at runtime rather than being hard-coded into the application.

For example:

```text
from:example@example.com
subject:"Newsletter"
older_than:1y
```

Any valid Gmail search query can be supplied at runtime.

---

## Architecture

```text
                         GOOGLE CLOUD
                              │
                         OAuth Client
                              │
                     Gmail API + OAuth
                              │
                     gmail.modify scope
                              │
                              ▼
                       Linux / WSL
                              │
                     Python Virtual Env
                              │
                              ▼
                       GmailPurge CLI
                              │
                     Gmail API Authentication
                              │
                              ▼
                    User enters Gmail query
                              │
                              ▼
                    Retrieve matching messages
                              │
                              ▼
                         Show count
                              │
                              ▼
                     Exact "YES" confirmation
                              │
                              ▼
                       Gmail API batchModify
                              │
                              ▼
                          Gmail Trash
```

---

## How It Works

### 1. First-Time Setup

Run:

```bash
gmailpurge setup
```

GmailPurge asks for the path to the Google OAuth credentials JSON file created in Google Cloud.

The application then starts the Google OAuth authorization flow.

After successful authorization, GmailPurge stores its local configuration and OAuth token under:

```text
~/.gmailpurge/
```

The token is reused for future executions so the user does not need to authorize the application every time.

### 2. Run GmailPurge

After setup:

```bash
gmailpurge
```

The application prompts:

```text
Enter Gmail search query:
```

The user can enter any valid Gmail search query.

### 3. Search Gmail

GmailPurge sends the search query to the Gmail API.

The application handles API pagination so that it can retrieve all matching messages rather than processing only the first page of results.

The number of matching messages is then displayed.

Example:

```text
Found 113 messages matching:
  from:example@example.com
```

### 4. Confirm the Operation

Before modifying anything, GmailPurge asks:

```text
Move ALL of these messages to Trash? Type YES to continue:
```

The operation only proceeds when the user enters:

```text
YES
```

Any other input cancels the operation.

This confirmation step provides a simple safeguard against accidental bulk modification.

### 5. Move Messages to Trash

Confirmed messages are moved to Gmail Trash using the Gmail API's batch modification capability.

The tool does **not** permanently delete the messages.

Example:

```text
Done. Moved 113 messages to Trash.
```

---

## Google Cloud Setup

GmailPurge requires a Google Cloud project with Gmail API access and an OAuth client.

### Required Configuration

1. Create or select a Google Cloud project.
2. Enable the Gmail API.
3. Configure the OAuth consent screen.
4. Configure the application for the intended Google account.
5. Add your Google account as a test user if the OAuth application is in testing mode.
6. Create an OAuth client for a desktop application.
7. Download the OAuth credentials JSON file.

The credentials file is used locally during the initial GmailPurge setup.

**Never commit the credentials file or OAuth token to GitHub.**

---

## Installation

Clone the repository:

```bash
git clone https://github.com/dev-kdarshan/gmailpurge.git
cd gmailpurge
```

Create a Python virtual environment:

```bash
python3 -m venv gmail-venv
```

Activate it:

```bash
source gmail-venv/bin/activate
```

Install GmailPurge:

```bash
pip install -e .
```

The project dependencies are also listed in:

```text
requirements.txt
```

---

## Usage

### First-Time Setup

```bash
gmailpurge setup
```

### Run GmailPurge

```bash
gmailpurge
```

### Show Help

```bash
gmailpurge --help
```

### Show Version

```bash
gmailpurge --version
```

---

## Example Workflow

```text
$ gmailpurge

GmailPurge
==========

Enter Gmail search query: from:example@example.com

Searching Gmail...

Found 113 messages matching:
  from:example@example.com

Move ALL of these messages to Trash? Type YES to continue: YES

Done. Moved 113 messages to Trash.
```

The same application can then be reused with a completely different Gmail query.

---

## Technical Highlights

### Gmail API Integration

Uses the Gmail API to:

- Search messages.
- Retrieve all matching results.
- Batch-modify messages.
- Move confirmed messages to Trash.

### OAuth Authentication

Uses Google's OAuth 2.0 flow rather than storing a Gmail password in the application.

The application requests the:

```text
https://www.googleapis.com/auth/gmail.modify
```

scope.

### API Pagination

Gmail search results can span multiple API pages.

GmailPurge follows `nextPageToken` values until all matching message IDs have been retrieved.

### Batch Processing

Messages are processed using Gmail API batch modification requests instead of making an individual API request for every message.

### CLI Design

The project provides a real executable command:

```bash
gmailpurge
```

with separate setup, help, and version functionality.

### Reusable Configuration

OAuth configuration and authorization state are stored locally so that subsequent executions can use the existing authorization.

### Linux / WSL

The project was developed and tested in an Ubuntu environment running through WSL on Windows.

---

## Engineering Workflow

The project involved several practical engineering steps:

1. Identify a repetitive real-world task.
2. Evaluate existing Gmail automation options.
3. Configure Google Cloud and Gmail API access.
4. Configure OAuth authentication.
5. Test Gmail API access independently.
6. Implement Gmail search and pagination.
7. Implement safe bulk modification.
8. Add explicit user confirmation.
9. Convert the working script into a reusable Python package.
10. Add a CLI entry point.
11. Add persistent local configuration.
12. Add dependency management and Git hygiene.
13. Test the complete workflow end-to-end.

---

## Skills Demonstrated

This project demonstrates practical experience with:

- Google Cloud
- Gmail API
- OAuth 2.0
- API authentication
- REST API integration
- API pagination
- Batch processing
- Python
- Linux
- WSL
- Command-line applications
- Python packaging
- Virtual environments
- Git and GitHub
- Credential and token handling
- Defensive user confirmation
- Cloud service integration
- Automation

---

## Security Considerations

GmailPurge is designed to avoid requiring the user's Gmail password.

Important security practices include:

- OAuth authentication instead of password-based authentication.
- OAuth credentials kept outside the Git repository.
- OAuth tokens stored locally.
- Sensitive files excluded through `.gitignore`.
- Explicit confirmation before bulk modification.
- Messages moved to Trash rather than permanently deleted.

Users should never commit files containing OAuth credentials, access tokens, refresh tokens, or other secrets.

---

## Limitations

Current limitations include:

- Requires the user to create and configure a Google Cloud OAuth application.
- Requires Gmail API access.
- Designed for command-line use.
- The current operation moves messages to Trash rather than permanently deleting them.
- OAuth credentials must be configured separately by each user.

---

## Future Improvements

Possible future improvements include:

- Better command-line argument support.
- Optional dry-run mode.
- More detailed operation summaries.
- Improved error handling and retry logic.
- Additional Gmail actions beyond moving messages to Trash.
- Automated testing.
- Distribution through PyPI.
- Support for additional authentication and configuration workflows.

---

## Project Structure

```text
GmailPurge/
├── gmailpurge/
│   ├── __init__.py
│   ├── auth.py
│   ├── cli.py
│   └── gmail.py
├── .gitignore
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

## Final Outcome

GmailPurge turns a repetitive Gmail cleanup task into a reusable command-line workflow.

Instead of manually selecting and deleting large groups of messages, a user can authenticate once, provide a Gmail search query, review the number of matching messages, confirm the operation, and let the Gmail API handle the bulk action.

The project demonstrates how a practical everyday problem can be solved by combining **cloud services, APIs, authentication, Python automation, Linux, and software packaging**.

---

## License

This project is licensed under the MIT License.