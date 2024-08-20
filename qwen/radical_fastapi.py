# -*- coding:utf-8 -*-
import os
import time
from typing import Union, List
from typing import Optional
import uvicorn
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from radical_engine import RadicalEngine
from fastapi import File, UploadFile
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='radical server')
    parser.add_argument('-m', '--message', type=int, default=1, required=False, help='output debug message')
    parser.add_argument('-p', '--port', type=int, default=8105, required=False, help='port number')
    parser.add_argument('-w', '--workers', type=int, default=1, required=False, help='worker number')

    return parser.parse_args()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load resources
    global g_radicalEngine
    print('liftspan', 'start...')
    args = parse_args()
    g_radicalEngine = RadicalEngine()
    print('liftspan', 'finish.')
    yield
    # Clean up and release resources
    pass

app = FastAPI(lifespan=lifespan)
      
@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"The parameter is incorrect. {request.method} {request.url}")
    return JSONResponse({"code": "400", "message": exc.errors()})

class RadicalModel(BaseModel):
    text:str

class RadicalRepData(BaseModel):
    radicals:str
    han:str
    pinyin:str
    
class RadicalRepModel(BaseModel):
    code:int = 200
    message:str = "OK"
    data:RadicalRepData
    
@app.post("/radical")
async def getRadical(tokenModel: RadicalModel) ->RadicalRepModel:
    print('{} {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), tokenModel.model_dump()))
    start = time.time()
    respond = g_radicalEngine.getRadical(tokenModel.model_dump())
    end = time.time()

    return respond

if __name__ == "__main__":
    args = parse_args()
    print('radical_fastapi server', 'port = {}, worker = {}.'.format(args.port, args.workers))
    uvicorn.run(app='radical_fastapi:app', host='0.0.0.0', log_level='warning', port=args.port, workers=args.workers, reload=False)
