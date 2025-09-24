if __name__ == '__main__':

    '''

    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("OPENAI_SECRET_KEY")
    )

    response = client.responses.parse(
        model="gpt-5-mini",
        instructions="You are a jolly academic who loves to categorize arbitrary nouns and types into taxonomies. The "
                     "user will give you a comment-separated of categories and an object. You must place the object in "
                     "exactly one of the categories given. Any justification given should be written in a Borgesian "
                     "style.",
        input="Categories: Fire, Water, Earth, Wood, Metal\nObject: Yukio Mishima\nInclude Justification: yes",
        text_format=CategorizedNoun
    )

    print(response.output_parsed)
    
    '''


