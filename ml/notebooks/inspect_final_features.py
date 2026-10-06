import joblib


MODEL_PATH = "ml/models/diabetes_risk_model.joblib"


model = joblib.load(MODEL_PATH)

calibrated_model = model.calibrated_classifiers_[0]

pipeline = calibrated_model.estimator

preprocessor = pipeline.named_steps["preprocessor"]

logistic_model = pipeline.named_steps["model"]


feature_names = preprocessor.get_feature_names_out()

coefficients = logistic_model.coef_[0]


print()
print("=" * 70)
print("FINAL MODEL FEATURES AND COEFFICIENTS")
print("=" * 70)

print(f"Number of transformed features: {len(feature_names)}")

print()

for feature_name, coefficient in zip(
    feature_names,
    coefficients
):
    print(
        f"{feature_name:40} "
        f"{coefficient:+.6f}"
    )

print("=" * 70)