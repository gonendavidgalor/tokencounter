from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os

app = FastAPI()

# Initialize tokenizer with error handling
tokenizer = None
try:
    from transformers import AutoTokenizer
    # Try to load the tokenizer, but don't crash if it fails
    tokenizer = AutoTokenizer.from_pretrained("./deepseek_v3_tokenizer", trust_remote_code=True)
    print("✅ Tokenizer loaded successfully")
except Exception as e:
    print(f"❌ Failed to load tokenizer: {e}")
    print("🔄 Will use simple token estimation")

API_KEY = "supersecret123"

@app.post("/tokenize")
async def tokenize_text(request: Request):
    if request.headers.get("x-api-key") != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

    data = await request.json()
    text = data.get("text", "")
    
    if tokenizer:
        # Use actual tokenizer if available
        token_count = len(tokenizer.encode(text))
    else:
        # Fallback to simple estimation
        token_count = max(1, len(text) // 4)
    
    return {"token_count": token_count}

@app.get("/")
async def root():
    return {
        "status": "Tokenizer server is running",
        "tokenizer_loaded": tokenizer is not None
    }

# This is crucial - Render needs this to start the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
