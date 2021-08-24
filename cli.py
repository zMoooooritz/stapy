#!/usr/bin/env python

from sta.entity import Entity
from sta.post import Post

from PyInquirer import prompt
from inspect import signature
import requests
import logging

logger = logging.getLogger('root')

def request():
    question = construct_choice_question(message="What do you want to do?", choices=["GET", "ADD", "DELETE", "UPDATE"])
    operation = prompt(question)
    
    if operation["value"] in ["ADD", "DELETE", "UPDATE"]:
        question = construct_choice_question(message="Which entity to operate on?", choices=list(map(Entity.remap, Entity.list())))
        entity = prompt(question)

        if operation["value"] == "DELETE":
            # delete the list of given ids of type entity
            question = construct_input_question(message="List of IDs to delete:")
            result = prompt(question)
            ids = list(map(int, filter(lambda x: x.isdigit(), result["value"].split())))
            Post.delete_entity(entity["value"], ids)
        elif operation["value"] == "ADD":
            # add a new entity
            func = Post.get_entity_method(entity["value"])
            parameters = list(map(lambda param: param.name, signature(func).parameters.values()))
            questions = []
            for param in parameters:
                questions.append(construct_input_question(name=param, message=param.capitalize() + ":")[0])

            answers = prompt(questions)
            args = []
            for param in parameters:
                args.append(answers[param])

            Post.new_entity(entity["value"], *args)

        elif operation["value"] == "UPDATE":
            # UPDATE Operation
            raise NotImplementedError
        
    else:
        # GET Operation
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
