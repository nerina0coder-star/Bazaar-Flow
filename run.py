from app import create_app, db
from dotenv import load_dotenv

sock, app = create_app()

if __name__ == "__main__":
    load_dotenv()
    sock.run(app=app, debug=True, host="0.0.0.0")
