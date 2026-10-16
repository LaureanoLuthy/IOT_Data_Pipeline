-- 1. View: Média de temperatura por dispositivo e localização
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT 
    device_id,
    location,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY device_id, location;

-- 2. View: Contagem de leituras por hora do dia
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT 
    hora,
    COUNT(*) AS contagem,
    ROUND(AVG(temperature)::numeric, 2) AS temp_media_hora
FROM temperature_readings
GROUP BY hora
ORDER BY hora ASC;

-- 3. View: Temperaturas máximas, mínimas e médias por dia
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT 
    data,
    MAX(temperature) AS temp_max,
    MIN(temperature) AS temp_min,
    ROUND(AVG(temperature)::numeric, 2) AS temp_media
FROM temperature_readings
GROUP BY data
ORDER BY data ASC;