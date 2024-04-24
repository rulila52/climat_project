import RPi.GPIO as GPIO
import time
import smbus2
import bme280
import os

# Крутим мотором при достижении температуры!

# Настройка BME280
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# Функция для считывания температуры с BME280
def read_temperature():
    data = bme280.sample(bus, address, calibration_params)
    print(f"Текущая температура {data.temperature}")
    return data.temperature

# Функция для записи текущей температуры в файл
def write_current_temperature(temperature):
    with open("current_temperature.txt", "w") as file:
        file.write(str(temperature))

# Устанавливаем номер пина для ШИМ
pwm_pin = 18

# Путь к файлу с пороговой температурой
threshold_file_path = "threshold_temperature.txt"

# Значение пороговой температуры по умолчанию
default_threshold_temperature = 30

try:
    # Настройка GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pin, GPIO.OUT)
    
    # Создаем объект PWM
    pwm = GPIO.PWM(pwm_pin, 100)
    
    while True:
        # Чтение пороговой температуры из файла
        if os.path.exists(threshold_file_path):
            with open(threshold_file_path, 'r') as file:
                threshold_temperature_str = file.read().strip()
                print(f"Пороговое значение {threshold_temperature_str}")
                try:
                    threshold_temperature = float(threshold_temperature_str)
                except ValueError:
                    print("Ошибка: Невозможно преобразовать значение пороговой температуры в число. "
                          "Используется значение по умолчанию.")
                    threshold_temperature = default_threshold_temperature
        else:
            print("Файл с пороговой температурой не найден. Используется значение по умолчанию.")
            threshold_temperature = default_threshold_temperature

        # Считываем температуру
        temperature = read_temperature()

        # Записываем текущую температуру в файл
        write_current_temperature(temperature)
        
        # Если температура выше порога - вращаем мотором
        if temperature > threshold_temperature:
            pwm.start(99)  # Максимальная скорость
        else:
            pwm.stop()  # Остановка мотора
        
        time.sleep(1)  # Пауза между измерениями

except KeyboardInterrupt:
    # Останавливаем PWM при нажатии Ctrl+C
    pwm.stop()
    GPIO.cleanup()