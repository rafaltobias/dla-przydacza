import tkinter as tk
from tkinter import ttk, messagebox
from sv_ttk import set_theme  # Import motywu Sun Valley
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

# Konfiguracja ścieżek
CHROMEDRIVER_PATH = r"chromedriver.exe"
PROTON_PLUGIN_PATH = r"Proton-VPN-Fast-Secure-Chrome-Web-Store.crx"
PROTON_LOGIN_URL = "https://account.proton.me/vpn"

def create_driver_with_extension():
    """Tworzy przeglądarkę z wtyczką Proton VPN"""
    chrome_options = Options()
    chrome_options.add_extension(PROTON_PLUGIN_PATH)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=750,350")
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

def proton_login(driver, email, password):
    """Automatyzacja logowania do Proton VPN"""
    try:
        driver.get(PROTON_LOGIN_URL)
        
        # Wypełnij nazwę użytkownika
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#username"))
        ).send_keys(email)
        time.sleep(3)  # Opoźnienie
        
        # Kliknij przycisk "Kontynuuj"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.w-full.button-large.button-solid-norm.mt-6[type='submit']"))
        ).click()
        time.sleep(3)  # Opoźnienie
        
        # Wypełnij hasło
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#password[autocomplete='current-password']"))
        ).send_keys(password)
        time.sleep(3)  # Opoźnienie
        
        # Kliknij przycisk "Zaloguj się"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.w-full.button-large.button-solid-norm.mt-6[type='submit']"))
        ).click()
        
        time.sleep(5)  # Czekaj na pełne zalogowanie
        return True
    
    except Exception as e:
        print(f"Błąd logowania: {str(e)}")
        return False

def run_browsers(num_browsers, twitch_url, email, password, manual_login):
    """Uruchamia przeglądarki z Twitch po zalogowaniu i dodaje autorefresh co 900s"""
    drivers = []
    for _ in range(num_browsers):
        driver = create_driver_with_extension()
        if not manual_login:
            # Automatyczne logowanie
            if proton_login(driver, email, password):
                driver.get(twitch_url)
                drivers.append(driver)
        else:
            # Ręczne logowanie
            # Otwórz Twitch na głównej karcie
            
            # Otwórz nową kartę z logowaniem Proton VPN
            driver.execute_script("window.open('');")  # Otwórz nową kartę
            driver.switch_to.window(driver.window_handles[-1])  # Przejdź do nowej karty
            driver.get(PROTON_LOGIN_URL)  # Otwórz stronę logowania Proton VPN
            time.sleep(60)  
            driver.get(twitch_url)

            drivers.append(driver)
        time.sleep(1)

    # Autorefresh co 900 sekund (15 minut)
    refresh_interval = 900  # 900 sekund = 15 minut
    while True:
        time.sleep(refresh_interval)
        for driver in drivers:
            try:
                driver.refresh()  # Odśwież przeglądarkę
                print("Odświeżono przeglądarkę.")
            except Exception as e:
                print(f"Błąd podczas odświeżania przeglądarki: {str(e)}")

def start_program():
    """Funkcja uruchamiająca program po kliknięciu przycisku Start"""
    try:
        email = email_entry.get()
        password = password_entry.get()
        num_browsers = int(num_browsers_entry.get())  # Pobierz liczbę okien z pola tekstowego
        twitch_url = twitch_url_entry.get()
        manual_login = manual_login_var.get()


        if num_browsers <= 0:
            messagebox.showerror("Błąd", "Liczba okien musi być większa od 0!")
        else:
            threading.Thread(
                target=run_browsers,
                args=(num_browsers, twitch_url, email, password, manual_login),
                daemon=True
            ).start()
    except ValueError:
        messagebox.showerror("Błąd", "Liczba okien musi być liczbą całkowitą!")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Twitch Viewer")
root.geometry("400x350")

# Ustawienie motywu Sun Valley
set_theme("light")  # Możesz zmienić na "dark" dla ciemnego motywu

# Tworzenie interfejsu użytkownika
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Nazwa użytkownika/e-mail").pack()
email_entry = ttk.Entry(frame)
email_entry.pack()

ttk.Label(frame, text="Hasło").pack()
password_entry = ttk.Entry(frame, show="*")
password_entry.pack()

ttk.Label(frame, text="Liczba okien").pack()
num_browsers_entry = ttk.Entry(frame)  # Pole tekstowe do wpisania liczby okien
num_browsers_entry.insert(0, "5")  # Domyślna wartość
num_browsers_entry.pack()

ttk.Label(frame, text="URL Twitch").pack()
twitch_url_entry = ttk.Entry(frame)
twitch_url_entry.insert(0, "https://www.twitch.tv/")
twitch_url_entry.pack()

manual_login_var = tk.BooleanVar()
manual_login_checkbox = ttk.Checkbutton(frame, text="Ręczne logowanie", variable=manual_login_var)
manual_login_checkbox.pack()

start_button = ttk.Button(frame, text="Start", command=start_program)
start_button.pack()

# Uruchomienie głównej pętli aplikacji
root.mainloop()