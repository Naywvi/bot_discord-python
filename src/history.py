import json, os
from src.functions import *

class Node:
    def __init__(self, data):
        self.data = data
        self.next_node = None

    def to_dict(self):
        return {"data": self.data}

class ChainedList:
    def __init__(self, data):
        jsonD = loadJson()
        
        if os.path.exists(jsonD['path']):
            with open(jsonD['path'], 'r') as f:
                data_dict = json.load(f)
            self.size = data_dict['size']
            nodes_list = data_dict['nodes']
            self.first_node = Node(nodes_list[0]['data'])
            current_node = self.first_node
            for i in range(1, self.size):
                new_node = Node(nodes_list[i]['data'])
                current_node.next_node = new_node
                current_node = new_node
            self.last_node = current_node
        else:
            self.first_node = Node(data)
            self.last_node = self.first_node
            self.size = 1
            self.to_json(jsonD['path'])

    def to_dict(self):
        nodes = []
        current_node = self.first_node
        while current_node:
            nodes.append(current_node.to_dict())
            current_node = current_node.next_node
        return {"size": self.size, "nodes": nodes}

    def to_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def insert_first(self, data):
        new_node = Node(data)
        new_node.next_node = self.first_node
        self.first_node = new_node
        self.size += 1

    def append(self, data):
        new_node = Node(data)
        self.last_node.next_node = new_node
        self.last_node = new_node
        self.size += 1