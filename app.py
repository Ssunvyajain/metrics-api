from fastapi import FastAPI, Request, Response, Query
import time
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import uuid
import time
app = FastAPI()



ALLOWED_ORIGIN = "https://app-nuc1x9.example.com"

@app.middleware("http")
async def cors_and_metrics(request: Request, call_next):
    start = time.time()

    # Reuse incoming X-Request-ID if present, else generate one
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(time.time() - start)

    origin = request.headers.get("origin")

    # Allow both the Q1 origin and the Q10 origin
    if origin in [
        "https://dash-tws8op.example.com",
        "https://app-nuc1x9.example.com",
    ]:
        response.headers["Access-Control-Allow-Origin"] = origin

    return response

@app.get("/stats")

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
from fastapi import Header, HTTPException

API_KEY = "ak_tu44gobz72jnn19gs0t5erv7"


@app.post("/analytics")
def analytics(payload: dict, x_api_key: str = Header(None)):

    # 1. CHECK API KEY
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Wrong API Key")

    events = payload.get("events", [])

    total_events = len(events)
    users = set()
    revenue = 0
    user_totals = {}

    # 2. LOOP THROUGH EVENTS
    for e in events:
        user = e.get("user")
        amount = float(e.get("amount", 0))

        users.add(user)

        # only positive revenue counts
        if amount > 0:
            revenue += amount

            if user in user_totals:
                user_totals[user] += amount
            else:
                user_totals[user] = amount

    # 3. FIND TOP USER
    top_user = None
    if user_totals:
        top_user = max(user_totals, key=user_totals.get)

    # 4. RETURN RESULT
    return {
        "email": "23f2005564@ds.study.iitm.ac.in",
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user
    }

from fastapi import Request, Response
import uuid

from fastapi import Request, Response

@app.get("/ping")
def ping(request: Request, response: Response):
    request_id = request.state.request_id

    response.headers["X-Request-ID"] = request_id

    return {
        "email": "23f2005564@ds.study.iitm.ac.in",
        "request_id": request_id
    }

import time
import json

START_TIME = time.time()
HTTP_COUNTER = 0
LOGS = []

@app.get("/work")
def work(n: int = 1):
    global HTTP_COUNTER

    HTTP_COUNTER += 1

    LOGS.append({
        "level": "INFO",
        "ts": time.time(),
        "path": "/work",
        "request_id": str(uuid.uuid4())
    })

    return {
        "email": "23f2005564@ds.study.iitm.ac.in",
        "done": n
    }

from fastapi.responses import PlainTextResponse

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return (
        "# HELP http_requests_total Total HTTP requests\n"
        "# TYPE http_requests_total counter\n"
        f"http_requests_total {HTTP_COUNTER}\n"
    )

@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "uptime_s": time.time() - START_TIME
    }


@app.get("/logs/tail")
def logs_tail(limit: int = 10):
    return LOGS[-limit:]
