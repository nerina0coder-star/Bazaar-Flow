from app import create_app, db

sock, app = create_app()

if __name__ == "__main__":
    sock.run(app=app, debug=True)