import uvicorn

from app.utils.LoggerSingleton import logger
from app.utils.configs import ENV

def main():
    if ENV in ["production", "staging"]:
        uvicorn.run("app.api.app:app", host="0.0.0.0", port=9000, reload=False, workers=4)
    else:
        uvicorn.run("app.api.app:app", host="0.0.0.0", port=9000, reload=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server stopped")
