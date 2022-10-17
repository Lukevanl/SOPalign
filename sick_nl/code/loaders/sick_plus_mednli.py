# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:24:44 2022

@author: lukev
"""

from config import sick_plus_mednli_fn_en, sick_plus_mednli_fn_nl_go, sick_plus_mednli_fn_nl_dl

class SICK_PLUS_MEDNLI(object):
    def __init__(self, sick_plus_mednli_fn: str):
        self.sick_plus_mednli_fn = sick_plus_mednli_fn
        self.name = self.sick_plus_mednli_fn.split('/')[-1].split('.')[0]
        self.data = self.load_data()
        self.train_data, self.dev_data, self.test_data = self.split_data()

    def load_data(self):
        with open(self.sick_plus_mednli_fn, 'r', encoding="UTF-8") as in_file:
            lines = [ln.strip().split('\t') for ln in in_file.readlines()][1:]
        sentence_data = [tuple(ln[1:5]+ln[-1:]) for ln in lines]
        sentence_data = [(s1, s2, el, 0.0, split)
                         for (s1, s2, el, rl, split) in sentence_data]
        return sentence_data

    def split_data(self):
        train_data, dev_data, test_data = [], [], []
        for (s1, s2, el, rl, s) in self.data:
            if s == 'TRAIN':
                train_data.append((s1, s2, el, rl))
            if s == 'TRIAL':
                dev_data.append((s1, s2, el, rl))
            if s == 'TEST':
                test_data.append((s1, s2, el, rl))
        return train_data, dev_data, test_data

def load_sick_plus_mednli_en():
    return SICK_PLUS_MEDNLI(sick_plus_mednli_fn_en)

def load_sick_plus_mednli_nl_go():
    return SICK_PLUS_MEDNLI(sick_plus_mednli_fn_nl_go)

def load_sick_plus_mednli_nl_dl():
    return SICK_PLUS_MEDNLI(sick_plus_mednli_fn_nl_dl)