import os
from openai import OpenAI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def generate_response(prompt):
    chat_messages = get_chat_messages(prompt)

    if os.getenv("MODEL") == "mistral":
        if len(chat_messages) > 0 and chat_messages[len(chat_messages) - 1].role == "assistant":
            chat_messages.pop()
        return generate_response_mistral(chat_messages)
    elif os.getenv("MODEL") == "openai":
        return generate_response_openai(chat_messages)
    else:
        raise ValueError('Model to use not specified.')


def get_chat_messages(text):
    if os.getenv("MODEL") == '':
        raise ValueError('Model to use not specified.')

    chat_messages = []
    messages = text.split("[stop]")
    for msg in messages:
        role = "assistant" if msg.find("assistant:") != -1 else "user"
        message = msg.replace(f"{role}:", "").strip()

        if os.getenv("MODEL") == "mistral":
            chat_messages.append(ChatMessage(role=role, content=message))
        elif os.getenv("MODEL") == "openai":
            chat_messages.append({"role": role, "content": message})

    return chat_messages


def generate_response_openai(prompt):
    if os.getenv("OPENAI_API_KEY") == '':
        raise ValueError('OPENAI_API_KEY is missing.')

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.9,
        max_tokens=450,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
    )

    return completion.choices[0].message.strip("\n")


def generate_response_mistral(prompt):
    model = "mistral-tiny"
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    prompt.insert(0,
                  ChatMessage(
                      role="system", content="Language to use in your responses is French."))

    # No streaming
    chat_response = client.chat(
        model=model,
        messages=prompt,
        max_tokens=150
    )

    return chat_response.choices[0].message.content
