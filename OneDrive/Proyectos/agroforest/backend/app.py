# main.py
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import os
import uuid