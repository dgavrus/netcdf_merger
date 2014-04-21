from urllib import thishost


class HostsInfo:
    def __init__(self, filename, nodes):
        self.filename = filename
        self.nodes = nodes
           
class Node:
    def __init__(self, type, switch, number):
        self.type = type
        self.switch = switch
        self.number = number
        
    def get_node_name(self):
        return "node" + self.type + "-" + self.switch + "-" + self.number
    
    @staticmethod
    def cmp(node1, node2):
        if int(node1.type) > int(node2.type): return 1
        elif int(node1.type) < int(node2.type): return -1
        elif int(node1.switch) > int(node2.switch): return 1
        elif int(node1.switch) < int(node2.switch): return -1
        elif int(node1.number) > int(node2.number): return 1
        elif int(node1.number) < int(node2.number): return -1
        return 0