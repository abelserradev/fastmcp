import uvicorn
from app.utils.LoggerSingleton import logger


def main():
    uvicorn.run("app.api.app:app", host="0.0.0.0", port=9000, reload=True, workers=4)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server stopped")

