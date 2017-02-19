#encoding=utf8
import sys,os
import ctypes


gmax_long = 2 ** 32

def RSHash(s):
    b = 378551
    a = 63689
    hash = 0
    for c in list(s):
        hash = ((hash * a) % gmax_long + ord(c)) % gmax_long
        a = (a * b) % gmax_long
    return hash


def JSHash(s):
    hash = 1315423911
    for c in list(s):
        hash ^= ((hash << 5) % gmax_long + ord(c) + (hash >> 2)) % gmax_long
        hash %= gmax_long
    return hash


def ELFHash(s):
    hash = 0
    x = 0
    for c in list(s):
        hash = ((hash << 4) % gmax_long + ord(c)) % gmax_long
        x = hash & int('0xF0000000', 16)
        if x != 0:
            hash ^= (x >> 24)
        hash &= ~x
    return hash


def SDBMHash(s):
    hash = 0
    for c in list(s):
        hash = (ord(c) + (hash << 6) % gmax_long + (hash << 16) % gmax_long - hash) % gmax_long
    return hash


def BKDRHash(s):
    hash = 0
    seed = 131 
    for c in list(s):
        hash = ((hash * seed) % gmax_long + ord(c)) % gmax_long
    return hash


def DJBHash(s):
    hash = 5381
    for c in list(s):
        hash = (((hash << 5) % gmax_long + hash) % gmax_long + ord(c)) % gmax_long
    return hash


def DEKHash(s):
    s_tmp = list(s)
    hash = len(s_tmp)
    for c in s_tmp:
        hash = (((hash << 5) % gmax_long) ^ (hash >> 27)) % gmax_long
        hash = hash ^ ord(c)
    return hash


def BPHash(s):
    hash = 0
    s_tmp = list(s)
    for c in s_tmp:
        hash = (hash << 7) % gmax_long
        hash = hash ^ ord(c)
    return hash


def FNVHash(s):
    fnv_prime = int('0X811C9DC5', 16)
    hash = 0
    for c in list(s):
        hash = (hash * fnv_prime) % gmax_long
        hash ^= ord(c)
    return hash


def APHash(s):
    hash = int('0XAAAAAAAA', 16)
    tmp_s = list(s)
    for i in xrange(len(tmp_s)):
        c = tmp_s[i]
        if (i & 1) == 0:
            v = ((hash << 7) % gmax_long) ^ ord(c) ^ (hash >> 3)
            hash ^= v
        else:
            k = (hash << 11) % gmax_long
            v = unsigned32( ~( k ^ ord(c) ^ (hash >> 5)))
            hash ^= v
    return hash


def unsigned32(n):
    return n & int('0XFFFFFFFF', 16)


def unsigned32_v2(n):
    ## convert python's negative number to c unsigned long
    return ctypes.c_uint32(n).value 



if __name__ == '__main__':
    s = 'abcdeftg'
    print 'RSHash:',s,'hash:',RSHash(s)
    print 'JSHash:',s,'hash:',JSHash(s)
    print 'ELFHash:',s,'hash:',ELFHash(s)
    print 'BKDRHash:',s,'hash:',BKDRHash(s)
    print 'SDBMHash:',s,'hash:',SDBMHash(s)
    print 'DJBHash:',s,'hash:',DJBHash(s)
    print 'DEKHash:',s,'hash:',DEKHash(s)
    print 'BPHash:',s,'hash:',BPHash(s)
    print 'FNVHash:',s,'hash:',FNVHash(s)
    print 'APHash:',s,'hash:',APHash(s)
    print 'unsigned32(-1):', unsigned32(-1)
    print 'unsigned32_v2(-1):', unsigned32_v2(-1)
    print 'gmax_long', gmax_long
    

