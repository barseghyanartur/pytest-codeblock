# Customisation

Customisation examples.

## External references

- [openai](https://github.com/openai/openai-python)
- [moto](https://docs.getmoto.org)
- [fake.py](https://github.com/barseghyanartur/fake.py)

## `fake.py` example

<!-- pytestmark: fakepy -->
```python name=test_create_pdf_file
from fake import FAKER

FAKER.pdf_file()
```

## `moto` example

<!-- pytestmark: aws -->
```python name=test_create_bucket
import boto3

s3 = boto3.client("s3", region_name="us-east-1")
s3.create_bucket(Bucket="my-bucket")
assert "my-bucket" in [b["Name"] for b in s3.list_buckets()["Buckets"]]
```

## `openai` example

<!-- pytestmark: openai -->
```python name=test_tell_me_a_joke
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
```
