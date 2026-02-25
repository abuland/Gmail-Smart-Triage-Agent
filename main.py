from gmail_client import get_gmail_service, get_or_create_label
from ai_triage import classify_email


def main():
    print("🔍 Checking inbox...")

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=5,
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        print("No unread emails 🎉")
        return

    print(f"Fetched {len(messages)} unread emails:\n")

    LABEL_MAP = {
        "Promotion": "AI/Promotions",
        "Newsletter": "AI/Newsletters",
        "Personal": "AI/Personal",
        "Work": "AI/Work",
        "Important": "AI/Important",
    }

    for msg in messages:
        msg_id = msg["id"]

        message = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="metadata",
            metadataHeaders=["From", "Subject"],
        ).execute()

        headers = message["payload"]["headers"]
        sender = subject = "Unknown"

        for h in headers:
            if h["name"] == "From":
                sender = h["value"]
            elif h["name"] == "Subject":
                subject = h["value"]

        snippet = message.get("snippet", "")

        print("📩 From:", sender)
        print("📝 Subject:", subject)
        print("🔍 Snippet:", snippet)

        category = classify_email(sender, subject, snippet)
        print("🏷 Category:", category)

        label_name = LABEL_MAP.get(category, "AI/Other")
        label_id = get_or_create_label(service, label_name)

        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={
                "addLabelIds": [label_id],
                "removeLabelIds": ["UNREAD"],
            },
        ).execute()

        print(f"✅ Labeled as {label_name} & marked read")
        print("-" * 50)


if __name__ == "__main__":
    main()
