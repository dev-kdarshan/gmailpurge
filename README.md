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
