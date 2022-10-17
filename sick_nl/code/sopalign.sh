#!/bin/bash
#SBATCH --partition=csedu
#SBATCH --gres=gpu:6

python3 main.py

