import inspect
import os
import sys
from typing import List, Tuple
from fastapi import FastAPI, UploadFile, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud, models_sql, schemas
from database import SessionLocal, engine
import uvicorn
import numpy as np
import time
from strsimpy.cosine import Cosine
import pandas as pd
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import torch
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from models.bert_finetune import BERT_DATASET, BERTFineTuner
from config import (bert, bert_nl, roberta, roberta_nl, mbert)
from loaders.nli_models import load_bert_nli_model
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import RobertaTokenizer, RobertaForSequenceClassification

import fitz

#Based on tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/

models_sql.Base.metadata.create_all(bind=engine)

app = FastAPI()
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())

#Enable CORS (because sending requests from diff src port)
app.add_middleware(
    # eerste 3 regels zijn voor requests toelaten
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    # dit hieronder is als je custom headers wilt terugsturen met response
    expose_headers=["X-Process-Time"],
)

class SOPsent(BaseModel):
    sentences_list: List[str]

class Aanbevelingen(BaseModel):
    aanbevelingen_list: List[Tuple[str, str]]

aanbevelingen = [] #Keeps track of latest entered list of 'aanbevelingen'
sop_sentences = [] #Keeps track of latest sop (sentences) being analysed
results_counts = []
threshold_counts = [0,0,0]
file_object = None
file_object_ann = None

#Load models/tokenizers/database/etc.:
#------------------------------------#
#STS
cosineObject = Cosine(5)
sts_model = SentenceTransformer('paraphrase-xlm-r-multilingual-v1')

#NLI 
import os.path as path
three_up =  path.abspath(path.join(__file__ ,"../../.."))
#model_mednli_roberta_nl_dl = torch.load( three_up + "/model_data/models/model_MEDNLI_NL_dl_robbert-v2-dutch-base.pt")
#model_mednli_roberta_nl_dl = torch.load( three_up + "/model_data/models/model_SICK_NL_robbert-v2-dutch-base.pt")
model_mednli_roberta_nl_dl = torch.load("model_data/models/model_SICK_PLUS_MEDNLI_NL_dl_robbert-v2-dutch-base.pt")


model_mednli_roberta_nl_dl.eval()

#Load tokenizer
tokenizer_robertanl = RobertaTokenizer.from_pretrained(roberta_nl)

#Init Pytorch Trainer object (used for easy+fast predictions)
tuner = BERTFineTuner(roberta_nl, tokenizer_robertanl, model_mednli_roberta_nl_dl, [], [],"", True)

#Function to load database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#------------------------------------#




#HTTP REQUESTS:

@app.post("/feedback", response_model=schemas.Feedback)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return crud.create_feedback(db=db, feedback=feedback)

@app.post("/richtlijn_post", response_model=schemas.Richtlijn)
def create_richtlijn(richtlijn: schemas.RichtlijnCreate, db: Session = Depends(get_db)):
    return crud.create_richtlijn(db=db, richtlijn=richtlijn)

@app.get("/rem_richtlijn/{name}", response_model=list[schemas.Richtlijn])
def remove_richtlijn_by_name(name: str, db: Session = Depends(get_db)):
    richtlijnen = crud.remove_richtlijn_by_name(db, name=name)
    return richtlijnen

@app.get("/richtlijn/", response_model=list[schemas.Richtlijn])
def read_richtlijnen(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db)):
    richtlijnen = crud.get_richtlijnen(db, skip=skip, limit=limit)
    return richtlijnen

@app.get("/richtlijn/{name}", response_model=schemas.Richtlijn)
def read_richtlijn(name: str, db: Session = Depends(get_db)):
    db_richtlijn = crud.get_richtlijn_by_name(db, name=name)
    if db_richtlijn is None:
        raise HTTPException(status_code=404, detail="Richtlijn not found")
    return db_richtlijn

#Save sop contents to global variable
@app.post("/post_sop")
def post_sop(sopSentences: SOPsent):
    global sop_sentences
    sop_sentences = sopSentences.sentences_list

#Save entered aanbevelingen to global variable
@app.post("/post_aanbevelingen")
def post_aanbev(aanbev: Aanbevelingen):
    global aanbevelingen
    aanbevelingen = aanbev.aanbevelingen_list

#Save uploaded file to global variable
@app.post("/post_pdf")
async def post_pdf(file: UploadFile):
    global file_object
    file_object = file
        

#Return entered aanbevelingen
@app.get("/get_aanbevelingen")
def get_aanbev():
    global aanbevelingen
    return {"aanbevelingen": aanbevelingen}

@app.get("/get_ann_pdf")
def get_annot_pdf():
    global file_object_ann
    return file_object_ann

@app.get("/get_and_ann_pdf")
async def get_and_ann_pdf(sop_sentences: List[str] = Query(None), aanbevelingen: List[str] = Query(None), aanbeveling_ids: List[str] = Query(None), labels: List[str] = Query(None), probabilities: List[str] = Query(None)):
    #print(f"sop: {sop_sentences}, aanb: {aanbevelingen}, id: {aanbeveling_ids}, lab: {labels}, prob: {probabilities}")
    #print(f"sop: {type(sop_sentences)}, aanb: {type(aanbevelingen)}, id: {type(aanbeveling_ids)}, lab: {type(labels)}, prob: {type(probabilities)}")
    #pdf = await highlight_pdf([[sop_sentence] for sop_sentence in sop_sentences], 
    #                          [[aanbeveling] for aanbeveling in aanbevelingen], 
    #                          [[aanbeveling_id] for aanbeveling_id in aanbeveling_ids], 
    #                          [[label] for label in labels], 
    #                          probabilities)
    print(len(sop_sentences), len(aanbevelingen), len(aanbeveling_ids), len(labels), len(probabilities))
    pdf = await highlight_pdf(sop_sentences[0].split(','), aanbevelingen[0].split(','), aanbeveling_ids[0].split(','), labels[0].split(','), [float(prob) for prob in probabilities[0].split(',')], rerun=True)
    return pdf

#Main loop, executes STS + NLI steps, returns results and highlights them in PDF.
@app.get("/get_sentence_pairs")
async def get_sentence_pairs(chosen_strictness: str = "Normaal"):
    with open("file.txt","a+", encoding="UTF-8") as f:
        cosine_threshold, sts_threshold = mapStrictnessToThresholds(chosen_strictness)
        start_time = time.time()
        total_count = 0
        sentence_pairs = []
        identifiers = []
        above_cosine_threshold_count = 0
        above_both_threshold_count = 0
        #Loop that calculates STS + Cosine scores and filters out sentences considered irrelevant (below thereshold)
        for sop_sent in sop_sentences:
            nr_connected_to_sop_sent = 0
            connections_to_sop_sent_data = []
            for aanbeveling in aanbevelingen:
                total_count += 1
                score = calculate_cosine_similarity(cosineObject, sop_sent, aanbeveling[0])
                #score = score - ((len(aanbeveling) + len(sop_sent)) / (len(aanbeveling) * len(sop_sent) * 3))
                f.write(f"sop:{sop_sent} aanb: {aanbeveling} \n cos_score = {score}")
                #print(score, end= " | ")
                if(score > cosine_threshold):
                    above_cosine_threshold_count += 1
                    sts_score = get_sts_score(sop_sent, aanbeveling[0], sts_model)
                    f.write(f", sts_score = {sts_score}")
                    #print(sts_score)
                    if(sts_score > sts_threshold):
                        connections_to_sop_sent_data.append([aanbeveling[0], sop_sent, aanbeveling[1], sts_score, score])
                        nr_connected_to_sop_sent += 1
                f.write("\n")
            #Sort connections based on sts score
            connections_to_sop_sent_data.sort(key=lambda x: -x[3])
            #Only keep top three connections
            if (len(connections_to_sop_sent_data) > 3):
                connections_top3 = connections_to_sop_sent_data[:3]
            else:
                connections_top3 = connections_to_sop_sent_data
            for (aanbeveling, sop_sent, id_x, sts_score, score) in connections_top3:
                above_both_threshold_count += 1
                sentence_pairs.append([aanbeveling, sop_sent])
                identifiers.append(id_x)
                print(f"{score} for sentence \n {sop_sent} \n -------compared to------- \n {aanbeveling}\n")
                print(f"STS score: {sts_score}\n\n")
        threshold_counts[0] += total_count 
        threshold_counts[1] += above_cosine_threshold_count
        threshold_counts[2] += above_both_threshold_count
        print(threshold_counts)
        #     Make predictions on the filtered sentence pairs:     #
        #----------------------------------------------------------#
        # Add random evaluation data so we can reuse code from dev set evaluation for predictions
        sop_sents_extr = [i[1] for i in sentence_pairs]
        aanb_extr = [i[0] for i in sentence_pairs]
        sentence_pairs_w_labels = [i + ["NEUTRAL", 0] for i in sentence_pairs]
        global file_object_ann
        results_counts.append(above_both_threshold_count)
        print(results_counts)
        #If NO matching pairs found:
        if(above_both_threshold_count == 0):
            bytes = await file_object.read()
            doc = fitz.open(stream=bytes)
            output_path = "output.pdf"
            doc.save(output_path, garbage=4)
            #Inside FileResponse object so it can be sent back to frontend
            headers = {'Access-Control-Expose-Headers': 'Content-Disposition'}
            pdf = FileResponse(output_path, filename="ann_results.pdf", headers=headers)
            file_object_ann = pdf
            return {"results": [], "sts_counts": [total_count, above_cosine_threshold_count, above_both_threshold_count], "time": (time.time() - start_time) }
        #If matching pairs found:
        print(" -----------------------  GETS HERE 8 --------------------------")
        test_set_sopalign = BERT_DATASET(sentence_pairs_w_labels, tokenizer_robertanl)
        results = tuner.predict(test_set_sopalign).metrics
        predictions = results["test_predictions"]
        probabilities = results["test_probabilities"]
        labels = ["niet conform", "neutraal", "conform"]
        predictions_string = [labels[i] for i in predictions]
        #print_results(sentence_pairs, predictions_string, probabilities, identifiers)
        results_zipped = list(zip(sentence_pairs, identifiers, predictions_string, probabilities))
        #print(list(results_zipped))
        #----------------------------------------------------------#
        print('important')
        print(sop_sents_extr, aanb_extr, identifiers, predictions_string, probabilities)
        pdf = await highlight_pdf(sop_sents_extr, aanb_extr, identifiers, predictions_string, probabilities)
        file_object_ann = pdf
        print(" -----------------------  GETS HERE 10 --------------------------")
    return {"results": results_zipped, "sts_counts": [total_count, above_cosine_threshold_count, above_both_threshold_count], "time": (time.time() - start_time) }

async def highlight_pdf(sop_sentences, aanbevelingen, aanbeveling_ids, labels, probabilities, rerun=False):
    if rerun:
        sop_sentences = [sop_sentence.replace('$#$', ',') for sop_sentence in sop_sentences]
        aanbevelingen = [aanbeveling.replace('$#$', ',') for aanbeveling in aanbevelingen]
    print(" -----------------------  GETS HERE 9 --------------------------")
    bytes = await file_object.read()
    doc = fitz.open(stream=bytes)
    zipped_results = zip(sop_sentences, aanbevelingen, aanbeveling_ids, labels, probabilities)
    results_df = pd.DataFrame(zipped_results,
               columns =['SOP_SENT', 'AANB', 'ID', 'LABEL', 'PROBS'])
    #Group by SOP sents because you only want one note per highlight.
    grouped_df = results_df.groupby('SOP_SENT')
    #Loop over sop sentences with duplicates removed
    for sop_sentence in list(dict.fromkeys(sop_sentences)):
        #print(sop_sentence)
        group_for_sentence = grouped_df.get_group(sop_sentence)
        for page in doc:
            found_matches = page.search_for(sop_sentence)
            aanbevelingen_for_sop = group_for_sentence['AANB'].tolist()
            ids_for_sop = group_for_sentence['ID'].tolist()
            labels_for_sop = group_for_sentence['LABEL'].tolist()
            probabilities_for_sop = group_for_sentence['PROBS'].tolist()
            annot_text = generate_annotation_text(aanbevelingen_for_sop, ids_for_sop, labels_for_sop, probabilities_for_sop, rerun)
            for (i,inst) in enumerate(found_matches):
                text_highlight = page.add_highlight_annot(inst)
                text_highlight.update()
                #If no if, you would get a sticky note for every sentence. Now only on middle line
                if(i == (int(len(found_matches) - 1))):
                    #Place top-left of textbox right next to highlight location (top-right of highlight)
                    tl_coor_of_textbox = inst.top_right
                    text_annotation = page.add_text_annot(tl_coor_of_textbox, annot_text)
                    #Increase rect size
                    #text_annotation.set_popup(text_annotation.popup_rect + (200, -200, 200, -200))
                    text_annotation.update()
    output_path = "output.pdf"
    doc.save(output_path, garbage=4)
    #Inside FileResponse object so it can be sent back to frontend
    headers = {'Access-Control-Expose-Headers': 'Content-Disposition'}
    pdf = FileResponse(output_path, filename="ann_results.pdf", headers=headers)
    return pdf

def generate_annotation_text(aanbevelingen, aanbeveling_ids, labels, probabilities, rerun=False):
    label_to_index = {"niet conform": 0, "neutraal": 1, "conform": 2}
    text_header = f"Aantal gematchte aanbevelingen: {len(set(aanbeveling_ids))}\n\n"
    text_body = f""
    for (index, (aanbeveling, id, label, probability)) in enumerate(zip(aanbevelingen, aanbeveling_ids, labels, probabilities)):
        if (id in aanbeveling_ids[:index]):
            continue
        if (not rerun):
            probability_for_label = probability[label_to_index[label]] * 100
        else:
            probability_for_label = probability * 100
        text_body += f"Koppeling {index+1}: \n{aanbeveling} (ID={id})\nLabel is {label} t.o.v. de sop passage met {probability_for_label:.2f}% kans\n" 
    return text_header + text_body


def print_results(sentence_pairs, pred, prob, id):
    for (i,pair) in enumerate(sentence_pairs):
        print(f"Predicted label: {pred[i]}\nFor aanbeveling: \n{pair[0]} \n with ID: {id[i]} AND sop sentence: \n{pair[1]}\n\n\n")

def mapStrictnessToThresholds(chosenStrictness):
    strictnessToThresholds = {"Extreem Mild": [0.15, 0.575], "Erg Mild": [0.16, 0.600], "Mild": [0.18, 0.64], "Normaal": [0.20, 0.675], "Strikt": [0.215, 0.69], "Erg Strikt": [0.23, 0.71], "Extreem Strikt": [0.24, 0.75]}
    cosine, sts = strictnessToThresholds[chosenStrictness]
    return cosine, sts

def calculate_cosine_similarity(cosineObject, sentence1, sentence2):
    return cosineObject.similarity(sentence1, sentence2)

def get_sts_score(sentence_sop, sentence_aanbeveling, model):
    sop_embedding = model.encode([sentence_sop])[0]
    aanbeveling_embedding = model.encode([sentence_aanbeveling])[0]
    sts_score = cosine(aanbeveling_embedding, sop_embedding)
    return sts_score

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

if __name__ == "__main__":
     uvicorn.run(app, host="127.0.0.1", port=8000)