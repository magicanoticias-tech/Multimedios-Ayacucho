import os
from fastapi import FastAPI, Request, Response

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "")


@app.get("/")
def home():
    return {"status": "ok", "service": "Multimedios Ayacucho Bot"}


@app.get("/webhook")
def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None,
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return Response(content=hub_challenge or "", media_type="text/plain")

    return Response(content="Verification failed", status_code=403)


@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()

    # Por ahora confirmamos la recepción.
    # En el próximo paso procesaremos mensajes, fotos y comandos.
    print("WhatsApp webhook:", data)

    return {"status": "ok"}
