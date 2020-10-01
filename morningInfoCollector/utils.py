import re


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def camel_to_snake(s):
    """
    Is it ironic that this function is written in camel case, yet it
    converts to snake case? hmm..
    """
    subbed = re.compile(r"(.)([A-Z][a-z]+)").sub(r"\1_\2", s)
    return re.compile("([a-z0-9])([A-Z])").sub(r"\1_\2", subbed).lower()


def to_snake_dict(dictionary):
    new_dict = {}
    for k, v in dictionary.items():
        snake_key = camel_to_snake(k)

        if isinstance(v, dict):
            new_dict[snake_key] = to_snake_dict(v)
        elif isinstance(v, list):
            new_dict[snake_key] = [to_snake_dict(k) for k in v]
        else:
            new_dict[snake_key] = v
    return new_dict
