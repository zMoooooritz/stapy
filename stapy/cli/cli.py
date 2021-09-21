from PyInquirer import prompt
import logging

from stapy.sta.entity import Entity
from stapy.sta.post import Post
from stapy.sta.delete import Delete
from stapy.sta.request import Request
from stapy.sta.patch import Patch
from stapy.sta.abstract_request import AbstractRequest

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

def main():
    while(True):
        select_request()

        question = construct_input_question("confirm", message="Do you want to continue?")
        cont = cprompt(question)
        if not cont:
            break

def select_request():
    question = construct_choice_question(message="What do you want to do?", choices=Request.list())
    operation = cprompt(question)

    if operation == Request.POST.value:
        entity = cprompt(entity_question)
        post_request(Entity.match(entity))
    elif operation == Request.DELETE.value:
        delete_request()
    elif operation == Request.PATCH.value:
        entity = cprompt(entity_question)
        patch_request(Entity.match(entity))
    elif operation == Request.GET.value:
        get_request()

def delete_request():
    question = construct_choice_question(message="Delete by IDs or path?", choices=["IDs", "Path"])
    mode = cprompt(question)
    if mode == "IDs":
        entity = cprompt(entity_question)
        question = construct_input_question(message="List of IDs to delete:")
        result = cprompt(question)
        ids = list(filter(lambda x: x.isdigit(), result.split()))
        Delete.entity(Entity.match(entity), ids)
    else:
        question = construct_input_question(message="Path for entities to delete:")
        result = cprompt(question)
        Delete.query(result)

def post_request(entity):
    Post.entity(entity, **build_entity(entity))

def patch_request(entity):
    question = construct_input_question(type="input",
        message="ID of the " + entity.value + " to operate on:")
    entity_id = cprompt(question)

    Patch.entity(entity, entity_id, **build_entity(entity))

def get_request():
    raise NotImplementedError

def build_entity(entity):
    ent = AbstractRequest.get_entity(entity)()
    req_attributes = ent.req_attributes()
    opt_attributes = ent.opt_attributes()

    req_answers = question_block(req_attributes)

    optional = False
    if len(opt_attributes) > 0:
        question = construct_input_question("confirm", message="Do you want to add optional parameters?")
        optional = cprompt(question)

    args = {}
    if optional:
        opt_answers = question_block(opt_attributes)
        for opt in opt_attributes:
            args.update({opt: opt_answers[opt]})

    for req in req_attributes:
        args.update({req: req_answers[req]})

    final_args = {}
    for k, v in args.items():
        if v != "":
            final_args.update({k: v})
    return final_args

def question_block(attributes):
    questions = []
    for attribute in attributes:
        questions.append(construct_input_question(name=attribute, message=cap_first(attribute) + ":")[0])
    return cprompt(questions, named=True)

def cap_first(string):
    if not isinstance(string, str) or len(string) <= 1:
        return ""
    return string[0].upper() + string[1:]

def cprompt(question, named=False):
    answer = prompt(question)
    if answer == {}:
        quit()
    return answer if named else answer["value"]
