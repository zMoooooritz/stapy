from stapy.sta.entity import Entity
from stapy.sta.post import Post

from PyInquirer import prompt
from inspect import signature
import logging

logger = logging.getLogger('root')

def request():
    while(True):
        select_request()

        question = construct_input_question("confirm", message="Do you want to continue?")
        cont = prompt(question)
        if not cont["value"]:
            break

def select_request():
    question = construct_choice_question(message="What do you want to do?", choices=["GET", "POST", "DELETE", "PATCH"])
    operation = prompt(question)

    if operation["value"] in ["POST", "DELETE", "PATCH"]:
        question = construct_choice_question(message="Which entity to operate on?",
            choices=list(map(Entity.remap, Entity)))
        entity = prompt(question)

        if operation["value"] == "DELETE":
            delete_request(entity)
        elif operation["value"] == "POST":
            post_request(entity)
        elif operation["value"] == "PATCH":
            patch_request(entity)
    else:
        get_request()

def delete_request(entity):
    question = construct_input_question(message="List of IDs to delete:")
    result = prompt(question)
    ids = list(filter(lambda x: x.isdigit(), result["value"].split()))
    Post.delete_entity(Entity.match(entity["value"]), ids)

def post_request(entity):
    func = Post.get_entity_method(Entity.match(entity["value"]))
    parameters = list(map(lambda param: param.name, signature(func).parameters.values()))
    questions = []
    for param in parameters:
        questions.append(construct_input_question(name=param, message=param.capitalize() + ":")[0])

    answers = prompt(questions)
    args = []
    for param in parameters:
        args.append(answers[param])

    Post.new_entity(Entity.match(entity["value"]), *args)

def patch_request(entity):
    raise NotImplementedError

def get_request():
    raise NotImplementedError

def construct_choice_question(type="rawlist", name="value", message="", choices=[]):
    return [
        {
            "type": type,
            "name": name,
            "message": message,
            "choices": choices
        }
    ]

def construct_input_question(type="input", name="value", message=""):
    return [
        {
            "type": type,
            "name": name,
            "message": message
        }
    ]
