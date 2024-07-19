from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def descargar_foto_de_perfil(dni):
    # Inicializar el navegador
    driver = webdriver.Chrome()  # ChromeDriver debe estar en tu PATH (OS)
    driver.get("https://eldni.com/pe/buscar-datos-por-dni")
    time.sleep(1)  # Esperar tiempo suficiente para escanear el código QR

    try:
        # 01. Buscar el campo de búsqueda y escribir el DNI
        search_box = driver.find_element(By.XPATH, '//*[@id="dni"]')
        search_box.clear()
        search_box.send_keys(dni)

        # 02. Hacer clic en el botón de búsqueda
        search_button = driver.find_element(By.XPATH, '//*[@id="btn-buscar-datos-por-dni"]')
        search_button.click()
        time.sleep(2)  # Esperar a que aparezcan los resultados de búsqueda

        # 04. Obtener la URL de la foto de perfil
        input_element = driver.find_element(By.XPATH, '//*[@id="completos"]')
        picture_url = input_element.get_attribute('value')
        return picture_url
    except Exception as e:
        return str(e)
    finally:
        # Cerrar el navegador
        driver.quit()

@app.route('/get_profile_picture', methods=['GET'])
def get_profile_picture():
    dni = request.args.get('dni')
    if dni:
        picture_url = descargar_foto_de_perfil(dni)
        response = {
            'dni': dni,
            'picture_url': picture_url
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'DNI parameter is missing'}), 400

if __name__ == '__main__':
    app.run(debug=True)
