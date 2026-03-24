import pickle
with open("resume_model.pkl", "rb") as f:
    data = pickle.load(f)
model = data['model']
print(model.classes_)
