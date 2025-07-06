"""
Run script for the application.

This script provides a convenient way to run the application.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
