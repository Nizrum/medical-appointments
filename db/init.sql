-- Пользователи
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL CHECK (role IN ('patient', 'admin', 'doctor')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Врачи
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    specialization VARCHAR(255) NOT NULL,
    cabinet_number VARCHAR(10) NOT NULL,
    appointment_duration INTEGER DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Услуги
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    duration INTEGER DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Связь врачей с услугами
CREATE TABLE doctor_services (
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    service_id INTEGER REFERENCES services(id) ON DELETE CASCADE,
    PRIMARY KEY (doctor_id, service_id)
);

-- Шаблоны расписания (рабочая неделя)
CREATE TABLE schedule_templates (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_working BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Временные слоты
CREATE TABLE time_slots (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'free' CHECK (status IN ('free', 'booked', 'blocked', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(doctor_id, start_time)
);

-- Записи на приём
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    time_slot_id INTEGER REFERENCES time_slots(id) ON DELETE CASCADE,
    service_id INTEGER REFERENCES services(id),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled')),
    complaints TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Настройки клиники
CREATE TABLE clinic_settings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    working_hours TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Уведомления
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для производительности
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_time_slots_doctor_date ON time_slots(doctor_id, start_time);
CREATE INDEX idx_time_slots_status ON time_slots(status);
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_date ON appointments(created_at);

-- Вставка тестовых данных
INSERT INTO clinic_settings (name, address, phone, email, working_hours) VALUES 
('Городская поликлиника №1', 'ул. Медицинская, 15, г. Москва', '+7 (495) 123-45-67', 'info@clinic.ru', 'Пн-Пт: 8:00-20:00, Сб: 9:00-15:00');

-- Создание пользователей
INSERT INTO users (email, hashed_password, full_name, phone, role) VALUES 
('admin@clinic.ru', '$2b$12$mnxX2kMwUoe36LDik6SfIO3dC6rVXKgSFojvJMdxD/wCSsygrU4NS', 'Иванов Иван Администратор', '+7 (495) 111-11-11', 'admin'),
('doctor@clinic.ru', '$2b$12$puDFDWUMkhqZVrfWdIUPlOB8sCLsDFmK5RzkRRQzg8bDFdJz2CkzW', 'Петрова Анна Врач', '+7 (495) 222-22-22', 'doctor'),
('patient@clinic.ru', '$2b$12$puDFDWUMkhqZVrfWdIUPlOB8sCLsDFmK5RzkRRQzg8bDFdJz2CkzW', 'Сидоров Петр Пациент', '+7 (495) 333-33-33', 'patient');

-- Создание врачей
INSERT INTO doctors (user_id, specialization, cabinet_number, appointment_duration) VALUES 
((SELECT id FROM users WHERE email = 'doctor1@clinic.ru'), 'Терапевт', '101', 30);

-- Создание услуг
INSERT INTO services (name, description, price, duration) VALUES 
('Первичный приём терапевта', 'Осмотр, сбор анамнеза, назначение лечения', 1500.00, 30),
('Повторный приём терапевта', 'Контроль лечения, корректировка терапии', 1200.00, 20),
('ЭКГ', 'Электрокардиограмма с расшифровкой', 800.00, 20);

-- Связь врача с услугами
INSERT INTO doctor_services (doctor_id, service_id) VALUES 
(1, 1), (1, 2), (1, 3);

-- Создание шаблона расписания (Пн-Пт 9:00-18:00)
INSERT INTO schedule_templates (doctor_id, day_of_week, start_time, end_time) VALUES 
(1, 0, '09:00', '18:00'),
(1, 1, '09:00', '18:00'),
(1, 2, '09:00', '18:00'),
(1, 3, '09:00', '18:00'),
(1, 4, '09:00', '18:00');

DO $$
DECLARE
    doc_id INTEGER := 1;
    start_date DATE := CURRENT_DATE;
    end_date DATE := CURRENT_DATE + 7;
    current_date DATE;
    slot_start TIMESTAMP;
    slot_end TIMESTAMP;
BEGIN
    FOR current_date IN SELECT generate_series(start_date, end_date, '1 day'::interval) LOOP
        IF EXTRACT(DOW FROM current_date) BETWEEN 0 AND 4 THEN
            FOR slot_start IN SELECT generate_series(
                (current_date + TIME '09:00')::TIMESTAMP,
                (current_date + TIME '17:30')::TIMESTAMP,
                '30 minutes'::interval
            ) LOOP
                slot_end := slot_start + INTERVAL '30 minutes';
                INSERT INTO time_slots (doctor_id, start_time, end_time, status)
                VALUES (doc_id, slot_start, slot_end, 'free')
                ON CONFLICT (doctor_id, start_time) DO NOTHING;
            END LOOP;
        END IF;
    END LOOP;
END $$;
