from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from typing import List, Optional

from utils.search_filter_summarize import search_filter_and_summarize
from starlette.responses import RedirectResponse

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    include_domains: List[str] = None
    exclude_domains: List[str] = None

class SearchResponse(BaseModel):
    summary: str
    useful_products: Optional[List[str]]
    used_links: Optional[List[str]]

@app.get("/", response_class=RedirectResponse)
async def root():
    return "/docs"

@app.post("/search-filter-summarize", response_model=SearchResponse)
async def search_filter_and_summarize_endpoint(
    request: SearchRequest
):
    try:
        summary, useful_products, used_links = search_filter_and_summarize(request.query, request.include_domains, request.exclude_domains)

        return {"summary": summary, "useful_products": useful_products, "used_links": used_links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
