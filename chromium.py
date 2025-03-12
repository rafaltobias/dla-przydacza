from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Ścieżka do ChromeDriver
CHROMEDRIVER_PATH = r"C:/Users/Rafał/Downloads/chrome/chromedriver-win64/chromedriver.exe"

# Ścieżka do pliku CRX wtyczki Proton VPN
PROTON_PLUGIN_PATH = r"C:/Users/Rafał/Downloads/Proton-VPN-Fast-Secure-Chrome-Web-Store.crx"

# Liczba przeglądarek do uruchomienia jednocześnie
BATCH_SIZE = 5

# Całkowita liczba przeglądarek do uruchomienia
TOTAL_BROWSERS = 30

def create_driver_with_extension(plugin_path):
    """Tworzy nową instancję przeglądarki Chrome z wtyczką."""
    chrome_options = Options()
    chrome_options.add_extension(plugin_path)  # Dodaj wtyczkę z pliku .crx
    chrome_options.add_argument("--no-sandbox")  # Wyłącz piaskownicę
    chrome_options.add_argument("--disable-dev-shm-usage")  # Unikaj problemów z pamięcią
    chrome_options.add_argument("--disable-gpu")  # Wyłącz akcelerację GPU
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def main():
    total_batches = TOTAL_BROWSERS // BATCH_SIZE
    remaining_browsers = TOTAL_BROWSERS % BATCH_SIZE

    for batch in range(total_batches):
        print(f"Uruchamianie partii {batch + 1} z {total_batches}")
        drivers = []

        # Uruchom partię przeglądarek
        for _ in range(BATCH_SIZE):
            driver = create_driver_with_extension(PROTON_PLUGIN_PATH)
            drivers.append(driver)

        # Poczekaj, aby wtyczka została zainstalowana (możesz dostosować czas)
        time.sleep(10)

        # Zamknij wszystkie przeglądarki w tej partii
        for driver in drivers:
            try:
                driver.quit()  # Zamknij przeglądarkę
            except Exception as e:
                print(f"Błąd podczas zamykania przeglądarki: {e}")

        print(f"Partia {batch + 1} zakończona.")

    # Uruchom pozostałe przeglądarki (jeśli liczba nie jest podzielna przez BATCH_SIZE)
    if remaining_browsers > 0:
        print(f"Uruchamianie pozostałych {remaining_browsers} przeglądarek")
        drivers = []

        for _ in range(remaining_browsers):
            driver = create_driver_with_extension(PROTON_PLUGIN_PATH)
            drivers.append(driver)

        time.sleep(10)

        for driver in drivers:
            try:
                driver.quit()
            except Exception as e:
                print(f"Błąd podczas zamykania przeglądarki: {e}")

        print("Pozostałe przeglądarki zakończone.")

    print("Wszystkie przeglądarki zostały obsłużone.")

if __name__ == "__main__":
    main()