from utilss.config import *
from os import listdir
import re
from utilss.node_parser import *
from hosts_info import *
from netCDF4 import Dataset
import numpy
from nntplib import NNTP
from numpy.random import uniform
from platform import node

config = parse_config()
path = config.path + "/"

# get files list without merged file
files = filter(lambda f: f.endswith(".txt") and not f.startswith("merged"), listdir(path))
filename_first_part = re.search("^\D+", files[0]).group()

hosts_files_list = HostsInfo.get_hosts_list(files, NodeParser(), path)
 
i = 0

nodes = NodeParser.get_nodes_list(hosts_files_list)
nodes_len = nodes.__len__()
    
file_matrix_mapping = numpy.zeros((nodes_len, nodes_len))

not_mapped = nodes_len * nodes_len

for hosts in hosts_files_list:
    for i in xrange(hosts.nodes.__len__()):
        for j in xrange(i + 1, hosts.nodes.__len__()):
            if not_mapped <= 0:
                break
            node_i = nodes.index(hosts.nodes[i].get_node_name())
            node_j = nodes.index(hosts.nodes[j].get_node_name())
            if file_matrix_mapping[node_i, node_j] == 0:
                file_matrix_mapping[node_i, node_j] = int(re.search("\d+", hosts.filename).group()) + 1
                file_matrix_mapping[node_j, node_i] = int(re.search("\d+", hosts.filename).group()) + 1
                not_mapped -= 2
        else: continue
        break
    else: continue
    break



matrix = []
merged_hosts_file_list = []
merge = True

result_types = ["average.nc", "deviation.nc", "min.nc", "median.nc"] 

if merge:
    for type in result_types:
        
        files = filter(lambda f: f.endswith(type), listdir(path))
        files.sort(cmp=None, key=lambda x: not x.startswith("merged") and int(re.search("\d+", x).group()), reverse=False)
        merge_cdf = Dataset(path + "merged_" + type, 'w', format="NETCDF3_64BIT")
        x_dim = merge_cdf.createDimension(u'x', size=nodes_len)
        y_dim = merge_cdf.createDimension(u'y', size=nodes_len)
        n_dim = merge_cdf.createDimension(u'n', size=None)
        print len(n_dim)
        merge_cdf.createDimension(u'strings', size=101)
        proc_num = merge_cdf.createVariable(u'proc_num', 'i4')
        test_type = merge_cdf.createVariable(u'test_type', 'i4')
        data_type = merge_cdf.createVariable(u'data_type', 'i4')
        begin_mes_length = merge_cdf.createVariable(u'begin_mes_length', 'i4')
        end_mes_length = merge_cdf.createVariable(u'end_mes_length', 'i4')
        step_length = merge_cdf.createVariable(u'step_length', 'i4')
        noise_mes_length = merge_cdf.createVariable(u'noise_mes_length', 'i4')
        num_noise_mes = merge_cdf.createVariable(u'num_noise_mes', 'i4')
        num_noise_proc = merge_cdf.createVariable(u'num_noise_proc', 'i4')
        num_repeates = merge_cdf.createVariable(u'num_repeates', 'i4')
        data = merge_cdf.createVariable(u'data', 'f8', (u'n', u'x', u'y'))
        print data.shape
        data[:,:,:] = uniform(size=(10, len(x_dim), len(y_dim)))
        zeros = numpy.zeros((10, nodes_len, nodes_len))
        data[:] = zeros
        proc_num[:] = nodes_len
        
        fill_var = False
        
        for i in xrange(nodes_len):
            for j in xrange(i + 1, nodes_len):
                if int(file_matrix_mapping[i, j]) == 0:
                    continue
                filename = filename_first_part + str(int(file_matrix_mapping[i, j]) - 1) + "_" + type
                rootgrp = Dataset(path + filename, 'r', format='NETCDF3_64BIT')
                if not fill_var:
                    fill_var = True
                    print test_type[:]
                    test_type[:] = rootgrp.variables[u'test_type'][:]
                    print test_type[:]
                    print data_type[:]
                    data_type[:] = rootgrp.variables[u'data_type'][:]
                    print data_type[:]
                    begin_mes_length[:] = rootgrp.variables[u'begin_mes_length'][:]
                    end_mes_length[:] = rootgrp.variables[u'end_mes_length'][:]
                    step_length[:] = rootgrp.variables[u'step_length'][:]
                    noise_mes_length[:] = rootgrp.variables[u'noise_mes_length'][:]
                    num_noise_mes[:] = rootgrp.variables[u'num_noise_mes'][:]
                    num_noise_proc[:] = rootgrp.variables[u'num_noise_proc'][:]
                    num_repeates[:] = rootgrp.variables[u'num_repeates'][:]
                h_file = open(path + filename.replace(type, "hosts.txt"))
                names = h_file.readlines();
                names = [x.strip() for x in names]
                print str(i) + " " + str(j)
                file_index_i = names.index(nodes[i])
                file_index_j = names.index(nodes[j])
                for ii in xrange(10):
                    data[ii, i, j] = rootgrp.variables['data'][ii][file_index_i][file_index_j]
                    data[ii, j, i] = rootgrp.variables['data'][ii][file_index_j][file_index_i]
    
                rootgrp.close()
        merge_cdf.close()
    
f = open(path + "merged_hosts.txt", 'w')
for n in nodes:
    f.write(n + '\n')
f.close()

