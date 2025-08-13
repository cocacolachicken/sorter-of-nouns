import os

if __name__ == '__main__':

    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("OPENAI_SECRET_KEY")
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input="My name is pink and i'm really glad to meet you"
    )

    print(response)

