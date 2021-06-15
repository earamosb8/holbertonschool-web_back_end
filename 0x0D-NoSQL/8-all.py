#!/usr/bin/env python3
""" List documents """
import pymongo


def list_all(mongo_collection) -> list:
    """function that lists all documents in a collection"""
    documents: list = []

    for document in mongo_collection.find():
        documents.append(document)

    return documents
