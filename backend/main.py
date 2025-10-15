from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# your library
from demojify_lib import emoji_semantic_clean, demojify

# --- LLM Config ---
BASE_URL = "https://fast-api.snova.ai/v1"
MODEL = "DeepSeek-V3.1"
sambanova_key = "3f792f08-b267-4123-916a-58d780ca98bd"

# Initialize the OpenAI-compatible client directly
try:
    from openai import OpenAI
    OpenAIClient = OpenAI(base_url=BASE_URL, api_key=sambanova_key)
    print("[INFO] OpenAI client initialized successfully.")
except Exception as e:
    OpenAIClient = None
    print("[ERROR] Failed to initialize OpenAI client:", repr(e))

# --- FastAPI app setup ---
app = FastAPI(title="Demojifier API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # You can restrict this for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---
class ConvertIn(BaseModel):
    text: str
    mode: str = "auto"  # "auto" or "standard"

class ConvertOut(BaseModel):
    output: str
    source: str
    reason: str

# --- Routes ---
@app.post("/api/convert", response_model=ConvertOut)
def convert(payload: ConvertIn):
    text = (payload.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")

    # If user forces standard, or client failed to init
    if payload.mode == "standard" or OpenAIClient is None:
        output = emoji_semantic_clean(text)
        return ConvertOut(output=output, source="standard", reason="rules_only")

    # Otherwise run full pipeline
    result = demojify(text, client=OpenAIClient, model=MODEL)
    return ConvertOut(output=result.final_text, source=result.source, reason=result.reason)

@app.get("/health")
def health():
    return {"ok": True, "llm_client": OpenAIClient is not None, "model": MODEL}
