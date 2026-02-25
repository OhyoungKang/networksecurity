# NETWORKSECURITY/app.py

import sys
import os
import certifi
import psutil

ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")
# print(mongo_db_url)

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, status
from uvicorn import run as app_run
from fastapi.responses import Response, JSONResponse
from contextlib import asynccontextmanager
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.network_model = NetworkModel(
            preprocessor=load_object("final_model/preprocessing.pkl"),
            model=load_object("final_model/model.pkl")
        )
        app.state.model_loaded = True
    except:
        app.state.model_loaded = False

    yield
app = FastAPI(lifespan=lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/live")
def live():
    return {"status": "alive"}

@app.get("/health/ready")
def ready():
    try:
        client.admin.command("ping")
        return {"status": "ready", "mongodb": "connected"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "mongodb": "down"}
        )

@app.get("/health/startup")
def startup():
    try:
        return {"model_loaded": getattr(app.state, "model_loaded", False)}
    except:
        return {"model": "missing"}

@app.get("/health/system")
def system():
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        logging.info(f"Predicting {file.filename}")

        try:
            df = pd.read_csv(file.file)
        except Exception:
            raise ValueError("Invalid CSV file")

        logging.info(f"Input shape: {df.shape}")

        network_model = getattr(request.app.state, "network_model", None)

        if network_model is None:
            raise RuntimeError("Model not loaded")

        if not df.empty:
            logging.info(f"Input sample: {df.iloc[0].to_dict()}")

        y_pred = network_model.predict(df)

        logging.info(f"Prediction done: {len(y_pred)} rows")

        df['predicted_column'] = y_pred
        logging.info(f"Prediction completed. Rows={len(df)}")

        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv('prediction_output/output.csv')

        table_html = df.to_html(classes='table table-striped')

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        logging.exception(f"Prediction failed")
        raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)