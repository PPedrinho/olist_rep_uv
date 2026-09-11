# Olist

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

br e-commerce public dataset

# Project Organization

```
├── LICENSE
├── Makefile
├── README.md
│
├── data
│   ├── external          <- Data from third party sources
│   ├── interim           <- Intermediate processed datasets
│   ├── processed         <- Final datasets for modeling
│   └── raw               <- Original raw datasets
│
├── docs
│
├── models
│   │
│   ├── best_model.joblib <- Final trained model
│   ├── metadata.json     <- Model information and threshold
│   └── olist_model.pkl   <- Previous model version
│
├── notebooks
│
├── pyproject.toml
│
├── references
│
├── reports
│   └── figures           <- Generated graphics and reports
│
├── requirements.txt
│
├── setup.cfg
│
└── module_olist
    │
    ├── __init__.py
    │
    ├── config.py              <- Project configurations and paths
    │
    ├── dataset.py             <- Data loading and dataset creation
    │
    ├── features.py             <- Feature engineering
    │
    ├── main.py                <- Main machine learning pipeline
    │
    ├── inference.py           <- Model inference execution
    │
    ├── explain.py             <- SHAP model interpretation
    │
    ├── plots.py               <- Visualization functions
    │
    ├── teste.py               <- Auxiliary tests
    │
    └── modeling
        │
        ├── __init__.py
        │
        ├── pipeline.py        <- Machine learning pipelines
        │
        ├── train.py           <- Model training
        │
        ├── split.py           <- Train/test data split
        │
        ├── cross_validation.py <- Cross-validation and model selection
        │
        ├── evaluate.py        <- Model evaluation metrics
        │
        ├── predict.py         <- Model loading and prediction functions
        │
        └── interpret.py       <- SHAP helper functions
```

---

# Project Execution

## 1. Environment setup

Install project dependencies:

```powershell
uv sync
```

Verify Python environment:

```powershell
uv run python --version
```

---

# 2. Model training

The complete training pipeline must be executed through:

```text
module_olist.main
```

Command:

```powershell
uv run python -m module_olist.main
```

The `main.py` executes the complete machine learning workflow:

```
Raw data loading
        ↓
Dataset creation
        ↓
Feature engineering
        ↓
Train/test split
        ↓
Cross Validation
        ↓
Model selection
        ↓
Final training
        ↓
Model persistence
        ↓
Metadata generation
```

After execution, the following files are generated:

```
models/

├── best_model.joblib
└── metadata.json
```

`best_model.joblib` contains the final trained model.

`metadata.json` contains:

- Selected model name;
- Classification threshold.

Example:

```json
{
    "model_name": "LightGBM",
    "threshold": 0.14
}
```

---

# 3. Model inference

After training, predictions can be generated without retraining the model.

Command:

```powershell
uv run python -m module_olist.inference
```

The inference workflow:

```
Input data
      ↓
Load trained model
      ↓
Load threshold
      ↓
Generate probabilities
      ↓
Generate final prediction
```

The output contains:

```
prob_is_late
prediction
```

Where:

- `prob_is_late`: probability of order delay;
- `prediction`: final classification based on the selected threshold.

Example:

```
prob_is_late     prediction

0.08             0
0.21             1
0.04             0
```

Interpretation:

```
0 → Order predicted as on time

1 → Order predicted as delayed
```

---

# 4. Model explainability (SHAP)

The explainability module should be executed after the model training.

Command:

```powershell
uv run python -m module_olist.explain
```

The workflow:

```
Load trained model
        ↓
Prepare data for SHAP
        ↓
Calculate SHAP values
        ↓
Generate interpretation plots
```

The generated files are saved in:

```
reports/figures/
```

Example:

```
reports/

└── figures

    └── shap_summary.png
```

The SHAP analysis allows understanding:

- Most important variables for the model;
- How each feature affects predictions;
- Factors that increase or decrease delay probability.

---

# Recommended Execution Flow

## Step 1 - Train the model

Run:

```powershell
uv run python -m module_olist.main
```

Responsible for:

- Data preparation;
- Feature generation;
- Cross validation;
- Model training;
- Saving trained model.

---

## Step 2 - Run inference

After the model is generated:

```powershell
uv run python -m module_olist.inference
```

Used when:

- New orders need predictions;
- The production scenario needs simulation;
- Retraining is unnecessary.

---

## Step 3 - Generate model explanations

Run:

```powershell
uv run python -m module_olist.explain
```

Used when:

- Understanding model decisions;
- Analyzing feature importance;
- Generating SHAP plots.

---

# Complete Project Flow

```
                 TRAINING

main.py

Raw Data
    ↓
Dataset
    ↓
Features
    ↓
Cross Validation
    ↓
Training
    ↓
best_model.joblib
metadata.json


                 INFERENCE

inference.py

New Data
    ↓
Saved Model
    ↓
Prediction
    ↓
Classification


                 EXPLAINABILITY

explain.py

Saved Model
    ↓
SHAP
    ↓
Feature Interpretation
```

---

# Main Commands

## Train model

```powershell
uv run python -m module_olist.main
```

## Run inference

```powershell
uv run python -m module_olist.inference
```

## Generate SHAP explanation

```powershell
uv run python -m module_olist.explain
```

---

# Notes

- Execute `main.py` whenever there are changes in datasets, features, models, or training parameters.
- Execute `inference.py` when the model is already trained and new predictions are required.
- Execute `explain.py` to analyze model behavior using SHAP.
- The saved model in `models/best_model.joblib` allows predictions without retraining.
- The file `olist_model.pkl` represents an older model version and can be removed if no longer used.