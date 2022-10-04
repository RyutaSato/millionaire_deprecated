from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/src",
    tags=["src"],
    # :TODO dependencies
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def get():
    return FileResponse("index.html")
    # return HTMLResponse(html)


@router.get("/style.css")
async def get():
    return FileResponse("style.css")


@router.get("/main.js")
async def get():
    return FileResponse("main.js")
