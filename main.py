from fastapi import FastAPI
from database import Base, engine
from business_profile.routes import router as business_info_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(business_info_router)