from app import HOST, PORT, app

if __name__ == "__main__":
    app.run(host=HOST, debug=False, port=PORT)
