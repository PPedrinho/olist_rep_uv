from sklearn.metrics import confusion_matrix

y_proba = models["LightGBM"].predict_proba(X_test)[:, 1]

y_pred = (y_proba >= 0.13).astype(int)

TN, FP, FN, TP = confusion_matrix(
    y_test,
    y_pred
).ravel()

print(f"TN = {TN}")
print(f"FP = {FP}")
print(f"FN = {FN}")
print(f"TP = {TP}")