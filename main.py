import os
from fastapi import FastAPI, Request, Response, HTTPException

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")


@app.get("/")
def home():
    return {"status": "ok", "service": "Multimedios Ayacucho Bot"}


@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge or "", media_type="text/plain")

    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
@app.get("/debug")
def debug():
    return {
        "verify_token_loaded": bool(VERIFY_TOKEN),
        "verify_token_length": len(VERIFY_TOKEN)
    }
async def receive_webhook(request: Request):
    data = await request.json()
    print("Webhook recibido:", data)
    return {"status": "ok"}
