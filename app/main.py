

import subprocess
from fastapi import FastAPI, HTTPException

from app.core.chunking import SplitRequest, split_media

app = FastAPI(title="Video Chunking Service")


import os
import redis


redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
#parallel processing
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


#video merging
@app.post("/split")
def split_video(req: SplitRequest):
    try:
        chunks = split_media(
            file_path=req.file_path,
            chunk_duration=req.chunk_duration
        )
        return {
            "status": "success",
            "chunk_count": len(chunks),
            "chunks": chunks
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail="FFmpeg failed"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
