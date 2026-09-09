import pandas as pd
import shap
from scipy import sparse

def prepare_data_for_shap(pipeline, X):
    """
    Prepara os dados para o SHAP
    """
    preprocessor = pipeline.named_steps["preprocessor"]
    preprocessor.transform(X)

    X_transformed = preprocessor.transform(X)

    if sparse.issparse(X_transformed):
        X_transformed = X_transformed.toarray()

    feature_names = preprocessor.get_feature_names_out()

    X_transformed = pd.DataFrame(X_transformed, columns=feature_names, index=X.index)

    return X_transformed

def create_explainer(pipeline):

    model = pipeline.named_steps['model']

    #criar um explicador que entenda as previsoes desse modelo

    explainer = shap.TreeExplainer(model)

    return explainer

def calculate_shap_values(explainer, X_transformed):
    """
    Calcula os valores SHAP para o conjunto de dados transformado
    """
    shap_values = explainer.shap_values(X_transformed)
    return shap_values
