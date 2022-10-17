# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 18:15:07 2021

@author: lukev
"""
from deep_translator import GoogleTranslator
from deep_translator import DeepL
#from google_trans_new import google_translator 
#from googletrans import Translator
import os
import numpy as np
import copy
import pickle
import time
import json
from tqdm import tqdm

API_KEY = "unknown"
DIR = "data/medNLI"
DIRECTORY_ABS = os.path.abspath(DIR)
os.chdir(DIRECTORY_ABS)


def clean_data(sentences): 
    #Make into [(sentence1, sentence2, label)] format
    filtered_data = [(i["sentence1"].strip(), i["sentence2"].strip(), i["gold_label"].strip()) for i in sentences]
    #Remove long sentences (>750 characters) to prevent errors during translation
    for i,data in enumerate(filtered_data):
        if (len(data[0]) > 750 or (len(data[1]) > 750)):
            print(f"Removed indice {i} because one of the sentences was too large")
            del filtered_data[i]
    return filtered_data
    

def read_files(filename): #Read json files into list
    sentences = []
    for line in open(filename, 'r'):
        sentences.append(json.loads(line))
    return sentences

def eda(data): #Brief eda on sentence lengths to estimate costs of translation and check for outliers
    lengths = [(len(i[0]), len(i[1])) for i in data]
    lengths_sentence1 = [i[0] for i in lengths]
    lengths_sentence2 = [i[1] for i in lengths]
    lengths_sentence1 = np.array(lengths_sentence1)
    lengths_sentence2 = np.array(lengths_sentence2)
    print(f"Minimum sentence character length: {np.min(lengths_sentence1)} and {np.min(lengths_sentence1)}")
    print(f"Maximum sentence character length: {np.max(lengths_sentence1)} and {np.max(lengths_sentence1)}")
    print(f"Average sentence character length:  {np.average(lengths_sentence1)} and {np.average(lengths_sentence1)}")
        

def translate_sentences(data, translator_type):
    if(translator_type == "go"): #Use GoogleTranslate
        translator = GoogleTranslator(source='en', target ='nl') 
    elif(translator_type == "dl"): #Use DeepL with API-key
        global API_KEY
        if(API_KEY == "unknown"): #If API-key has not been set yet
            print("IMPORTANT: Using this translator to translate the entire dataset is not free!")
            print("If you want to continue, please enter your DeepL Pro API key:")
            API_KEY = input()
        translator = DeepL(api_key=str(API_KEY), source="en", target="nl", use_free_api=False)
    sentences_premise = [i[0] for i in data]
    sentences_hypothesis = [i[1] for i in data]
    premises_nl = []
    hypothesis_nl = []
    for i, premise in enumerate((tqdm(sentences_premise))):
        translated = False
        while(not translated):
            try: #Translate premise and hypothesis
                premises = translator.translate(premise) 
                hypothesis = translator.translate(sentences_hypothesis[i])
                translated = True
                premises_nl.append(premises)
                hypothesis_nl.append(hypothesis)
            except: #Connection lost
                print("\nFailed attempt at translating... trying again")
                time.sleep(2)
    data_nl = list(zip(premises_nl, hypothesis_nl)) #Zip translated premises and hypothesis together
    return data_nl


def translate_file(data, filename, translator):
    print(f"Cleaning data for {filename}...")
    data = clean_data(data) #Make data into format [sentence1, sentence2, label]
    eda(data)
    print("Done cleaning...")
    time1 = time.time()
    if(translator == "dl"):
        chosen_translator = "DeepL translator"
    else:
        chosen_translator = "Google translate"
    print(f"Starting translation of {filename} using the {chosen_translator}...\n")
    translated = translate_sentences(data, translator) #Translated sentence pairs
    labels = [i[2] for i in data] #Keep same label
    translated = list(zip(translated, labels)) #Combine sentences and labels
    if("train" in filename):
       with open('MEDNLI_train_dutch_' + translator + '.pkl', 'wb') as f:
           pickle.dump(translated, f) #Save dutch mednli training data
    if("dev" in filename):
        with open('MEDNLI_dev_dutch_' + translator + '.pkl', 'wb') as f:
            pickle.dump(translated, f) #Save dutch mednli dev data
    if("test" in filename):
        with open('MEDNLI_test_dutch_' + translator + '.pkl', 'wb') as f:
            pickle.dump(translated, f) #Save dutch mednli test data
    print(f"\nFinished translation of {filename}...\n")
    print(f"Time it took: {(time.time())- time1}")
    return translated

def pickle_to_txt_deepl():
    #Training data to txt
    with open('MEDNLI_train_dutch_dl.pkl', 'rb') as f:
        data_train = pickle.load(f)
    with open('MEDNLI_train_dutch_dl.txt', 'w', encoding="utf-8") as f:
        for element in data_train:
            f.write(f"{element[0][0]} \t {element[0][1]} \t {element[1]} \n")
    #Development data to txt
    with open('MEDNLI_dev_dutch_dl.pkl', 'rb') as f:
        data_dev = pickle.load(f)
    with open('MEDNLI_dev_dutch_dl.txt', 'w', encoding="utf-8") as f:
        for element in data_dev:
            f.write(f"{element[0][0]} \t {element[0][1]} \t {element[1]} \n")
    #Test data to txt
    with open('MEDNLI_test_dutch_dl.pkl', 'rb') as f:
        data_test = pickle.load(f)
    with open('MEDNLI_test_dutch_dl.txt', 'w', encoding="utf-8") as f:
        for element in data_test:
            f.write(f"{element[0][0]} \t {element[0][1]} \t {element[1]} \n")

def pickle_to_txt_google():
    #Training data to txt
    with open('MEDNLI_train_dutch_go.pkl', 'rb') as f:
        data_train = pickle.load(f)
    with open('MEDNLI_train_dutch_go.txt', 'w', encoding="utf-8") as f:
        for element in data_train:
            f.write(f"{element[0][0]} \t {element[0][1]} \t {element[1]} \n")
    #Development data to txt
    with open('MEDNLI_dev_dutch_go.pkl', 'rb') as f:
        data_dev = pickle.load(f)
    with open('MEDNLI_dev_dutch_go.txt', 'w', encoding="utf-8") as f:
        for element in data_dev:
            f.write(f"{element[0][0]} \t {element[0][1]} \t {element[1]} \n")
    #Test data to txt
    with open('MEDNLI_test_dutch_go.pkl', 'rb') as f:
        data_test = pickle.load(f)
    with open('MEDNLI_test_dutch_go.txt', 'w', encoding="utf-8") as f:
        for element in data_test:
            f.write(f"{element[0][0]} \t {element[0][1]} \t {element[1]} \n")
            
def read_txts(translator):
    with open('MEDNLI_train_dutch_' + translator + ".txt", 'r', encoding="UTF-8") as f:
        train = [ln.strip().split('\t') for ln in f.readlines()]
    with open('MEDNLI_dev_dutch_' + translator + ".txt", 'r', encoding="UTF-8") as f:
        dev = [ln.strip().split('\t') for ln in f.readlines()]   
    with open('MEDNLI_test_dutch_' + translator + ".txt", 'r', encoding="UTF-8") as f:
        test = [ln.strip().split('\t') for ln in f.readlines()]     
    return train, dev, test
        

def transform_data(train, dev, test):
    train = [sent + ["TRAIN"] for sent in train]
    dev = [sent + ["TRIAL"] for sent in dev]
    test = [sent + ["TEST"] for sent in test]
    merged = train + dev + test
    merged_with_correct_labels = [[s1.replace("\t", " "), s2.replace("\t", ""), label.strip().upper(), 0, ds] for [s1, s2, label, ds] in merged if (len(s1) < 512) and (len(s2) < 512)]
    final_data = merged_with_correct_labels
    return final_data

def transform_to_bert_format_en(train, dev, test): #Change english mednli data to correct format for MEDNLI object 
    cleaned_train = clean_data(train)
    cleaned_dev = clean_data(dev)
    cleaned_test = clean_data(test)
    #Transform tuples to list (so that function call to transform_data can be reused)
    cleaned_train = [list(i) for i in cleaned_train]
    cleaned_dev = [list(i) for i in cleaned_dev]
    cleaned_test = [list(i) for i in cleaned_test]
    transformed_data = transform_data(cleaned_train, cleaned_dev, cleaned_test)
    path = DIRECTORY_ABS.replace("\\medNLI", "") + "/tasks/mednli_nl/MEDNLI.txt"
    with open(path, 'w', encoding="utf-8") as f:
        f.write("pair_ID\tsentence_A\tsentence_B\tentailment_label\trelatedness_score\tSemEval_set\n")
        for index, element in enumerate(transformed_data):
            f.write(f"{index}\t{element[0]}\t{element[1]}\t{element[2]}\t{element[3]}\t{element[4]}\n")
    

def transform_to_bert_format_nl(translator): #Make correct format of translated text for MEDNLI object 
    if(translator == "go"):
        print("Converting google translated sentences to BERT format...")
        train, dev, test = read_txts(translator)
        transformed_data = transform_data(train, dev, test)
    else:
        print("Converting DeepL translated sentences to BERT format...")
        train, dev, test = read_txts(translator) 
        transformed_data = transform_data(train, dev, test)
    path = DIRECTORY_ABS.replace("\\medNLI", "") + f"/tasks/mednli_nl/MEDNLI_nl_{translator}.txt"
    with open(path, 'w', encoding="utf-8") as f:
        f.write("pair_ID\tsentence_A\tsentence_B\tentailment_label\trelatedness_score\tSemEval_set\n")
        for index, element in enumerate(transformed_data):
            f.write(f"{index}\t{element[0]}\t{element[1]}\t{element[2]}\t{element[3]}\t{element[4]}\n")

def main():
    filename_train = "mli_train_v1.jsonl"
    filename_dev = "mli_dev_v1.jsonl"
    filename_test = "mli_test_v1.jsonl"
    
    #Read sentences and labels
    sentences_train = read_files(filename_train)
    sentences_dev = read_files(filename_dev)
    sentences_test = read_files(filename_test)
    #Transform english medNLI to correct format
    transform_to_bert_format_en(sentences_train, sentences_dev, sentences_test)
    #Translate sentences and save files using google translate
    translator = "go"
    translate_file(sentences_train, filename_train, translator)
    translate_file(sentences_dev, filename_dev, translator)
    translate_file(sentences_test, filename_test, translator)
    pickle_to_txt_google()
    transform_to_bert_format_nl(translator)
    
    #Translate sentences and save files using DeepL translator
    translator = "dl"
    translate_file(sentences_train, filename_train, translator)
    translate_file(sentences_dev, filename_dev, translator)
    translate_file(sentences_test, filename_test, translator)
    pickle_to_txt_deepl()
    transform_to_bert_format_nl(translator)

    
if __name__ == "__main__":
    main()
    