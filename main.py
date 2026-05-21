import os
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import time
from dotenv import load_dotenv

load_dotenv()
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
GYM_URL = "https://appbrewery.github.io/gym/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options = chrome_options)
driver.maximize_window()
driver.get(url= GYM_URL)

wait = WebDriverWait(driver, 2)

driver.get(url= GYM_URL)

def retry(func, retries=7, description=None):
    for i in range(retries):
        print(f"Trying {description}. Attempt: {i + 1}")
        try:
            return func()
        except TimeoutException:
            if i == retries - 1:
                raise
            time.sleep(1)

def login():
    login_button = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
    login_button.click()

    email_input = wait.until(ec.presence_of_element_located((By.ID, "email-input")))
    email_input.send_keys(MY_EMAIL)
    password_input = driver.find_element(By.ID, "password-input")
    password_input.send_keys(MY_PASSWORD)
    submit = driver.find_element(By.CSS_SELECTOR, "#submit-button")
    submit.click()

    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

def book_class(booking_button):
    booking_button.click()

    wait.until(lambda d: booking_button.text == "Booked")

def join_waitlist(card):
    book_button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
    book_button.click()

    wait.until(lambda d: card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']").text
                         == "Waitlisted")


retry(login, description= "login")

class_card = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

bookedCount = 0
waitListCount = 0
alreadyBookedCount = 0

processed_class = []

for card in class_card:
    day_group = card.find_element(By.XPATH, './ancestor::div[contains(@id, "day-group-")]')
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    if "Tue" in day_title or "Thu" in day_title:
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time']").text
        if "6:00 PM" in time_text:
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            book_button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

            class_info = f"{class_name} on {day_title}"
            if book_button.text == "Booked":
                print(f"Already booked: {class_info}")
                alreadyBookedCount += 1
                processed_class.append(f"[Booked] {class_info}")
            elif book_button.text == "Waitlisted":
                print(f"Already on Waitlisted: {class_info}")
                alreadyBookedCount += 1
                processed_class.append(f"[Waitlisted] {class_info}")
            elif book_button.text == "Book Class":
                retry(lambda: book_class(book_button), description= "Booking")
                bookedCount += 1
                print(f"✓ Successfully booked: {class_info}")
                processed_class.append(f"[New Booking] {class_info}")
            elif book_button.text == "Join Waitlist":
                retry(lambda: join_waitlist(card), description= "Join Waitlist")
                print(f"✓ joined waitlist for: {class_info}")
                waitListCount += 1
                processed_class.append(f"[New waitlist] {class_info}")


print("\n---Booking summary---\n")
print(f"Classes booked: {bookedCount}")
print(f"Waitlist joined: {waitListCount}")
print(f"Already booked/Waitlist: {alreadyBookedCount}")
print(f"Total tuesday 6pm classes processed: {bookedCount + waitListCount + alreadyBookedCount}")

print("\n--- DETAILED CLASS LIST ---")
for class_detail in processed_class:
    print(f" * {class_detail}")


total_booked = alreadyBookedCount + bookedCount + waitListCount
print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")
print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

# Navigate to My Bookings page
def get_my_booking():
    my_booking_link = wait.until(ec.element_to_be_clickable((By.ID, "my-bookings-link")))
    my_booking_link.click()

    wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))
    cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
    if not cards:
        raise TimeoutException("No Booking cards found - page may not have loaded")
    return cards

all_cards = retry(get_my_booking, description= "Get my bookings")

verified_count = 0

for card in all_cards:
    try:
        when_pargraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
        when_text = when_pargraph.text
        if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
            class_name = card.find_element(By.TAG_NAME, "h3").text
            print(f"✓ verified: {class_name}")
            verified_count += 1
    except NoSuchElementException:
        pass

print(f"\n--- VERIFICATION RESULT ---")
print(f"Expected: {total_booked} bookings")
print(f"Found: {verified_count} bookings")

if total_booked == verified_count:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {total_booked - verified_count} bookings")






