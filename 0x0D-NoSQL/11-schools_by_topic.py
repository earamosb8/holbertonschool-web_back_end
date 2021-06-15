#!/usr/bin/env python3
""" 11. Where can I learn Python? """
import pymongo


def schools_by_topic(mongo_collection, topic: str):
    """ function that returns the list of
	school having a specific topic
    """
    query: dict = {"topics": topic}
    schools: list = []

    for school in mongo_collection.find(query):
        schools.append(school)

    return schools
