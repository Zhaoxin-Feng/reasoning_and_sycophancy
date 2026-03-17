#!/bin/bash
# python data.py
# python bad_file.py
# python split_data.py
# python patch.py
# python qwen.py
# chmod +x train_lens.sh

# final_result.tar.gz ~/Desktop/

# tmux new -s train
# tmux attach -t train

export HF_HOME="/workspace/hf_cache"
export TRANSFORMERS_CACHE="/workspace/hf_cache/transformers"
export HF_DATASETS_CACHE="/workspace/hf_cache/datasets"
export WANDB_DIR="/workspace/wandb"

pip install --upgrade pip
pip install --upgrade transformers huggingface_hub[cli] tuned-lens accelerate

export WANDB_API_KEY=""
export WANDB_PROJECT="tuned-lens"

export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1

export CUDA_VISIBLE_DEVICES=0,1

export HF_TOKEN=""


MODEL_NAME="google/gemma-2-9b-it"
OUTPUT_DIR="lens_checkpoints"

echo "Model: $MODEL_NAME"

# --nproc-per-node=2
torchrun --standalone --nnodes=1 --nproc-per-node=2 -m tuned_lens train \
    --model.name $MODEL_NAME \
    --data.name /workspace/redpajama_2023_06_sample \
    --per_gpu_batch_size 2 \
    --output $OUTPUT_DIR \
    --fsdp \
    --wandb "tuned-lens-gemma" \
    --precision bfloat16