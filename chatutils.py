import os
import openai

# Utilisez openai pour définir le modèle
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    completions = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    
    message = completions.choices[0].text.strip("\n")
    return message
