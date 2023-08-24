from app import app, db


if __name__ == "__main__":
    # Create the database tables
    with app.app_context():
        db.create_all()

    # Run the development server
    app.run(host="0.0.0.0", port=8000, debug=True)

