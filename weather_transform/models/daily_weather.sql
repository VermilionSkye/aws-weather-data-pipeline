SELECT
    DATE(recorded_at) as weather_date,
    city,
    AVG(temperature) as avg_temp,
    MIN(temperature) as min_temp,
    MAX(temperature) as max_temp,
    COUNT(*) as readings_count
FROM raw_data.weather_logs
GROUP BY 1, 2