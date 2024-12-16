from spyne import Application, rpc, ServiceBase, Unicode, Date, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from sqlalchemy import create_engine, Column, Integer, String, Date as SQLDate, and_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/soap_db")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Availability(Base):
    __tablename__ = "availability"

    room_id = Column(Integer, primary_key=True)
    room_type = Column(String, nullable=False)
    available_date = Column(SQLDate, nullable=False)
    status = Column(String, nullable=False)

class HotelAvailabilityService(ServiceBase):
    @rpc(Date, Date, Unicode, _returns=Array(Unicode))
    def consultar_disponibilidad(ctx, fecha_inicio, fecha_fin, tipo_habitacion):
        """
        Verifica la disponibilidad de habitaciones basado en tipo y rango de fechas.
        """
        session = SessionLocal()
        try:
            num_days = (fecha_fin - fecha_inicio).days + 1
            print(f"Rango de fechas: {fecha_inicio} a {fecha_fin}, Días: {num_days}")

            query = session.query(Availability.room_id) \
                .filter(
                    Availability.room_type == tipo_habitacion,
                    Availability.status == 'disponible',
                    Availability.available_date.between(fecha_inicio, fecha_fin)
                ).distinct()

            results = query.all()
            available_rooms = [str(row[0]) for row in results]
        except Exception as e:
            print(f"Error al consultar disponibilidad: {e}")
            available_rooms = []
        finally:
            session.close()

        return available_rooms

application = Application(
    [HotelAvailabilityService],
    tns='http://disponibilidad.hotel.com',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    Base.metadata.create_all(engine)

    print("Iniciando el servidor SOAP en http://0.0.0.0:8080 ...")
    server = make_server('0.0.0.0', 8080, WsgiApplication(application))
    server.serve_forever()
