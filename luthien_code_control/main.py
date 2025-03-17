"""
Luthien Code Control (LCC) - A proxy for OpenAI-compatible API endpoints.

This module serves as the main entry point for the LCC application.
"""
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from luthien_code_control import config, control, proxy

app = FastAPI(
    title="Luthien Code Control",
    description="A proxy for OpenAI-compatible API endpoints with security controls",
    version="0.1.0",
)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"status": "ok", "message": "Luthien Code Control is running"}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def api_proxy(request: Request, path: str):
    """
    Proxy endpoint for the OpenAI API.
    
    This endpoint proxies all requests to the OpenAI API and applies security controls.
    """
    # Construct the target URL
    target_url = f"{config.TARGET_URL}/{path}"
    
    try:
        # Get the request body
        request_data = await request.json() if request.method in ["POST", "PUT"] else {}
        
        # Analyze the request
        allowed, reason, modified_data = control.analyze_request(request_data)
        
        # If not allowed, return an error
        if not allowed:
            return JSONResponse(
                content={"error": reason},
                status_code=403,
            )
        
        # Forward the request to the target URL
        response_data = await proxy.proxy_request(request, target_url)
        
        # Analyze the response
        allowed, reason, modified_response = control.analyze_response(response_data)
        
        # If not allowed, return an error
        if not allowed:
            return JSONResponse(
                content={"error": reason},
                status_code=403,
            )
        
        # Return the (possibly modified) response
        return modified_response
    
    except Exception as e:
        # Handle errors
        return JSONResponse(
            content={"error": f"Error proxying request: {str(e)}"},
            status_code=500,
        )


if __name__ == "__main__":
    uvicorn.run("luthien_code_control.main:app", host="0.0.0.0", port=8000, reload=True)