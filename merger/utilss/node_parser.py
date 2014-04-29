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
    def get_nodes_list(hosts_files_list):
        nodes = []
        for h in hosts_files_list:
            for node in h.nodes:
                if not nodes.__contains__(node.get_node_name()):
                    nodes.append(node.get_node_name())
        nodes.sort(cmp=Node.cmp, key=lambda x : NodeParser.parse_node(x), reverse=False)
        return nodes
    
    @staticmethod
    def parse_node(node_name):
        nums = re.findall("\d+", node_name)
        return Node(nums[0], nums[1], nums[2])
    
    