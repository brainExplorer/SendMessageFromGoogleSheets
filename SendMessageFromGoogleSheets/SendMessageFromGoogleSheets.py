import time
import schedule
import gspread
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 🟢 Google Sheets API Kimlik Doğrulama
# Define Google Sheets API scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials
try:
    creds = Credentials.from_service_account_file("sample.json", scopes=scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet
    sheet = client.open("Web Scraping Data").sheet1

    # Test read operation
    print("First row:", sheet.row_values(1))

    # Test write operation
    sheet.append_row(["Test", "Connection", "Successful"])
    print("✅ Google Sheets API is working correctly!")

except Exception as e:
    print("❌ Error:", e)

# 🟢 Selenium Başlat
chrome_options = Options()
chrome_options.add_argument("--headless")  # Arkaplanda çalıştır
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

def scrape_data():
    print("📡 Web scraping başlatıldı...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://destinationwebsite.com")  # Gerçek site URL'sini ekleyin
    time.sleep(3)  # Sayfanın yüklenmesini bekle

    # 🔎 Kullanıcı bilgilerini çek
    users = driver.find_elements(By.CLASS_NAME, "user-card")  
    user_data = []

    for user in users:
        try:
            username = user.find_element(By.CLASS_NAME, "username").text if user.find_elements(By.CLASS_NAME, "username") else "N/A"
            user_type = user.find_element(By.CLASS_NAME, "type").text if user.find_elements(By.CLASS_NAME, "type") else "N/A"
            status = user.find_element(By.CLASS_NAME, "status").text if user.find_elements(By.CLASS_NAME, "status") else "N/A"
            location = user.find_element(By.CLASS_NAME, "location").text if user.find_elements(By.CLASS_NAME, "location") else "N/A"
            user_data.append([username, user_type, status, location, ""])
        except:
            continue  # Eğer hata olursa kullanıcıyı atla

    driver.quit()  # Tarayıcıyı kapat
    print(f"✅ {len(user_data)} kullanıcı bulundu.")
    return user_data

def check_duplicates(data):
    print("🔍 Duplicate kontrolü yapılıyor...")
    existing_usernames = sheet.col_values(1)  # Mevcut kullanıcı adlarını al
    for row in data:
        if row[0] in existing_usernames:
            row[4] = "Duplicate"
    return data

def save_to_google_sheets(data):
    print("📂 Google Sheets'e veri kaydediliyor...")
    for i, row in enumerate(data, start=2):
        sheet.update(f"A{i}:E{i}", [row])  # Daha hızlı güncelleme sağlar
    print("✅ Veri başarıyla kaydedildi.")

def send_messages(data):
    print("📨 Mesaj gönderme işlemi başlıyor...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    for i, user in enumerate(data, start=2):
        if user[1] == "Vendor" or user[4] == "Duplicate":
            continue  # Vendor ve duplicate kullanıcıları atla

        driver.get(f"https://example.com/message/{user[0]}")  
        time.sleep(2)

        try:
            message_box = driver.find_element(By.NAME, "message")
            message_box.send_keys("Merhaba, bu otomatik bir mesajdır.")  
            
            send_button = driver.find_element(By.ID, "send")
            if send_button:
                send_button.click()
                sheet.update_cell(i, 6, "Messaged")
                print(f"✅ {user[0]} kullanıcısına mesaj gönderildi.")
            else:
                raise Exception("Mesaj butonu bulunamadı")
        except:
            sheet.update_cell(i, 6, "Blocked")
            print(f"❌ {user[0]} kullanıcısına mesaj gönderilemedi!")

    driver.quit()
    print("✅ Mesaj gönderme işlemi tamamlandı.")

def main():
    print("🚀 Bot çalışıyor...")
    scraped_data = scrape_data()  # Web scraping yap
    processed_data = check_duplicates(scraped_data)  # Duplicate kontrolü
    save_to_google_sheets(processed_data)  # Veriyi kaydet
    send_messages(processed_data)  # Mesaj gönder

# ⏳ 15 dakikada bir çalıştır
schedule.every(15).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
