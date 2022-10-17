import os

bert = "bert-base-cased"
bert_nl = "GroNLP/bert-base-dutch-cased"
roberta = "roberta-base"
roberta_nl = "pdelobelle/robbert-v2-dutch-base"
mbert = "bert-base-multilingual-cased"

data_folder = 'sick_nl/data'
stress_test_folder = os.path.join(data_folder, 'tasks/stress_tests')
sick_folder = os.path.join(data_folder, 'tasks/sick_nl')
mednli_folder = os.path.join(data_folder, 'tasks/mednli_nl')
sick_plus_mednli_folder = os.path.join(data_folder, 'tasks/sick_plus_mednli_nl')
vectors_folder = os.path.join(data_folder, 'vectors')

sick_fn_en = os.path.join(sick_folder, 'SICK.txt')
sick_fn_nl = os.path.join(sick_folder, 'SICK_NL.txt')

mednli_fn_en = os.path.join(mednli_folder, 'MEDNLI.txt')
mednli_fn_nl_go = os.path.join(mednli_folder, 'MEDNLI_NL_go.txt')
mednli_fn_nl_dl = os.path.join(mednli_folder, 'MEDNLI_NL_dl.txt')

sick_plus_mednli_fn_en = os.path.join(sick_plus_mednli_folder, 'SICK_PLUS_MEDNLI.txt')
sick_plus_mednli_fn_nl_go = os.path.join(sick_plus_mednli_folder, 'SICK_PLUS_MEDNLI_NL_go.txt')
sick_plus_mednli_fn_nl_dl = os.path.join(sick_plus_mednli_folder, 'SICK_PLUS_MEDNLI_NL_dl.txt')

skipgram_fn = os.path.join(vectors_folder, 'GoogleNews-vectors-negative300_SICK.txt')
skipgram_fn_nl = os.path.join(vectors_folder, '320/wikipedia-320.txt')

model_data_folder = 'sick_nl/model_data'
models_folder = os.path.join(model_data_folder, 'models')

results_folder = os.path.join(model_data_folder, 'results')

prep_order_fn = os.path.join(stress_test_folder, 'prep_phrase_order.txt')
present_tense_fn = os.path.join(stress_test_folder, 'present_cont_present_simple.txt')
