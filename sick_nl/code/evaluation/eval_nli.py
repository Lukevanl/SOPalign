import os
import pickle
import torch
from config import (models_folder, results_folder, bert, bert_nl,
                                 roberta, roberta_nl, mbert)
from loaders.sick import load_sick_en, load_sick_nl
from loaders.mednli import load_mednli_en, load_mednli_nl_go, load_mednli_nl_dl
from loaders.sick_plus_mednli import load_sick_plus_mednli_en, load_sick_plus_mednli_nl_go, load_sick_plus_mednli_nl_dl
from loaders.nli_models import load_bert_nli_model

def save_model(out_folder, model, dataset_name, name):
    model_name = name.split('/')[-1]
    out_fn = os.path.join(out_folder, f"model_{dataset_name}_{model_name}.pt")
    torch.save(model, out_fn)


def load_results(fn):
    with open(fn, 'rb') as in_file:
        results = pickle.load(in_file)
    return results


def save_results(out_folder, results, dataset_name, name):
    model_name = name.split('/')[-1]
    out_fn = os.path.join(out_folder, f"results_{dataset_name}_{model_name}.p")
    with open(out_fn, 'wb') as out_file:
        pickle.dump(results, out_file)


def get_epoch(fn):
    return int(fn.split('epoch')[-1].split('.')[0])


def run_finetuner(sick_dataset, name, setting='bert', num_epochs=3,
                  model_folder='models', result_folder='results', evaluating=False):
    tuner = load_bert_nli_model(sick_dataset, name, setting, num_epochs, evaluating)
    eval_results = []
    eval_results = tuner.evaluate()
    save_results(result_folder, eval_results, sick_dataset.name, name)

    print(f"Training for {num_epochs} epochs......")
    tuner.train()
    final_results = tuner.evaluate()
    save_results(result_folder, final_results, sick_dataset.name, name)
    save_model(model_folder, tuner.model, sick_dataset.name, name)
    print(f"Finished running! The test accuracy was {eval_results}!")
    #consolidate_results_and_models(sick_dataset.name, name, model_folder, result_folder)
    #quit()


def evaluate_en_nli_models():
    en_sick = load_sick_en()
    en_mednli = load_mednli_en()
    en_sick_plus_mednli = load_sick_plus_mednli_en()
    # run_finetuner(en_sick, bert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(en_sick, roberta, setting='roberta', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(en_sick, mbert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(en_mednli, bert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(en_mednli, roberta, setting='roberta', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(en_mednli, mbert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    run_finetuner(en_sick_plus_mednli, bert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    run_finetuner(en_sick_plus_mednli, roberta, setting='roberta', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    run_finetuner(en_sick_plus_mednli, mbert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)


def evaluate_nl_nli_models():
    nl_sick = load_sick_nl()
    nl_mednli_go = load_mednli_nl_go()
    nl_mednli_dl = load_mednli_nl_dl()
    nl_sick_plus_mednli_go = load_sick_plus_mednli_nl_go()
    nl_sick_plus_mednli_dl = load_sick_plus_mednli_nl_dl()
    # run_finetuner(nl_sick, bert_nl, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(nl_sick, roberta_nl, setting='roberta', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(nl_sick, mbert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(nl_mednli_go, bert_nl, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(nl_mednli_go, roberta_nl, setting='roberta', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(nl_mednli_go, mbert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(nl_mednli_dl, bert_nl, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(nl_mednli_dl, roberta_nl, setting='roberta', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    # run_finetuner(nl_mednli_dl, mbert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    run_finetuner(nl_sick_plus_mednli_go, bert_nl, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    run_finetuner(nl_sick_plus_mednli_go, roberta_nl, setting='roberta', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    run_finetuner(nl_sick_plus_mednli_go, mbert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    run_finetuner(nl_sick_plus_mednli_dl, bert_nl, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    run_finetuner(nl_sick_plus_mednli_dl, roberta_nl, setting='roberta', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
    run_finetuner(nl_sick_plus_mednli_dl, mbert, setting='bert', num_epochs=20, model_folder=models_folder, result_folder=results_folder)
