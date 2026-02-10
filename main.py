from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/process")
async def process_resource(request: Request):
    try:
        data = await request.json()

        resource_type = data.get("resourceType")
        subscription = data.get("subscription")

        if not resource_type:
            return JSONResponse(
                status_code=400,
                content={"error": "resourceType missing"}
            )

        # 🔥 Dummy processing (yahin logic add karega)
        result = {
            "resourceType": resource_type,
            "subscription": subscription,
            "moveSupported": resource_type != "Microsoft.AAD/domainservices"
        }

        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
