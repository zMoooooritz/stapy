from stapy.sta.entity import Entity
from stapy.sta.post import Post
from stapy.sta.delete import Delete
from stapy.sta.request import Request

from PyInquirer import prompt
from inspect import signature
import logging

logger = logging.getLogger('root')

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


entity_question = construct_choice_question(message="Which entity to operate on?",
        choices=list(map(Entity.remap, Entity)))

def request():
    while(True):
        select_request()

        question = construct_input_question("confirm", message="Do you want to continue?")
        cont = prompt(question)
        if not cont["value"]:
            break

def select_request():
    question = construct_choice_question(message="What do you want to do?", choices=Request.list())
    operation = prompt(question)

    if operation["value"] == Request.POST.value:
        entity = prompt(entity_question)
        post_request(entity)
    elif operation["value"] == Request.DELETE.value:
        delete_request()
    elif operation["value"] == Request.PATCH.value:
        entity = prompt(entity_question)
        patch_request(entity)
    elif operation["value"] == Request.GET.value:
        get_request()

def delete_request():
    question = construct_choice_question(message="Delete by IDs or path?", choices=["IDs", "Path"])
    mode = prompt(question)
    if mode["value"] == "IDs":
        entity = prompt(entity_question)
        question = construct_input_question(message="List of IDs to delete:")
        result = prompt(question)
        ids = list(filter(lambda x: x.isdigit(), result["value"].split()))
        Delete.entity(Entity.match(entity["value"]), ids)
    else:
        question = construct_input_question(message="Path for entities to delete:")
        result = prompt(question)
        Delete.query(result["value"])

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

    Post.entity(Entity.match(entity["value"]), *args)

def patch_request(entity):
    raise NotImplementedError

def get_request():
    raise NotImplementedError
