#encoding=gbk
import sys
import math
import datetime
import random
from data_util import read_one_line

class FTRL:

    def __init__(self, alfa = 0.1, beta = 1.0, numbda1 = 1.0, numbda2 = 1.0):
        self._alfa = alfa
        self._beta = beta
        ## L1's coeff
        self._numbda1 = numbda1
        ## L2's Coeff
        self._numbda2 = numbda2
        self._z = {}
        self._n = {}
        ## parameter
        self._w = {}


    def logistic(self, a):
        return 1.0 / (1 + math.exp(-a))
    
    
    def wtx(self, x):
        s = 0.0
        for i in x:
            if i not in self._w:
                continue
            s += self._w[i] * x[i]
        return s


    def predict(self, x):
        s = self.wtx(x)
        return self.logistic(s)


    def train_one(self, x, y):
        for i in x:
            xi = x[i]
            if i not in self._n:
                self._n[i] = 0
                self._w[i] = 0
                self._z[i] = 0 
            if xi == 0:
                continue
            else:
                if abs(self._z[i]) <= self._numbda1:
                    self._w[i] = 0
                else:
                    sign = -1
                    if self._z[i] >= 0:
                        sign = 1
                    eta = 1.0/ ((self._beta + math.sqrt(self._n[i])) / self._alfa + self._numbda2)
                    self._w[i] = eta * (sign * self._numbda1 - self._z[i])
        p = self.predict(x)
        for i in x:
            gi = (p - y) * x[i]
            ti = (math.sqrt(math.pow(gi, 2) + self._n[i]) - math.sqrt(self._n[i])) / self._alfa
            self._z[i] +=  gi - ti * self._w[i]
            self._n[i] += math.pow(gi, 2)


    def save_model(self, model_file):
        fp = open(model_file, 'w')
        s_alfa = '%s\t%s\n' % ('alfa', str(self._alfa))
        s_beta = '%s\t%s\n' % ('beta', str(self._beta))
        s_numbda1 = '%s\t%s\n' % ('numbda1', str(self._numbda1))
        s_numbda2 = '%s\t%s\n' % ('numbda2', str(self._numbda2))
        s_z = 'z\t' + json.dump(self._z) + '\n'
        s_n = 'n\t' + json.dump(self._n) + '\n'
        s_w = 'w\t' + json.dump(self._w) + '\n'
        fp.write(s_alfa)
        fp.write(s_beta)
        fp.write(s_numbda1)
        fp.write(s_numbda2)
        fp.write(s_z)
        fp.write(s_n)
        fp.write(s_w)
        fp.flush()
        fp.close()

    
    def load_model(self, model_file):
        fp = open(model_file)
        while True:
            line = fp.readline()
            if not line:
                break
            toks = line.strip().split('\t')
            if len(toks) < 2:
                continue
            k = toks[0]
            v = toks[1]
            if k == 'alfa':
                self._alfa = float(v)
            elif k == 'beta':
                self._beta = float(v)
            elif k == 'numbda1':
                self._numbda1 = float(self._numbda1)
            elif k == 'numbda2':
                self._numbda2 = float(self._numbda2)
            elif k == 'z':
                self._z = json.load(v)
            elif k == 'n':
                self._n = json.load(v)
            elif k == 'w':
                self._w = json.load(v)
            
    
    def logloss(self, p, y):
        p = max(min(p, 1. - 10e-15), 10e-15)
        if y == 1:
            return -math.log(p)
        else:
            return -math.log(1-p)



if __name__ == '__main__':
    train_file = u'D:/资料/机器学习/online在线学习/train/train.csv'
    test_file = u'D:/资料/机器学习/online在线学习/test/test.csv'
    #train_file = u'D:/资料/机器学习/online在线学习/test/test.csv'
    submission_file = 'submission_file'
    model_file = 'model_file'
    ftrls = []
    ftrls.append(FTRL(alfa = 0.1, beta=1.0, numbda1=1.0, numbda2=1.0))
    ftrls.append(FTRL(alfa = 0.1, beta=1.0, numbda1=1.0, numbda2=1.0))
    ftrls.append(FTRL(alfa = 0.1, beta=1.0, numbda1=1.0, numbda2=1.0))
    holdout = 0.001
    epoch = len(ftrls)
    start = datetime.datetime.now()
    for e in xrange(epoch):
        counter = 0
        logloss = 0.0
        logloss_count = 0
        print 'start epoch:', e
        ftrl = ftrls[e]
        for (ID, x, y) in read_one_line(train_file):
            r = random.random()
            if r > 0.999:
                p = ftrl.predict(x)
                logloss += ftrl.logloss(p, y)
                logloss_count += 1
            else:
                if random.random() < 0.632:
                    ftrl.train_one(x, y)
            counter += 1
            if counter % 1000000 == 0:
                print 'num:',counter," elapsed time:", str(datetime.datetime.now() - start)
            #    break
        print('Epoch %d finished, validation logloss: %f, elapsed time: %s' % (
        e, logloss/logloss_count, str(datetime.datetime.now() - start)))
    

    
    print 'start to make submission file ...'
    outfile = open(submission_file, 'w')
    outfile.write('id,click\n')
    counter = 0
    for (ID, x, y) in read_one_line(test_file):
        s = 0.0
        for e in xrange(epoch):
            s += ftrls[e].wtx(x)
        s /= epoch
        p = 1.0 / (1 + math.exp(-s))
        #p = ftrl.predict(x)
        outfile.write('%s,%s\n' % (ID, str(p)))
        if counter % 500000 == 0:
            print 'num:', counter
        counter += 1
    outfile.flush()
    outfile.close()
    print 'finished'
