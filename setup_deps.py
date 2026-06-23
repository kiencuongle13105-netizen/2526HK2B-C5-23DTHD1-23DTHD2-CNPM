import subprocess
import sys

packages = ["fastapi", "uvicorn", "sqlalchemy", "psycopg2-binary", "python-jose[cryptography]", "passlib[bcrypt]", "python-multipart"]
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
    print("Installation successful")
except Exception as e:
    print(f"Installation failed: {e}")
