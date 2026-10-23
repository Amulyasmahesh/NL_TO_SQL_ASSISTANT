from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
for m in sorted(OpenAI().models.list(), key=lambda m: m.id):
    print(m.id)
