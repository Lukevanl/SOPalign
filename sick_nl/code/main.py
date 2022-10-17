import os

os.chdir("..")
os.chdir("..")
print(os.getcwd())
    
from evaluation.eval_nli \
    import evaluate_en_nli_models, evaluate_nl_nli_models

def main():
    #sick_en_relatedness_results = evaluate_en_models()
    #sick_nl_relatedness_results = evaluate_nl_models()
    en_nli_results = evaluate_en_nli_models()
    nl_nli_results = evaluate_nl_nli_models()
    #stress_test_results_insick = evaluate_switched_sicks()
    #stress_test_results = evaluate_stress_tests()

main()
