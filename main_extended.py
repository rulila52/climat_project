import RPi.GPIO as GPIO
import time
import smbus2
import bme280

# Крутим мотором при достижении температуры!


# Настройка BME280
port = 1
address = 0x77
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# Функция для считывания температуры с BME280
def read_temperature():
    data = bme280.sample(bus, address, calibration_params)
    print(data.temperature)
    return data.temperature

# Устанавливаем номер пина для ШИМ
pwm_pin = 18

# Пороговая температура для вращения мотора (в градусах Цельсия)
threshold_temperature = 30


try:
    # Настройка GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pin, GPIO.OUT)
    
    # Создаем объект PWM
    pwm = GPIO.PWM(pwm_pin, 100)
    
    while True:
        # Считываем температуру
        temperature = read_temperature()
        
        # Если температура выше порога - вращаем мотором
        if temperature > threshold_temperature:
            pwm.start(100)  # Максимальная скорость
        else:
            pwm.stop()  # Остановка мотора
        
        time.sleep(1)  # Пауза между измерениями

except KeyboardInterrupt:
    # Останавливаем PWM при нажатии Ctrl+C
    pwm.stop()
    GPIO.cleanup()
