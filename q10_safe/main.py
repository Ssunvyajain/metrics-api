from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uuid
import time
from collections import defaultdict, deque

app = FastAPI()

EMAIL = "23f2005564@ds.study.iitm.ac.in"

ALLOWED_ORIGIN = "https://app-nuc1x9.example.com"

RATE_LIMIT = 14
WINDOW = 10

hits = defaultdict(deque)


# ---------------- CORS ----------------
@app.middleware("http")
async def cors(request: Request, call_next):
    response = await call_next(request)

    origin = request.headers.get("origin")

    if origin == "https://app-nuc1x9.example.com":
        response.headers["Access-Control-Allow-Origin"] = origin

    return response


# ---------------- REQUEST CONTEXT ----------------
@app.middleware("http")
async def request_context(request: Request, call_next):
    start = time.time()

    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = req_id

    response = await call_next(request)

    response.headers["X-Request-ID"] = req_id
    response.headers["X-Process-Time"] = str(time.time() - start)

    return response

# ---------------- RATE LIMIT ----------------
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_id = request.headers.get("X-Client-Id", "anon")
    now = time.time()

    q = hits[client_id]

    while q and now - q[0] > WINDOW:
        q.popleft()

    if len(q) >= RATE_LIMIT:
        return JSONResponse({"error": "rate limit exceeded"}, status_code=429)

    q.append(now)

    return await call_next(request)


# ---------------- ENDPOINT ----------------
@app.get("/ping")
def ping(request: Request):
    return {
        "email": EMAIL,
        "request_id": request.state.request_id
    }

