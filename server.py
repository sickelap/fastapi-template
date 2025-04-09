import os
import subprocess
import sys

import uvicorn


def development():
    uvicorn.run("app.main:app", reload=True)


def production():
    port = int(os.getenv("APP_PORT", 8000))

    print("Running migrations...")
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    print("Finished migrations")

    uvicorn.run("app.main:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if mode == "prod":
        production()
    else:
        development()
