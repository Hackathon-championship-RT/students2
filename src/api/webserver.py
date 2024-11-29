def run_server() -> None:
    import dotenv
    import uvicorn

    dotenv.load_dotenv()

    uvicorn.run(
        "src.entrypoints.main:api",
        host="0.0.0.0",
        port=8080,
        reload=True,
        lifespan="on",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    run_server()
