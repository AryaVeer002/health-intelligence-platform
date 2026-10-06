import joblib

MODEL_PATH = "ml/models/diabetes_risk_model.joblib"

model = joblib.load(MODEL_PATH)

print()
print("=" * 50)
print("FINAL MODEL STRUCTURE")
print("=" * 50)

print("Model type:")
print(type(model))

print()
print("Number of calibrated classifiers:")
print(len(model.calibrated_classifiers_))

print()
print("First calibrated classifier:")
print(type(model.calibrated_classifiers_[0]))

print()
print("Base estimator:")
print(type(model.calibrated_classifiers_[0].estimator))

print()
print("Pipeline steps:")

pipeline = model.calibrated_classifiers_[0].estimator

for name, step in pipeline.named_steps.items():
    print(f"  {name}: {type(step)}")

print("=" * 50)
