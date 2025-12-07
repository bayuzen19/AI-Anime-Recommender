from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline.pipeline import AnimeRecommendetionPipeline
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(
    title="Anime Recommendation using Azure Open AI",
    description="API for get recommendation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

pipeline = None

@app.on_event("startup")
async def startup_event():
    global pipeline
    try:
        pipeline = AnimeRecommendetionPipeline()
    except Exception as e:
        print(f'Error initialize Pipeline {str(e)}')

class RecommendationRequest(BaseModel):
    query:str

class RecommendationResponse(BaseModel):
    query:str
    recommendation:str
    status:str = "Success"

@app.get("/")
async def root():
    return {
        "message":"Welcome to API for Recommendation ANIME powered by Azure Open AI",
        "status":"active",
        "docs":"/docs"
    }

@app.post("/recommend",response_model=RecommendationResponse)
async def get_recommendation(request:RecommendationRequest):

    if pipeline is None:
        raise HTTPException(
            status_code=500,
            detail="Pipeline not found or not Initialize"
        )
    
    try:
        recommendation = pipeline.recommender.get_recommendation(request.query)
        return RecommendationResponse(
            query=request.query,
            recommendation=recommendation
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error to get recommendation: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {
        "status":"healthy",
        "pipeline_loaded":pipeline is not None
    }

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000, reload=True)