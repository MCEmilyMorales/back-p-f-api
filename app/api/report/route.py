from fastapi import FastAPI, HTTPException
from app.api.database import db
from app.api.report import crud