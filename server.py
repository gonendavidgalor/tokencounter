from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import transformers

app = FastAPI()
API_KEY = "supersecret123"

chat_tokenizer_dir = "./deepseek_v3_tokenizer"

tokenizer = transformers.AutoTokenizer.from_pretrained(
    chat_tokenizer_dir,
    trust_remote_code=True
)

@app.post("/tokenize")
async def tokenize_text(request: Request):
    if request.headers.get("x-api-key") != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

    data = await request.json()
    text = data.get("text", "")

    token_ids = tokenizer.encode(text)
    token_count = len(token_ids)

    print(f"[TOKENIZE] IP: {request.client.host}, Tokens: {token_count}")
    print(f"[TOKEN IDS] {token_ids}")
    print(f"[TEXT] {text[:100]}")

    return {"token_count": token_count}

@app.get("/")
async def root():
    return {
        "status": "Tokenizer server is running",
        "tokenizer_loaded": tokenizer is not None
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

