from PyInquirer import prompt
import logging

from stapy.sta.entity import Entity
from stapy.sta.post import Post
from stapy.sta.delete import Delete
from stapy.sta.request import Request
from stapy.sta.patch import Patch
from stapy.sta.abstract_request import AbstractRequest

logger = logging.getLogger("root")

class CLI(object):
    """
    This class contains the interactive TUI build with PyInquirer
    """

    def __init__(self):
        """
        This is the main entry point of the TUI
        """
        self.main()

    def main(self):
        """
        Start the main loop of the TUI and continues as long as the user wants to
        """
        while(True):
            self.select_request()

            question = construct_input_question("confirm", message="Do you want to continue?")
            cont = cprompt(question)
            if not cont:
                break

    def select_request(self):
        """
        Select which type of request should be build and send
        """
        question = construct_choice_question(message="What do you want to do?", choices=Request.list())
        operation = cprompt(question)

        if operation == Request.POST.value:
            entity = cprompt(entity_question)
            self.post_request(Entity.match(entity))
        elif operation == Request.DELETE.value:
            self.delete_request()
        elif operation == Request.PATCH.value:
            entity = cprompt(entity_question)
            self.patch_request(Entity.match(entity))
        elif operation == Request.GET.value:
            self.get_request()

    def delete_request(self):
        """
        Build up and send a DELETE request
        """
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

    def post_request(self, entity):
        """
        Build up and send a POST request
        """
        Post.entity(entity, **self.build_entity(entity))

    def patch_request(self, entity):
        """
        Build up and send a PATCH request
        """
        question = construct_input_question(type="input",
            message="ID of the " + entity.name + " to operate on:")
        entity_id = cprompt(question)

        Patch.entity(entity, entity_id, **self.build_entity(entity))

    def get_request(self):
        """
        This functionality is not implemented yet
        """
        raise NotImplementedError

    def build_entity(self, entity):
        """
        Provided an entity ask the user for each field of this entity which value should be set
        :param entity: the STA entity to operate on
        :return: the resulting dict containing all values that the user entered
        """
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

def construct_choice_question(type="rawlist", name="value", message="", choices=[]):
    """
    Construct the dict of a question that allows for the selection of one out of multiple choices
    """
    return {
        "type": type,
        "name": name,
        "message": message,
        "choices": choices
    }

def construct_input_question(type="input", name="value", message=""):
    """
    Construct the dict of a question that allows for free-text input
    """
    return {
        "type": type,
        "name": name,
        "message": message
    }

entity_question = construct_choice_question(message="Which entity to operate on?", choices=Entity.keys())

def question_block(attributes):
    """
    Construct a list of questions that each as for one attribute of the STA entity
    """
    questions = []
    for attribute in attributes:
        questions.append(construct_input_question(name=attribute, message=cap_first(attribute) + ":"))
    return cprompt(questions, named=True)

def cap_first(string):
    """
    Capitalize the first letter of the provided string and return the result
    """
    if not isinstance(string, str) or len(string) <= 1:
        return ""
    return string[0].upper() + string[1:]

def cprompt(question, named=False):
    """
    Prompt the provided question and exit the TUI in case an error occurred
    """
    try:
        answer = prompt(question)
    except EOFError:
        quit()
    if answer == {}:
        quit()
    return answer if named else answer["value"]
