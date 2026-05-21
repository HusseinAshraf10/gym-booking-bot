# 🏋️ Gym Class Booking Bot

An intelligent automation tool that logs into a gym scheduling website, finds target classes, books them (or joins the waitlist), and verifies all bookings — with built-in network resilience.

Built with **Python + Selenium**.

---

## 🎯 What It Does

- ✅ Logs in automatically using stored credentials
- 🔍 Scans the weekly schedule for **Tuesday & Thursday 6:00 PM** classes
- 📅 Books available classes or joins the waitlist if full
- 🔄 Skips already-booked or already-waitlisted classes
- 🔁 Retries failed actions up to 7 times (network resilience)
- ✔️ Navigates to "My Bookings" and verifies every booking was saved

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| Selenium | Browser automation |
| WebDriverWait | Smart element waiting |
| python-dotenv | Secure credential management |
| ChromeDriver | Chrome browser control |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/gym-booking-bot.git
cd gym-booking-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file
```
MY_EMAIL=your_email@example.com
MY_PASSWORD=your_password
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 4. Run the bot
```bash
python main.py
```

---

## 🔑 Key Features Explained

### Smart Retry Logic
All critical actions (login, booking, navigation) are wrapped in a `retry()` function that handles `TimeoutException` and retries up to 7 times with a 1-second delay between attempts.

```python
def retry(func, retries=7, description=None):
    for i in range(retries):
        try:
            return func()
        except TimeoutException:
            if i == retries - 1:
                raise
            time.sleep(1)
```

### Booking State Detection
The bot reads the button text to determine what action is needed:

| Button Text | Action Taken |
|-------------|-------------|
| `Book Class` | Books the class |
| `Join Waitlist` | Joins the waitlist |
| `Booked` | Skips (already booked) |
| `Waitlisted` | Skips (already on waitlist) |

### End-to-End Verification
After booking, the bot navigates to the "My Bookings" page and counts verified Tue/Thu 6 PM entries to confirm everything was saved correctly.

---

## 📊 Sample Output

```
Trying login. Attempt: 1
Found 14 class cards.
✓ Successfully booked: Yoga on Tuesday
✓ Joined waitlist for: Spin Class on Thursday

--- Booking Summary ---
Classes booked:        1
Waitlist joined:       1
Already booked:        0
Total processed:       2

--- VERIFICATION RESULT ---
Expected: 2 bookings
Found:    2 bookings
✅ SUCCESS: All bookings verified!
```

---

## 📁 Project Structure

```
gym-booking-bot/
├── main.py            # Main automation script
├── .env               # Your credentials (not tracked by Git)
├── .gitignore         # Ignores .env and chrome_profile/
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## 🧠 Skills Demonstrated

- Browser automation with Selenium WebDriver
- DOM traversal using CSS Selectors and XPath
- Dynamic element waiting with `WebDriverWait`
- Error handling and retry mechanisms
- Secure credential management with environment variables
- End-to-end test verification logic

---

## 📌 Notes

- The bot uses a persistent Chrome profile (`chrome_profile/`) to maintain session state across runs.
- Target URL: [https://appbrewery.github.io/gym/](https://appbrewery.github.io/gym/) (demo site from Angela Yu's course)
- You must create an account on the gym site manually before running the bot.

---

## 👨‍💻 Author

**Hussein** — Python Developer in training  
🔗 [LinkedIn](https://linkedin.com/in/hussein-ashraf-969737269/) · [GitHub](https://github.com/HusseinAshraf10)
