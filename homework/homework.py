# flake8: noqa: E501
#
# En este dataset se desea pronosticar el default (pago) del cliente el próximo
# mes a partir de 23 variables explicativas.
#
#   LIMIT_BAL: Monto del credito otorgado. Incluye el credito individual y el
#              credito familiar (suplementario).
#         SEX: Genero (1=male; 2=female).
#   EDUCATION: Educacion (0=N/A; 1=graduate school; 2=university; 3=high school; 4=others).
#    MARRIAGE: Estado civil (0=N/A; 1=married; 2=single; 3=others).
#         AGE: Edad (years).
#       PAY_0: Historia de pagos pasados. Estado del pago en septiembre, 2005.
#       PAY_2: Historia de pagos pasados. Estado del pago en agosto, 2005.
#       PAY_3: Historia de pagos pasados. Estado del pago en julio, 2005.
#       PAY_4: Historia de pagos pasados. Estado del pago en junio, 2005.
#       PAY_5: Historia de pagos pasados. Estado del pago en mayo, 2005.
#       PAY_6: Historia de pagos pasados. Estado del pago en abril, 2005.
#   BILL_AMT1: Historia de pagos pasados. Monto a pagar en septiembre, 2005.
#   BILL_AMT2: Historia de pagos pasados. Monto a pagar en agosto, 2005.
#   BILL_AMT3: Historia de pagos pasados. Monto a pagar en julio, 2005.
#   BILL_AMT4: Historia de pagos pasados. Monto a pagar en junio, 2005.
#   BILL_AMT5: Historia de pagos pasados. Monto a pagar en mayo, 2005.
#   BILL_AMT6: Historia de pagos pasados. Monto a pagar en abril, 2005.
#    PAY_AMT1: Historia de pagos pasados. Monto pagado en septiembre, 2005.
#    PAY_AMT2: Historia de pagos pasados. Monto pagado en agosto, 2005.
#    PAY_AMT3: Historia de pagos pasados. Monto pagado en julio, 2005.
#    PAY_AMT4: Historia de pagos pasados. Monto pagado en junio, 2005.
#    PAY_AMT5: Historia de pagos pasados. Monto pagado en mayo, 2005.
#    PAY_AMT6: Historia de pagos pasados. Monto pagado en abril, 2005.
#
# La variable "default payment next month" corresponde a la variable objetivo.
#
# El dataset ya se encuentra dividido en conjuntos de entrenamiento y prueba
# en la carpeta "files/input/".
#
# Los pasos que debe seguir para la construcción de un modelo de
# clasificación están descritos a continuación.
#
#
# Paso 1.
# Realice la limpieza de los datasets:
# - Renombre la columna "default payment next month" a "default".
# - Remueva la columna "ID".
# - Elimine los registros con informacion no disponible.
# - Para la columna EDUCATION, valores > 4 indican niveles superiores
#   de educación, agrupe estos valores en la categoría "others".
#
# Renombre la columna "default payment next month" a "default"
# y remueva la columna "ID".
#
#
# Paso 2.
# Divida los datasets en x_train, y_train, x_test, y_test.
#
#
# Paso 3.
# Cree un pipeline para el modelo de clasificación. Este pipeline debe
# contener las siguientes capas:
# - Transforma las variables categoricas usando el método
#   one-hot-encoding.
# - Escala las demas variables al intervalo [0, 1].
# - Selecciona las K mejores caracteristicas.
# - Ajusta un modelo de regresion logistica.
#
#
# Paso 4.
# Optimice los hiperparametros del pipeline usando validación cruzada.
# Use 10 splits para la validación cruzada. Use la función de precision
# balanceada para medir la precisión del modelo.
#
#
# Paso 5.
# Guarde el modelo (comprimido con gzip) como "files/models/model.pkl.gz".
# Recuerde que es posible guardar el modelo comprimido usanzo la libreria gzip.
#
#
# Paso 6.
# Calcule las metricas de precision, precision balanceada, recall,
# y f1-score para los conjuntos de entrenamiento y prueba.
# Guardelas en el archivo files/output/metrics.json. Cada fila
# del archivo es un diccionario con las metricas de un modelo.
# Este diccionario tiene un campo para indicar si es el conjunto
# de entrenamiento o prueba. Por ejemplo:
#
# {'type': 'metrics', 'dataset': 'train', 'precision': 0.8, 'balanced_accuracy': 0.7, 'recall': 0.9, 'f1_score': 0.85}
# {'type': 'metrics', 'dataset': 'test', 'precision': 0.7, 'balanced_accuracy': 0.6, 'recall': 0.8, 'f1_score': 0.75}
#
#
# Paso 7.
# Calcule las matrices de confusion para los conjuntos de entrenamiento y
# prueba. Guardelas en el archivo files/output/metrics.json. Cada fila
# del archivo es un diccionario con las metricas de un modelo.
# de entrenamiento o prueba. Por ejemplo:
#
# {'type': 'cm_matrix', 'dataset': 'train', 'true_0': {"predicted_0": 15562, "predicte_1": 666}, 'true_1': {"predicted_0": 3333, "predicted_1": 1444}}
# {'type': 'cm_matrix', 'dataset': 'test', 'true_0': {"predicted_0": 15562, "predicte_1": 650}, 'true_1': {"predicted_0": 2490, "predicted_1": 1420}}
#
def pregunta01():
    import pickle
    import gzip
    import json
    import os

    import pandas as pd
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
    from sklearn.feature_selection import SelectKBest, f_classif
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import (
        precision_score,
        recall_score,
        f1_score,
        balanced_accuracy_score,
        confusion_matrix,
    )

    # Cargar datos
    with open("files/grading/x_train.pkl", "rb") as f:
        x_train = pickle.load(f)
    with open("files/grading/y_train.pkl", "rb") as f:
        y_train = pickle.load(f)
    with open("files/grading/x_test.pkl", "rb") as f:
        x_test = pickle.load(f)
    with open("files/grading/y_test.pkl", "rb") as f:
        y_test = pickle.load(f)

    # Columnas categóricas y numéricas
    categorical = ["SEX", "EDUCATION", "MARRIAGE"]
    numerical = [col for col in x_train.columns if col not in categorical]

    # Preprocesador
    preprocessor = ColumnTransformer(transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", MinMaxScaler(), numerical),
    ])

    # Pipeline
    pipeline = Pipeline([
        ("pre", preprocessor),
        ("select", SelectKBest(score_func=f_classif)),
        ("clf", LogisticRegression(max_iter=500, class_weight="balanced", solver="liblinear")),
    ])

    # Búsqueda de hiperparámetros
    param_grid = {
        "select__k": [15, 20, 'all'],
        "clf__C": [0.01, 0.1, 1.0, 10.0, 100.0],
    }

    model = GridSearchCV(
        pipeline,
        param_grid=param_grid,
        scoring="balanced_accuracy",
        cv=10,
        n_jobs=-1,
    )

    model.fit(x_train, y_train)

    # Guardar modelo entrenado
    os.makedirs("files/models", exist_ok=True)
    with gzip.open("files/models/model.pkl.gz", "wb") as f:
        pickle.dump(model, f)

    # Función de métricas con threshold ajustado
    def compute_metrics(x, y, name):
        y_proba = model.predict_proba(x)[:, 1]
        y_pred = (y_proba >= 0.68).astype(int)
        cm = confusion_matrix(y, y_pred)
        return [
            {
                "type": "metrics",
                "dataset": name,
                "precision": precision_score(y, y_pred),
                "balanced_accuracy": balanced_accuracy_score(y, y_pred),
                "recall": recall_score(y, y_pred),
                "f1_score": f1_score(y, y_pred),
            },
            {
                "type": "cm_matrix",
                "dataset": name,
                "true_0": {
                    "predicted_0": int(cm[0][0]),
                    "predicted_1": int(cm[0][1]),
                },
                "true_1": {
                    "predicted_0": int(cm[1][0]),
                    "predicted_1": int(cm[1][1]),
                },
            },
        ]

    # Evaluar métricas y guardar en orden correcto
    train_metrics, train_cm = compute_metrics(x_train, y_train, "train")
    test_metrics, test_cm = compute_metrics(x_test, y_test, "test")
    results = [train_metrics, test_metrics, train_cm, test_cm]

    # Guardar métricas
    os.makedirs("files/output", exist_ok=True)
    with open("files/output/metrics.json", "w", encoding="utf-8") as f:
        for entry in results:
            json.dump(entry, f)
            f.write("\n")

pregunta01()