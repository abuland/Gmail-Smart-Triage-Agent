import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_email(sender, subject, snippet):
    prompt = f"""
Classify the following email into ONE category.

Categories:
- Promotion
- Newsletter
- Personal
- Work
- Important

Email:
From: {sender}
Subject: {subject}
Snippet: {snippet}

Return only the category name.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()
