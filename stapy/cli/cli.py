from stapy.sta.entity import Entity
from stapy.sta.post import Post
from stapy.sta.delete import Delete
from stapy.sta.request import Request
from stapy.sta.patch import Patch

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
        post_request(Entity.match(entity["value"]))
    elif operation["value"] == Request.DELETE.value:
        delete_request()
    elif operation["value"] == Request.PATCH.value:
        entity = prompt(entity_question)
        patch_request(Entity.match(entity["value"]))
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
    func = Post.get_entity_method(entity)
    parameters = list(map(lambda param: param.name, signature(func).parameters.values()))
    questions = []
    for param in parameters:
        questions.append(construct_input_question(name=param, message=param.capitalize() + ":")[0])

    answers = prompt(questions)
    args = []
    for param in parameters:
        args.append(answers[param])

    Post.entity(entity, *args)

def patch_request(entity):
    ent = Patch.get_entity(entity)()

    question = construct_input_question(type="input",
        message="ID of the " + entity.value + " to operate on:")
    entity_id = prompt(question)["value"]

    req_attributes = ent.req_attributes()
    questions = []
    for req in req_attributes:
        questions.append(construct_input_question(name=req, message=req.capitalize() + ":")[0])

    req_answers = prompt(questions)
    args = {}

    opt_attributes = ent.opt_attributes()
    optional = False
    if len(opt_attributes) > 0:
        question = construct_input_question("confirm", message="Do you want to add optional parameters?")
        optional = prompt(question)["value"]

    if optional:
        questions = []
        for opt in opt_attributes:
            questions.append(construct_input_question(name=opt, message=opt.capitalize() + ":")[0])
        opt_answers = prompt(questions)
        for opt in opt_attributes:
            args.update({opt: opt_answers[opt]})

    for req in req_attributes:
        args.update({req: req_answers[req]})

    final_args = {}
    for k, v in args.items():
        if v != "":
            final_args.update({k: v})
    Patch.entity(entity, entity_id, **final_args)

def get_request():
    raise NotImplementedError
