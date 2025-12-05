import openai

def ask_ai(question, snippet, api_key):
    openai.api_key = api_key
    prompt = f"{question}\n\nContext:\n{snippet}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']
