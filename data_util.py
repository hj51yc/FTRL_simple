import sys
import io
from hash_lib import DJBHash

def get_dict_feature(line, format_toks, DIM = 1000000):
    x = {}
    toks = line.strip().split(',')
    toks_len = len(toks)
    for i in xrange(toks_len):
        x[format_toks[i]] = toks[i]
    ID = x['id']
    del x['id']
    x['hour'] = x['hour'][6:]
    x['ip_1'] = x['device_ip'][0:2]
    x['ip_2'] = x['device_ip'][0:4]
    x['ip_3'] = x['device_ip'][0:6]
    y = 0.0
    if 'click' in x:
        if x['click'] == '1':
            y = 1.
        del x['click']
    
    res_feat = {}
    for k in x:
        s = k + ':' + x[k]
        ind    = abs(DJBHash(s)) % DIM
        res_feat[ind] = 1.0
    return (ID, res_feat, y)


def read_one_line(data_file):
    fp = open(data_file)
    format_line = fp.readline()
    format_toks = format_line.strip().split(',')
    while True:
        line = fp.readline()
        if not line:
            break
        (ID, x, y) = get_dict_feature(line, format_toks)
        yield (ID, x, y)
    fp.close()
