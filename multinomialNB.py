#The first step is to walk among all directories and file
import os
import pandas as pd
from math import log10

def readEmail(filename):
    """input: name of a the txt file
        output: list of words of the message in the email
    """
    #data = [filename]
    data = []
    try:
        fh = open(filename,'r',encoding = 'latin1')
    except IOError:
        print('cannot open', filename)
    else:
        for line in fh:
            if line !='\n':
                words =  line[:-1].split(' ')
                for word in words:
                    data.append(word)
    finally:
        fh.close()
    return data

def readDirectory(directory, class_name):
    '''Takes the name of the directory and the name of the class
        and creates a subset of data  
    '''
    d = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            d.append([readEmail(os.path.join(root,name)),class_name])
    return d

def extractVocabulary(samples):
    """
    """
    vocabulary = []
    for sample in samples:
        #print (sample)
        for word in sample[0]:
            #print(word)
            if word not in vocabulary:
                vocabulary.append(word)
    return vocabulary

def countDocs(samples):
    return len(samples)

def countDocsInClass(samples,class_name):
    count = 0
    for sample in samples:
        if sample[1] == class_name:
            count += 1
    return count

def concatenateTextOfAllDocsInClass(samples,class_name):
    text_concatenated = []
    for sample in samples:
        if sample[1] == class_name:
            for word in sample[0]:
                text_concatenated.append(word)
    return text_concatenated

def countTokesnOfTerm(text,t):
    tokens = 0
    for word in text:
        if word == t:
            tokens += 1
    return tokens

def countWordsOfDocsInClass(samples,class_name):
    count = 0
    for sample in samples:
        if sample[1] == class_name:
            count = count + len(sample[0])
    return count

def trainMultinomialNB(C, D):
    V = extractVocabulary(D)
    B = len(V)
    N = countDocs(D)
    prior = pd.DataFrame(index = C ,columns = ['value_prior'])
    cond_prob = pd.DataFrame(index = C, columns = V)
    for c in C:
        Nc = countDocsInClass(D,c)
        prior['value_prior'][c] = Nc/N
        text_c = concatenateTextOfAllDocsInClass(D,c)
        num_words_tecxt_c = len(text_c)
        for t in V:
            Tct = countTokesnOfTerm(text_c,t)
            cond_prob [t][c] = (Tct + 1)/(num_words_tecxt_c + B)
    return V,prior,cond_prob


def extractTockensFromDoc(vocabulary,document_message):
    """
    """
    words_in_vocab = []
    for word in document_message:
        if word in vocabulary:
            words_in_vocab.append(word)
    return words_in_vocab

def applyMultinomialNB(C,V,prior,cond_prob,d):
    W = extractTockensFromDoc(V,d)
    score = pd.DataFrame(index = C ,columns = ['value_score'])
    max_score = - 1000000000000.0
    result = -1
    for c in C:
        score['value_score'][c] = log10(prior['value_prior'][c])
        for t in W:
            score['value_score'][c] += log10(cond_prob[t][c])
        temp_score = score['value_score'][c]
        #print(temp_score)
        if temp_score > max_score:
            result = c
            max_score = temp_score
    return result


def accuracy(C,V,prior,cond_prob,dataset_test):
    count_correct = 0
    for sample in dataset_test:
        temp = applyMultinomialNB(C,V,prior,cond_prob,sample[0])
        if temp == sample[1]:
            count_correct += 1
    return float(count_correct)/len(dataset_test)



#print(applyMultinomialNB(C,V,prior,cond_prob,data[200][0]),' and it was',data[200][1])



""" ------------------ Testing dataset_1 -------------------- """        
#the name of the files I want to reare are
train_ham_file = '/home/pili/T2/dataset_1/train/ham'
train_spam_file = '/home/pili/T2/dataset_1/train/spam'
test_ham_file = '/home/pili/T2/dataset_1/test/ham'
test_spam_file = '/home/pili/T2/dataset_1/test/spam'
data_train = readDirectory(train_spam_file,1) + readDirectory(train_ham_file,0) 
C = [0,1]
V,prior,cond_prob = trainMultinomialNB(C, data_train)
data_test = readDirectory(test_spam_file,1) + readDirectory(test_ham_file,0)
print("The accuracy for dataset 1 is: ",accuracy(C,V,prior,cond_prob,data_test))
""" ------------------ Testing dataset_2 -------------------- """        
#the name of the files I want to reare are
train_ham_file = '/home/pili/T2/dataset_2/train/ham'
train_spam_file = '/home/pili/T2/dataset_2/train/spam'
test_ham_file = '/home/pili/T2/dataset_2/test/ham'
test_spam_file = '/home/pili/T2/dataset_2/test/spam'

data_train = readDirectory(train_spam_file,1) + readDirectory(train_ham_file,0) 
C = [0,1]
V,prior,cond_prob = trainMultinomialNB(C, data_train)
data_test = readDirectory(test_spam_file,1) + readDirectory(test_ham_file,0)
print("The accuracy for dataset 2 is: ",accuracy(C,V,prior,cond_prob,data_test))
""" ------------------ Testing dataset_3 -------------------- """        
#the name of the files I want to reare are
train_ham_file = '/home/pili/T2/dataset_3/train/ham'
train_spam_file = '/home/pili/T2/dataset_3/train/spam'
test_ham_file = '/home/pili/T2/dataset_3/test/ham'
test_spam_file = '/home/pili/T2/dataset_3/test/spam'
data_train = readDirectory(train_spam_file,1) + readDirectory(train_ham_file,0) 
C = [0,1]
V,prior,cond_prob = trainMultinomialNB(C, data_train)
data_test = readDirectory(test_spam_file,1) + readDirectory(test_ham_file,0)
print("The accuracy for dataset 3 is: ",accuracy(C,V,prior,cond_prob,data_test))


