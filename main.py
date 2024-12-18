import argparse
from utils import test_split, get_score, log_answers_to_wandb
from transformers import AutoTokenizer, AutoProcessor, AutoModelForCausalLM, set_seed, GenerationConfig,AutoModelForVision2Seq
from PIL import Image
import requests
from datasets import load_dataset
import re
import json
import gc
import torch
import wandb

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--model_checkpoint", type=str, required=True, help="Path to model checkpoint")
parser.add_argument("--dataset", type=str, required=True, help="Name of the dataset")
parser.add_argument("--subset", type=str, default="MENSA Norway", help="Dataset subset to use")
parser.add_argument("--start", type=int, default=0, help="Start index for the dataset split")
parser.add_argument("--end", type=int, default=100, help="End index for the dataset split")
parser.add_argument("--decoding_strategy", type=str, default="greedy", help="Decoding strategy (greedy, top_p, beam_search)")
parser.add_argument("--top_p", type=float, default=0.9, help="Top-p sampling probability")
parser.add_argument("--num_beams", type=int, default=2, help="Number of beams for beam search")
parser.add_argument("--max_new_tokens", type=int, default=512, help="Maximum number of new tokens to generate")
parser.add_argument("--device", type=str, default="GPU", help="Device to run the model on (GPU/CPU)")

args = parser.parse_args()

# Load dataset and model (pseudo-code, adjust as per your implementation)
dataset = load_dataset(args.dataset)
model = load_model(args.model_checkpoint)

# Define the parameters for test_split
params = {
    "subset": args.subset,
    "start": args.start,
    "end": args.end,
    "decoding_strategy": args.decoding_strategy,
    "top_p": args.top_p,
    "num_beams": args.num_beams,
    "max_new_tokens": args.max_new_tokens,
    "device": args.device,
}

# Run test
answers = test_split(dataset, model, prompts['prompt_2'], processor, **params)
score = get_score(answers, dataset)

# Log and print results
log_answers_to_wandb(answers, score)
print(f"Correct Answers: {score[0]} | Correct Percentage: {score[1]} | IQ: {score[2]}")
