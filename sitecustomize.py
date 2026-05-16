# sitecustomize.py - loaded automatically at Python startup
# Applies nest_asyncio to handle nested event loops (required for Horizon)
import nest_asyncio
try:
    nest_asyncio.apply()
except Exception:
    pass
