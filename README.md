This repository contains the code and data for our paper "Good Arguments Against the People Pleasers: How Reasoning Mitigates (Yet *Masks*) LLM Sycophancy".

## Repository Structure

```
.
├── data/
│   ├── objective_data.csv      # Objective tasks (MMLU, MATH, AQuA, TruthfulQA)
│   └── subjective_data.csv     # Subjective tasks (DailyDilemmas, Feedback, Social Attitudes)
└── code/
    ├── 1_Decisional_Impact_of_CoT/
    │   ├── objective_task.ipynb     # Inference on objective tasks
    │   ├── subjective_task.ipynb    # Inference on subjective tasks
    │   └── evaluation.ipynb         # Sycophancy rate & accuracy evaluation
    ├── 2_Linguistic_Disparities_in_Reasoning/
    │   └── bias_vs_unbias_linguistic_feature.ipynb  # Linguistic metric analysis
    ├── 3_Dynamics_of_Sycophancy/
    │   ├── first_token_all_examples.ipynb  # Tuned Lens on first output token
    │   └── cot_process.ipynb               # Tuned Lens across reasoning segments
    ├── 4_Dynamics_of_Bias_in_CoT/
    │   ├── typeB_mode.ipynb         # Semantic patterns in CoT-Corrected samples
    │   └── typeAC_mode.ipynb        # Semantic patterns in sycophantic samples
    └── 5_SAE/
        └── sae_cot_segments.ipynb   # SAE feature tracing during reasoning
```

## Data

| File | Samples | Description |
|------|---------|-------------|
| `objective_data.csv` | 3,096 | Questions with ground-truth answers across four benchmarks |
| `subjective_data.csv` | 3,076 | Open-ended questions without definitive answers across three datasets |

## Models

We evaluate six LLMs: Llama-3.1-8B-Instruct, Qwen-2.5-7B-Instruct, Gemma-2-9B-IT, Claude-3.5-Sonnet, GPT-3.5, and o3-mini. Mechanistic analyses (Tuned Lens, SAE) are conducted on the three open-source models.
