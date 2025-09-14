from pydantic import BaseModel


class CategorizedNoun(BaseModel):
    category: str
    original_object: str
    reasoning: str


def partition_to_string(partition):
    if len(partition) == 1:
        return partition[0]
    elif len(partition) > 1:
        return partition[0] + ", " + partition_to_string(partition[1:])
    else:
        return ""


def sort_into_partition(client, partition, obj, reasoning="no") -> CategorizedNoun:
    """ Calls openAI to sort obj into categories specified by partition

    :param client: An openAI client
    :param partition: A list of strings denoting the categories wanted
    :param obj: A string denoting the obejct specified
    :param reasoning: include reasoning or no
    :return: output according to CategorizedNoun
    """

    response = client.responses.parse(
        model="gpt-5-mini",
        instructions="You are a jolly academic who loves to categorize arbitrary nouns and types into taxonomies. The "
                     "user will give you a comment-separated of categories and an object. You must place the object in "
                     "exactly one of the categories given. Any justification given should be written in a Borgesian "
                     "style.",
        input=f"Categories: {partition_to_string(partition)}\n"
              f"Object: {obj}\n"
              f"Include Justification: {reasoning}",
        text_format=CategorizedNoun
    )

    return response.output_parsed


if __name__ == "__main__":
    from openai import OpenAI

    print(partition_to_string(["Fire", "Water", "Earth", "Wood", "Metal"]))
    print(["Fire", "Water", "Earth", "Wood", "Metal"])


