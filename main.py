from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

def normalize(val):
    return str(val).strip().lower()

@app.post("/evaluate-resources")
async def evaluate_resources(resource_file: UploadFile = File(...)):
    content = await resource_file.read()
    resource_df = pd.read_excel(io.BytesIO(content))
    learn_df = pd.read_excel("Azure_Resource_Move_Matrix_v2.xlsx")

    resource_df["norm"] = resource_df["RESOURCE TYPE"].apply(normalize)
    learn_df["norm"] = learn_df["Resource Type"].apply(normalize)

    lookup = dict(zip(learn_df["norm"], learn_df["Subscription"]))

    results = []
    for _, row in resource_df.iterrows():
        results.append({
            "Resource Type": row["RESOURCE TYPE"],
            "Can Be moved": lookup.get(row["norm"], "Unknown")
        })

    return {
        "count": len(results),
        "results": results
    }
