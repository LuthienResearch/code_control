"""
Luthien Code Control (LCC) - A proxy for OpenAI-compatible API endpoints.

This module serves as the main entry point for the LCC application.
"""

from typing import Any, Callable, Dict, Union

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from luthien_code_control import config, control, proxy

app = FastAPI(
    title="Luthien Code Control",
    description="A proxy for OpenAI-compatible API endpoints with security controls",
    version="0.1.0",
)


@app.get("/", response_model=Dict[str, str])
async def root() -> dict[str, str]:
    """Root endpoint for health check."""
    return {"status": "ok", "message": "Luthien Code Control is running"}


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"],
    response_model=Union[JSONResponse, Dict[str, Any]],
)
async def api_proxy(request: Request, path: str) -> Union[JSONResponse, Dict[str, Any]]:
    """
    Proxy endpoint for the OpenAI API.

    This endpoint proxies all requests to the OpenAI API and applies security controls.
    """
    # Construct the target URL
    target_url = f"{config.TARGET_URL}/{path}"
    print(f"Proxying request to: {target_url}")

    try:
        # Get the request body
        request_data = await request.json() if request.method in ["POST", "PUT"] else {}

        print(f"Request path: {path}")
        print(f"Request method: {request.method}")
        print(f"Request data: {request_data}")

        # Analyze the request
        allowed, reason, modified_data = control.analyze_request(request_data)

        # If not allowed, return an error
        if not allowed:
            return JSONResponse(
                content={"error": reason},
                status_code=403,
            )

        # Forward the request to the target URL
        try:
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

        except Exception as proxy_error:
            print(f"Proxy error: {proxy_error}")
            return JSONResponse(
                content={"error": f"Error in proxy: {str(proxy_error)}"},
                status_code=502,
            )

    except Exception as e:
        # Handle errors
        print(f"Request processing error: {e}")
        return JSONResponse(
            content={"error": f"Error processing request: {str(e)}"},
            status_code=500,
        )


if __name__ == "__main__":
    uvicorn.run("luthien_code_control.main:app", host="0.0.0.0", port=8000, reload=True)
