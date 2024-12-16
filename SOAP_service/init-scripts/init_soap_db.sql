CREATE TABLE IF NOT EXISTS availability (
    room_id SERIAL PRIMARY KEY,
    room_type VARCHAR(50) NOT NULL,
    available_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('disponible', 'reservada'))
);

INSERT INTO availability (room_type, available_date, status)
VALUES
('simple', '2024-12-15', 'disponible'),
('simple', '2024-12-16', 'disponible'),
('doble', '2024-12-15', 'reservada'),
('suite', '2024-12-15', 'disponible'),
('suite', '2024-12-16', 'disponible');
