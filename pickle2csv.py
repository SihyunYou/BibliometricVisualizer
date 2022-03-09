import pickle as pkl
import pandas as pd
with open("3a240541d3627e8160092a24f375eaf9.pkl", "rb") as f:
    object = pkl.load(f)
    
df = pd.DataFrame(object)
df.to_csv(r'3a240541d3627e8160092a24f375eaf9.csv')