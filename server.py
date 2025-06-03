from fastapi import FastAPI, Request, HTTPException
from transformers import AutoTokenizer

app = FastAPI()
tokenizer = AutoTokenizer.from_pretrained("./deepseek_v3_tokenizer", trust_remote_code=True)

API_KEY = "supersecret123"

@app.post("/tokenize")
async def tokenize_text(request: Request):
    if request.headers.get("x-api-key") != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

    data = await request.json()
    text = data.get("text", "")
    tokens = tokenizer.encode(text)
    return {"tokens": tokens}
    
    
@app.get("/")
async def root():
    return {"status": "Tokenizer server is running"}
    
