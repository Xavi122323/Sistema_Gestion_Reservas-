from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import os
from xml.etree import ElementTree as ET

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/rest_db")
SOAP_SERVICE_URL = os.getenv("SOAP_SERVICE_URL", "http://soap_service:8080")  # Dirección del servicio SOAP

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id = Column(Integer, primary_key=True)
    room_number = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)

Base.metadata.create_all(engine)

@app.route("/reservations", methods=["POST"])
def create_reservation():
    session = SessionLocal()
    data = request.json
    try:
        soap_request = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hot="http://disponibilidad.hotel.com">
            <soapenv:Header/>
            <soapenv:Body>
                <hot:consultar_disponibilidad>
                    <hot:fecha_inicio>{data['start_date']}</hot:fecha_inicio>
                    <hot:fecha_fin>{data['end_date']}</hot:fecha_fin>
                    <hot:tipo_habitacion>{data['room_type']}</hot:tipo_habitacion>
                </hot:consultar_disponibilidad>
            </soapenv:Body>
        </soapenv:Envelope>
        """
        soap_response = requests.post(
            f"{SOAP_SERVICE_URL}",
            headers={"Content-Type": "text/xml"},
            data=soap_request
        )

        if soap_response.status_code != 200:
            return jsonify({"error": "Error al consultar disponibilidad"}), 500

        try:
            root = ET.fromstring(soap_response.text)
            ns = {"tns": "http://disponibilidad.hotel.com"}
            result_node = root.find(".//tns:consultar_disponibilidadResult", ns)
            available_rooms = [room.text for room in result_node.findall("tns:string", ns)]
        except Exception as e:
            print(f"Error al parsear la respuesta SOAP: {e}")
            return jsonify({"error": "Error al procesar respuesta SOAP"}), 500

        if not available_rooms:
            return jsonify({"error": "No hay disponibilidad"}), 400

        room_number = available_rooms[0]

        reservation = Reservation(
            room_number=room_number,
            customer_name=data["customer_name"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            status="active"
        )
        session.add(reservation)
        session.commit()

        return jsonify({
            "message": "Reserva creada exitosamente",
            "reservation_id": reservation.reservation_id
        }), 201

    except Exception as e:
        print(f"Error al crear reserva: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/reservations/<int:reservation_id>", methods=["GET"])
def get_reservation(reservation_id):
    session = SessionLocal()
    try:
        reservation = session.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
        if not reservation:
            return jsonify({"error": "Reserva no encontrada"}), 404

        return jsonify({
            "reservation_id": reservation.reservation_id,
            "room_number": reservation.room_number,
            "customer_name": reservation.customer_name,
            "start_date": reservation.start_date.strftime("%Y-%m-%d"),
            "end_date": reservation.end_date.strftime("%Y-%m-%d"),
            "status": reservation.status
        }), 200
    except Exception as e:
        print(f"Error al consultar reserva: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route("/reservations/<int:reservation_id>", methods=["DELETE"])
def cancel_reservation(reservation_id):
    session = SessionLocal()
    try:
        reservation = session.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
        if not reservation:
            return jsonify({"error": "Reserva no encontrada"}), 404

        reservation.status = "cancelled"
        session.commit()

        return jsonify({"message": "Reserva cancelada exitosamente"}), 200
    except Exception as e:
        print(f"Error al cancelar reserva: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
