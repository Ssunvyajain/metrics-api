from fastapi import FastAPI, Request, Response, Query
import time
import uuid

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-tws8op.example.com"

@app.middleware("http")
async def cors_and_metrics(request: Request, call_next):
    start = time.time()
    request_id = str(uuid.uuid4())

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(time.time() - start)

    origin = request.headers.get("origin")

    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    return response


@app.get("/stats")
def stats(values: str = Query(...)):
    nums = list(map(int, values.split(",")))

    return {
        "email": "23f2005564@ds.study.iitm.ac.in",
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": round(sum(nums) / len(nums), 2)
    }


@app.options("/stats")
def preflight():
    return Response(status_code=200)
