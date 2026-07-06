from fastapi import FastAPI, Request, Response
import time, uuid

app = FastAPI()

RATE_LIMIT = {}
WINDOW = 10

EMAIL = "23f2005564@ds.study.iitm.ac.in"


@app.middleware("http")
async def middleware(request: Request, call_next):
    start = time.time()

    # ---------------- request id ----------------
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

    # ---------------- rate limit ----------------
    client_id = request.headers.get("X-Client-Id")

    if client_id:
        now = time.time()

        RATE_LIMIT.setdefault(client_id, [])

        RATE_LIMIT[client_id] = [
            t for t in RATE_LIMIT[client_id]
            if now - t < WINDOW
        ]

        if len(RATE_LIMIT[client_id]) >= 14:
            return Response(status_code=429)

        RATE_LIMIT[client_id].append(now)

    # ---------------- response ----------------
    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(time.time() - start)

    origin = request.headers.get("origin") or ""

    if origin == "https://app-nuc1x9.example.com":
        response.headers["Access-Control-Allow-Origin"] = origin

    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "X-Request-ID, X-Client-Id"

    return response


@app.get("/ping")
def ping(request: Request):
    return {
        "email": EMAIL,
        "request_id": request.state.request_id
    }
