import asyncio
import logging
import json
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ig_parse import get_instagram_posts
from random import randint

from groq import Groq

API_URL = "https://api.aimlapi.com/chat/completions"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'
}

client = Groq(
    api_key='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')


def query(payload):
    payload = json.dumps({
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "messages": [
            {
                "role": "user",
                "content": f"Проанализируй настроение сообщения: '{payload}'"
            }
        ],
        "max_tokens": 512,
        "stream": False
    })

    # response = requests.post(API_URL, headers=headers,
    #                          data=payload.encode("utf-8"))

    # if (response.ok == False):
    #     logging.error(f"Error: {response.text}")
    #     return "Error"

    # return response.json()["choices"][0]["message"]["content"]

    chat_completionm = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Проанализируй настроение сообщения, в нем представлено описание поста, а также комментарии к нему, отдельно сделай анализ по комментариям: '{payload}'"
            }
        ],
        model="llama3-8b-8192",
        max_tokens=512,
        stream=False
    )

    return chat_completionm.choices[0].message.content


def send_email(subject, body, to_email):
    from_email = "macinchicken@alwaysdata.net"
    from_password = "TopFood2024"

    # Set up the server
    server = smtplib.SMTP(host='smtp-macinchicken.alwaysdata.net')
    server.starttls()
    server.login(from_email, from_password)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the message
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    server.send_message(msg)
    server.quit()


async def fetch_and_process_instagram_posts():
    session_file = "your_instagram_session"
    username = "stardust_rq"

    report = ""

    posts = get_instagram_posts('jas.almaty', session_file)
    for post in posts:
        mood = query(f"Описание поста: {post['caption']}, Комментарии к посту: {post['comments']}")
        print(post['comments'])
        report += f'Post shortcode: {post['url']}\n{mood}\n\n'

    open('report.md', 'w').write(report)

if __name__ == '__main__':
    asyncio.run(fetch_and_process_instagram_posts())
