#!/usr/bin/env python3
"""
Entry point for the Weather MCP Server
Runs the server with HTTP/SSE transport using FastMCP
"""

import asyncio
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from city_info_http import mcp


async def main():
    """Run the MCP server with FastMCP's built-in SSE transport"""
    print("Starting City Information  Server...")
    print("HTTP/SSE endpoint: http://localhost:8000")
    print("\nConnect with MCP Inspector:")
    print("  npx @modelcontextprotocol/inspector http://localhost:8000")
    print()

    # Get the SSE ASGI app from FastMCP
    app = mcp.sse_app()

    # Add CORS middleware for reliable client connections
    # This is essential for MCP Inspector to establish stable SSE connections
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Configure uvicorn with optimized settings for SSE connections
    config = uvicorn.Config(
        app,
        host="0.0.0.0",  # Bind to all interfaces for reliability
        port=8000,
        log_level="info",
        # Keep-alive settings for stable SSE connections
        timeout_keep_alive=65,
        timeout_notify=30,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
