CREATE TABLE IF NOT EXISTS rooms (
    room_id SERIAL PRIMARY KEY,
    room_number VARCHAR(50) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('available', 'maintenance', 'reserved'))
);
