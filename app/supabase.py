from fastapi import HTTPException
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()  

#Will connect later.
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
BUCKET_NAME = ""


if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise HTTPException(status_code=500, detail="Supabase credentials missing")

supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY) 