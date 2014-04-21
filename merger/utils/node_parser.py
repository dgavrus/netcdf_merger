import re
import hosts_info 
from hosts_info import Node

class NodeParser:
    
    def __init__(self):
        pass
    
    def parse_nodes(self, filename):
        f = open(filename, 'r')
        nodes = f.readlines()
        nodes = filter(lambda x: str(x).strip(), nodes);
        result = []
        for node in nodes:
            nums = re.findall("\d+", node)
            result.append(Node(nums[0], nums[1], nums[2]))
        f.close()
        return result
    
    @staticmethod
    def parse_node(node_name):
        nums = re.findall("\d+", node_name)
        return Node(nums[0], nums[1], nums[2])