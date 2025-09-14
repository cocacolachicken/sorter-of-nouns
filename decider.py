import os

from pydantic import BaseModel
from partition import Partition
from openai import OpenAI
import queryer

cursor = None;

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


def sort_into_partition(client, partition: list[str], obj, reasoning="no") -> CategorizedNoun:
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



class ReturnObj:
    m: str

    def __init__(self):
        return


def decide_on_cat(obj: str, partition: Partition, cache) -> ReturnObj | None: # todo complete function body
    # Lookup in cache
    cat = queryer.find_obj_in_cache(cursor, obj, partition.partition_id)

    if cat is not None:
        print(cat)
        return
    # Call upon chatgpt if cache miss

    client = OpenAI(
        api_key=os.environ.get("OPENAI_SECRET_KEY")
    )

    response = sort_into_partition(client, partition.categories, obj, reasoning="yes")

    # Cache the answer
    cache(response, partition)  # TODO implement a cache function that fits this bill

    return None







