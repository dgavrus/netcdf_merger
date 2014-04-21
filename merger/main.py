from utils.config import *
from os import listdir
import re
from utils.node_parser import *
from hosts_info import *
from netCDF4 import Dataset
import numpy
from nntplib import NNTP
from numpy.random import uniform

config = parse_config()
path = config.path + "/"

files = filter(lambda f: f.endswith(".txt") and not f.startswith("merged"), listdir(path))
test_numbers = []
i = 0
for f in files:
    match = re.search("\d+", f)
    test_numbers.append(int(re.search("\d+", f).group()))
    i += 1
test_numbers = sorted(test_numbers, key = lambda x: int(x))
parser = NodeParser()
hosts = []
i = 0
for f in files:
    hosts.append(HostsInfo(f, parser.parse_nodes(path + f)))

for h in hosts:
    print h.filename
    print [node.get_node_name() for node in h.nodes]
    

nodes = []

for h in hosts:
    for node in h.nodes:
        if not nodes.__contains__(node.get_node_name()):
            nodes.append(node.get_node_name())

    
nodes_len = nodes.__len__()

nodes.sort(cmp=Node.cmp, key=lambda x : NodeParser.parse_node(x), reverse=False)
    
matrix = []
merged_hosts_file_list = []
merge = True

if merge:
    files = filter(lambda f: f.endswith("average.nc"), listdir(path))
    files.sort(cmp=None, key=lambda x: not x.startswith("merged") and int(re.search("\d+", x).group()), reverse=False)
    merge_cdf = Dataset(path + "merged_average.nc", 'w', format="NETCDF3_64BIT")
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
    
    for f in files:
            
        h_file = open(path + f.replace("average.nc", "hosts.txt"))
        names = h_file.readlines();
        names = [x.strip() for x in names]
        rootgrp = Dataset(path + f, 'r', format='NETCDF3_64BIT')
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
        for nn in names:
            for nnn in names[names.index(nn) + 1:]:
                for ii in xrange(10):
                    inn = names.index(nn)
                    innn = names.index(nnn)
                    if(inn == innn): exit()
                    val_ij = rootgrp.variables['data'][ii][inn][innn]
                    val_ji = rootgrp.variables['data'][ii][innn][inn]
                    if(str(val_ij).startswith("0.0")): print nn + " " + nnn
                    if(str(val_ji).startswith("0.0")): print nnn + " " + nn
                    inn = nodes.index(nn)
                    innn = nodes.index(nnn)
                    if(inn == innn): exit()
                    data[ii, inn, innn] = val_ij
                    data[ii, innn, inn] = val_ji

        rootgrp.close()
        
    
    nc = Dataset('unl_dim.nc', 'w', format='NETCDF3_64BIT')
    dim = nc.createDimension(u'n')
    nc.dimensions['n'] = 10
    rootgrp.dimensions['n'] = dim 
    nc.close()    
    merge_cdf.close()
    
f = open(path + "merged_hosts.txt", 'w')
for n in nodes:
    f.write(n + '\n')
f.close()
merge_cdf = Dataset(path + "merged_average.nc", 'r', format="NETCDF3_64BIT")
print merge_cdf.variables['data']
test119 = Dataset(path + "test119_average.nc", 'r', format="NETCDF3_64BIT")
print test119.variables['data']

print len(merge_cdf.variables.values())
l = len(test119.variables.values())

for i in xrange(l):
    print merge_cdf.variables.values()[i], test119.variables.values()[i]
    print merge_cdf.variables.values()[i][:], test119.variables.values()[i][:]

