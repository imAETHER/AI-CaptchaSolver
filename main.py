from httpx import Client
from fastapi import FastAPI
from typing import Union
from fastapi.responses import JSONResponse
from solver import solveCaptcha

api = FastAPI(title="CaptchaSolver")
checker = Client(headers={
  "User-Agent": "CapSolver v1.0"
})

@api.get("/api/captcha/solve")
@api.get("/api/solve")
def solve_api(captcha: str, color: Union[str, None] = None):
  if (not str(captcha).startswith("https://cdn.discordapp.com")) or (not checker.get(captcha).status_code == 200):
    return JSONResponse({ "success": False, "message": "INVALID_URL" })
  
  if color is None:
    data = solveCaptcha(captcha)
  else:
    data = solveCaptcha(captcha, color=color)

  if data is None or len(data) < 3:
    return JSONResponse({ "success": False, "message": "SOLVE_FAILED" })
  
  return JSONResponse({ "success": True, "solve": data })

if __name__ == "__main__":
  import os
  os.system("uvicorn main:api --host 0.0.0.0 --port 3007")