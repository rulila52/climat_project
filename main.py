import RPi.GPIO as GPIO
import time

# Устанавливаем номер пина для ШИМ
pwm_pin = 18

try:
    # Настройка GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pin, GPIO.OUT)
    
    # Создаем объект PWM
    pwm = GPIO.PWM(pwm_pin, 100)
    
    # Запускаем PWM с максимальной скоростью (100%)
    pwm.start(100)
    
    # Ждем 5 секунд, а затем останавливаем мотор
    time.sleep(5)
    
    # Останавливаем PWM
    pwm.stop()

finally:
    # Выполняем очистку GPIO перед выходом
    GPIO.cleanup()
