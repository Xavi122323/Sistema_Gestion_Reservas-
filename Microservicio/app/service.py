from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/inventory_db")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True)
    room_number = Column(String, nullable=False)
    room_type = Column(String, nullable=False)
    status = Column(String, nullable=False)

Base.metadata.create_all(engine)

@app.route("/rooms", methods=["POST"])
def add_room():
    session = SessionLocal()
    data = request.json
    try:
        room = Room(
            room_number=data["room_number"],
            room_type=data["room_type"],
            status=data["status"]
        )
        session.add(room)
        session.commit()
        return jsonify({"message": "Room added", "room_id": room.room_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/rooms/<int:room_id>", methods=["PATCH"])
def update_room_status(room_id):
    session = SessionLocal()
    data = request.json
    try:
        room = session.query(Room).filter(Room.room_id == room_id).first()
        if not room:
            return jsonify({"error": "Room not found"}), 404

        room.status = data.get("status", room.status)
        session.commit()

        return jsonify({"message": "Room status updated"}), 200
    except Exception as e:
        print(f"Error al actualizar habitación: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
