from fastapi import FastAPI


app = FastAPI()


@app.get("/test")
async def _():
    return {"message": "Hello World"}
