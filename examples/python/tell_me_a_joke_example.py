from openai import OpenAI

client = OpenAI()
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "You are a famous comedian."},
        {"role": "user", "content": "Tell me a joke."},
    ],
)

assert isinstance(completion.choices[0].message.content, str)
