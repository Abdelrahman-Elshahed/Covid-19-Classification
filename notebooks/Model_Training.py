import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import time
from xgboost import XGBClassifier

def fit_classifiers(X_train, y_train, random_state=42):
    classifiers = {
        'Logistic Regression': LogisticRegression(random_state=random_state, solver='liblinear', max_iter=200, class_weight='balanced'),
        'Decision Tree': DecisionTreeClassifier(random_state=random_state, class_weight='balanced'),
        'Random Forest': RandomForestClassifier(random_state=random_state, n_estimators=100, class_weight='balanced'),
        'SVM': SVC(random_state=random_state, probability=True, class_weight='balanced'),
        'KNN': KNeighborsClassifier(),
        'Gradient Boosting': GradientBoostingClassifier(random_state=random_state),
        'XGBoost': XGBClassifier(random_state=random_state, eval_metric='logloss')
    }


    fitted_models = {}
    for name, model in classifiers.items():
        print(f"Training {name}...")
        start = time.time()
        try:
            model.fit(X_train, y_train)
            fitted_models[name] = model
            print(f" Done in {time.time() - start:.2f}s\n")
        except Exception as e:
            print(f" Error training {name}: {e}")

    return fitted_models


def evaluate_classifiers(fitted_models, X_test, y_test):
    results = []
    for name, model in fitted_models.items():
        print(f"\n📊 Evaluating {name}...")
        try:
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

            roc_auc = np.nan
            if hasattr(model, "predict_proba"):
                y_proba = model.predict_proba(X_test)
                if y_proba.shape[1] == 2:
                    roc_auc = roc_auc_score(y_test, y_proba[:, 1])
                else:
                    roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovr')

            print(classification_report(y_test, y_pred, zero_division=0))
            print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

            results.append({
                'Model': name,
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1 Score': f1,
                'ROC AUC': roc_auc
            })
        except Exception as e:
            print(f"⚠️ Evaluation failed for {name}: {e}")

    return pd.DataFrame(results).set_index("Model").sort_values(by="Accuracy", ascending=False)
