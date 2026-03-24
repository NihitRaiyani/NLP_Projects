import pickle
with open("resume_model.pkl", "rb") as f:
    data = pickle.load(f)
print(type(data))
if isinstance(data, dict):
    print(data.keys())
elif isinstance(data, tuple) or isinstance(data, list):
    for idx, item in enumerate(data):
        print(f"Item {idx}: {type(item)}")
else:
    print(dir(data))
