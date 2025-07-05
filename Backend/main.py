from fastapi import FastAPI, UploadFile, File, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from rag_backend import build_index, load_index
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INDEX_BASE_DIR = "index_store"

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_path = os.path.join("data", file.filename)
        os.makedirs("data", exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(contents)

        file_id = os.path.splitext(file.filename)[0]
        file_index_dir = os.path.join(INDEX_BASE_DIR, file_id)
        os.makedirs(file_index_dir, exist_ok=True)
        build_index(file_path, file_index_dir)

        return {"message": "PDF uploaded and index built successfully.", "id": file_id}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/summary/{file_id}")
async def get_summary(file_id: str = Path(...)):
    try:
        file_index_dir = os.path.join(INDEX_BASE_DIR, file_id)
        index = load_index(file_index_dir)
        query_engine = index.as_query_engine()
        summary = query_engine.query("Summarize the uploaded document.")
        return {"summary": str(summary)}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat/{file_id}")
async def chat_with_ai(file_id: str, request: ChatRequest):
    try:
        file_index_dir = os.path.join(INDEX_BASE_DIR, file_id)
        index = load_index(file_index_dir)
        query_engine = index.as_query_engine()
        response = query_engine.query(request.query)
        return {"response": str(response)}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
