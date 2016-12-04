#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import codecs
import sys
import morfessor
import flatcat

def filetowordlist(path, sfx, output, output_freq): 
    filedict = {}
    allwordlist = []
    fw = codecs.open(output, 'w', encoding = 'utf-8')
    for item in os.listdir(path):
        if sfx in item:
            wordlist = []
            for line in codecs.open(path+item, 'r', encoding = 'utf-8'):
                lines = line.strip().split()
                for word in lines:
                    wd = ''
                    for letter in word:
                        if letter.isalpha():
                            wd = wd+letter 
                        else:
                            wd = wd + ' '
                    w = wd.split()
                    for d in w:
                        wordlist.append(d.lower())
                        allwordlist.append(d.lower())
                        fw.write(d.lower() + '\n')
            filedict[item] = wordlist           
    print 'counting word frequencies ...'
    fw_freq = codecs.open(output_freq, 'w', encoding = 'utf-8')
    for word in set(allwordlist):
        fw_freq.write(str(allwordlist.count(word)) + ' ' + word + '\n')
    return filedict, allwordlist
            
print 'loading and preprocessing data ...'
files, allwordlist = filetowordlist(sys.argv[1], '.txt', 'TempOut.txt', 'Freq.txt')

def Base_SegModel(data):
    io = morfessor.MorfessorIO()
    train_data = list(io.read_corpus_file(data))
    model_types = morfessor.BaselineModel()
    model_types.load_data(train_data, count_modifier = lambda x:1)
    model_types.train_batch()
    model_tokens = morfessor.BaselineModel()
    model_tokens.load_data(train_data)
    model_tokens.train_batch()
    
    return model_types, model_tokens
    
print 'training the baseline ...'
segmentation_types, segmentation_tokens = Base_SegModel('TempOut.txt')

def Base_Segmentation(segmodel, fl, output):
    f = codecs.open(fl, 'r', encoding = 'utf-8')
    fw = codecs.open(output, 'w', encoding = 'utf-8')
    wordlist = []
    for line in f:
        lines = line.strip().split()
        wordlist.append((line[0], lines[1]))
    for count, word in wordlist:
        seg = segmodel.viterbi_segment(word)
        fw.write(count + ' ')
        opt = []
        for i in xrange(len(seg[0])):
            fw.write(seg[0][i])
            if len(seg[0][i:]) > 1:
                fw.write(' ' + '+' + ' ')  
        fw.write('\n')
    return wordlist

a = Base_Segmentation(segmentation_tokens, 'Freq.txt', 'Seg_output.txt')

print 'training the stemming model ...'
def ModelTraining(segmentation_file):
    io = flatcat.FlatcatIO()
    morph_usage = flatcat.categorizationscheme.MorphUsageProperties()
    model = flatcat.FlatcatModel(morph_usage, corpusweight = 1.0)
    model.add_corpus_data(io.read_segmentation_file(segmentation_file))
    model.initialize_hmm()
    return model
    
model = ModelTraining('Seg_output.txt')

print 'stemming ...'
def Segment(files, model, output_path):
    segdict = {}
    for file in files:
        seglist = []
        fw = codecs.open(output_path + file, 'w', encoding = 'utf-8')
        wordlist = files[file]
        for word in wordlist:
            ana = model.viterbi_analyze(word)
            for construct in ana[0]:
                if construct.category == 'STM':
                    fw.write(construct.morph + ' ')
                seglist.append(construct.morph)
        segdict[file] = seglist
    return segdict

sg = Segment(files, model, sys.argv[2])
print 'Finished!'
    




