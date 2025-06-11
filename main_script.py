import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

from datetime import datetime, timedelta





# Get current Windows username
windows_username = os.getlogin()

# Read profile number from file
def get_profile_number():
    profile_file = "desk/profilen.txt"
    try:
        with open(profile_file, 'r') as f:
            profile_number = f.read().strip()
            return profile_number
    except FileNotFoundError:
        print(f"Profile number file not found at {profile_file}")
        return "1"  # Default to Profile 1 if file doesn't exist

profile_number = get_profile_number()





# Define paths for ChromeDriver executables
chromedriver_paths = [
    r"desk\chromedriver.exe"
]

# Define Chrome user profile directory using detected username and profile number
chrome_profiles = [
    fr"C:\Users\{windows_username}\AppData\Local\Google\Chrome\User Data\Profile {profile_number}"
]





# Function to read URL from file
def read_url_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()  # Read the first line and remove any extra spaces or newlines
    except Exception as e:
        print(f"Error reading URL from file: {e}")
        return None

# Function to read the first key from key.txt
def read_key_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if lines:
                return lines[0].strip(), lines[1:]  # Return the first key and the rest of the lines
            else:
                print("No keys available in the file.")
                return None, []
    except Exception as e:
        print(f"Error reading key from file: {e}")
        return None, []



def open_chrome_instance(driver_path, profile_path, window_index, url=None):
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={profile_path}")  # Use the existing profile
    chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
    chrome_options.add_argument("--log-level=3")  # Reduce logging output
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")








    # Network & Performance Optimizations
    chrome_options.add_argument('--disable-gpu')  
    chrome_options.add_argument('--disable-software-rasterizer')  
    chrome_options.add_argument('--disable-dev-shm-usage')  # Prevents crashes in Docker/Linux
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--disable-logging')  
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  
    chrome_options.add_argument('--disable-infobars')  
    chrome_options.add_argument('--disable-notifications')  
    chrome_options.add_argument('--dns-prefetch-disable')  
    chrome_options.add_argument('--disable-background-networking')  

    # Force faster page loads (aggressive optimizations)
    chrome_options.add_argument('--disable-preconnect')  
    chrome_options.add_argument('--disable-http2')  # Fallback to HTTP/1.1 (sometimes faster)
    chrome_options.add_argument('--disable-cache')  # Bypass cache (if issues with stale data)
    chrome_options.add_argument('--disk-cache-size=1')  # Minimal disk cache
    chrome_options.add_argument('--media-cache-size=1')  
    chrome_options.add_argument('--aggressive-cache-discard')  






    service = Service(driver_path)
    browser = webdriver.Chrome(service=service, options=chrome_options)

    # Define window sizes and spacing
    window_width, window_height = 375, 800
    screen_padding_x = 125  # Space between columns
    screen_padding_y = 80  # Space between rows

    # Arrange based on the window index
    if window_index == 0:  # Profile 1 (Left Side)
        x_position, y_position = 1, 1
    elif window_index == 1:  # Profile 2 (Right Side)
        x_position, y_position = window_width + screen_padding_x, 0

    browser.set_window_position(x_position, y_position)

    if url:
        browser.get(url)
        print(f"Opened URL: {url}")

        # Wait for cookies and local storage to be set (simulate real session)
        time.sleep(2)

        # Try to unlock the wallet (if locked)
        try:
            input_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div[5]/div/div[1]/input"
            input_field = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, input_xpath))
            )
            input_field.clear()
            input_field.send_keys("Aixfly@1122")
            print("Entered wallet password.")

            button_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div[6]/div/button"
            button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            button.click()
            print("Unlocked wallet.")
        except Exception:
            print("Wallet is not locked or unlock failed.")

        # Wait for SVG to be visible (wallet unlocked confirmation)
        try:
            svg_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div[2]"
            WebDriverWait(browser, 30).until(
            EC.visibility_of_element_located((By.XPATH, svg_xpath))
            )
            print("Wallet unlocked ")
            # Open the extension import page in the same tab
            import_url = "chrome-extension://opfgelmcmbiajamepnmloijbpoleiama/popup.html#/import/pkey?onboarding=true"
            browser.get(import_url)
            print("Importing Page opening")

            # Wait for the input field to be present
            input_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div/input"
            input_field = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, input_xpath))
            )

            # Read one key from key.txt and move it to activekey.txt
            key_file = "desk/key.txt"
            active_key_file = "desk/activekey.txt"
            key, remaining_keys = read_key_from_file(key_file)
            if key:
                # Input the key
                input_field.clear()
                input_field.send_keys(key)
                print(f"Inputted wallet key: {key}")

                # Move the used key to activekey.txt (do not add '| Used')
                with open(active_key_file, "a") as akf:
                    akf.write(key + "\n")
                with open(key_file, "w") as kf:
                    kf.writelines(remaining_keys)

                # Click the import button
                import_btn_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div/button"
                import_btn = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, import_btn_xpath))
                )
                import_btn.click()
                print("Clicked import button.")

                # Wait for the confirmation element to appear
                confirm_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div[1]/div[1]"
                try:
                    WebDriverWait(browser, 3).until(
                        EC.visibility_of_element_located((By.XPATH, confirm_xpath))
                    )
                    print("Wallet unlocked confirmation detected.")
                    time.sleep(2)  # Wait for a moment to ensure the confirmation is stable
                    # Open URL from loginurl.txt in the same tab
                    login_url = read_url_from_file("desk/loginurl.txt")
                    if login_url:
                        browser.get(login_url)
                        print(f"Opened login URL: {login_url}")
                        # Wait for the "Log in with Wallet" button and click it
                        try:
                            login_btn_xpath = "//button[contains(., 'Log in with Wallet')]"
                            login_btn = WebDriverWait(browser, 20).until(
                                EC.element_to_be_clickable((By.XPATH, login_btn_xpath))
                            )
                            login_btn.click()
                            time.sleep(2)  # Wait for the button click to register
                            print("Clicked 'Log in with Wallet' button.")
                            # Wait for and click the "Rainbow" button by its text
                            rainbow_btn_xpath = "//button[contains(., 'Rainbow')]"
                            rainbow_btn = WebDriverWait(browser, 20).until(
                                EC.element_to_be_clickable((By.XPATH, rainbow_btn_xpath))
                            )
                            rainbow_btn.click()
                            print("Clicked 'Rainbow' button.")

                            # Open a new tab and switch to it
                            browser.execute_script("window.open('');")
                            browser.switch_to.window(browser.window_handles[-1])
                            print("Opened and switched to new tab.")

                            # Open the extension approval page in the new tab
                            approval_url = "chrome-extension://opfgelmcmbiajamepnmloijbpoleiama/popup.html"
                            browser.get(approval_url)
                            print("Opened approval page in new tab.")

                            # Wait for "Connect to zealy.io" button and click it
                            try:
                                connect_btn_xpath = "//*[contains(text(), 'Connect to zealy.io')]"
                                connect_btn = WebDriverWait(browser, 60).until(
                                    EC.element_to_be_clickable((By.XPATH, connect_btn_xpath))
                                )
                                connect_btn.click()
                                print("Clicked 'Connect to zealy.io' button.")
                            except Exception as e:
                                print(f"'Connect to zealy.io' button not found or not clickable: {e}")

                            # Wait for "Sign" button, reload until available, then click
                            sign_btn_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/button"
                            sign_clicked = False
                            max_attempts = 30
                            for attempt in range(max_attempts):
                                try:
                                    sign_btn = WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, sign_btn_xpath))
                                    )
                                    sign_btn.click()
                                    print("Clicked 'Sign' button.")
                                    sign_clicked = True

                                    # Wait for the success message to appear
                                    success_msg_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div[2]"
                                    WebDriverWait(browser, 10).until(
                                        EC.visibility_of_element_located((By.XPATH, success_msg_xpath))
                                    )
                                    print("Success message appeared.")
                                    #close the new tab after successful click
                                    browser.close()  # Close the new tab
                                    # Just switch back to the main tab, do not close the browser
                                    browser.switch_to.window(browser.window_handles[0])
                                    print("Switched back to main tab.")
                                    break  # Exit the loop after successful click
                                except Exception as e:
                                    print(f"'Sign' button not found or not clickable (attempt {attempt+1}/{max_attempts})")
                                    browser.refresh()
                                    time.sleep(1)
                            if not sign_clicked:
                                print("'Sign' button not found after multiple reloads.")

                            # Wait for confirmation element (no captcha handling)
                            start_time = datetime.now()
                            max_wait_seconds = 3600  # 1 hour

                            while True:
                                elapsed = (datetime.now() - start_time).total_seconds()
                                if elapsed >= max_wait_seconds:
                                    print("Confirmation element not found after 1 hour")
                                    break
                                try:
                                    confirm_elem = browser.find_element(By.XPATH, "/html/body/main/div/div[2]/div/div[1]/div/div/a")
                                    print("Ok Now Ready")

                                    # After captcha step, open URL from offerurl.txt file on that tab
                                    offer_url = read_url_from_file(r"desk\refer.txt")
                                    if offer_url:
                                        browser.get(offer_url)
                                        print(f"{offer_url}")

                                        # First check if claim is already completed
                                        completed_xpath = "/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[2]/div/span/span"
                                        try:
                                            completed_element = WebDriverWait(browser, 10).until(
                                                EC.visibility_of_element_located((By.XPATH, completed_xpath)) )
                                            if "Completed" in completed_element.text:
                                                print("Claim already completed, skipping claim step")
                                                # Proceed directly to logout
                                                # Click on the next button
                                                next_button_xpath = "/html/body/div[1]/div[2]/nav/div[2]/div[2]/div[2]/div[1]/div/button"
                                                try:
                                                    next_button = WebDriverWait(browser, 30).until(
                                                        EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                                                    )
                                                    next_button.click()
                                                    print("")

                                                    # Click on the logout button using its text "Log Out"
                                                    logout_button_xpath = "//*[text()='Log Out' or .='Log Out']"
                                                    try:
                                                        logout_button = WebDriverWait(browser, 60).until(
                                                            EC.element_to_be_clickable((By.XPATH, logout_button_xpath))
                                                        )
                                                        logout_button.click()
                                                        print("Logout ")

                                                        # Move the key from activekey.txt to usekey.txt before closing the browser
                                                        try:
                                                            active_key_file = "desk/activekey.txt"
                                                            used_key_file = "desk/usekey.txt"
                                                            # Read all keys from activekey.txt
                                                            with open(active_key_file, "r") as akf:
                                                                active_keys = akf.readlines()
                                                            if active_keys:
                                                                used_key = active_keys[0].strip()
                                                                # Write the used key to usekey.txt
                                                                with open(used_key_file, "a") as ukf:
                                                                    ukf.write(used_key + "\n")
                                                                # Remove the used key from activekey.txt
                                                                with open(active_key_file, "w") as akf:
                                                                    akf.writelines(active_keys[1:])
                                                                print(f"Moved key {used_key} from activekey.txt to usekey.txt")
                                                            else:
                                                                print("No active key found to move.")
                                                        except Exception as e:
                                                            print(f"Error moving key from activekey.txt to usekey.txt: {e}")

                                                        # Close the browser
                                                        browser.quit()
                                                        print("Browser closed.")

                                                        # Re-open with new key (recursive call)
                                                        driver_path = chromedriver_paths[0]
                                                        profile_path = chrome_profiles[0]
                                                        url = read_url_from_file("desk/unlocked.txt")
                                                        open_chrome_instance(driver_path, profile_path, 0, url)
                                                        return  # Exit after re-opening

                                                    except Exception as e:
                                                        print(f"Error clicking logout button: {e}")
                                                except Exception as e:
                                                    print(f"Error clicking next button: {e}")
                                                return
                                        except:
                                            pass  # "Completed" not found, proceed with normal claim process

                                        # If claim not completed, proceed with normal claim process
                                        # Wait for the offer button to become clickable and click it
                                        offer_button_xpath = "/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[2]/button[2]"
                                        try:
                                            offer_button = WebDriverWait(browser, 3600).until(
                                                EC.element_to_be_clickable((By.XPATH, offer_button_xpath))
                                            )
                                            offer_button.click()
                                            print("Claim Button Click")
                                            # Wait for claim confirmation element to appear (just check visibility, no click needed)
                                            claim_confirm_xpath = "/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[3]/div/a"
                                            try:
                                                claim_confirm = WebDriverWait(browser, 60).until(
                                                    EC.visibility_of_element_located((By.XPATH, claim_confirm_xpath)))
                                                print("Claim confirm")
                                                # After confirmation, click on the next button
                                                next_button_xpath = "/html/body/div[1]/div[2]/nav/div[2]/div[2]/div[2]/div[1]/div/button"
                                                try:
                                                    next_button = WebDriverWait(browser, 30).until(
                                                        EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                                                    )
                                                    next_button.click()
                                                    print("")

                                                    # Click on the logout button using its text "Log Out"
                                                    logout_button_xpath = "//*[text()='Log Out' or .='Log Out']"
                                                    try:
                                                        logout_button = WebDriverWait(browser, 60).until(
                                                            EC.element_to_be_clickable((By.XPATH, logout_button_xpath)))
                                                        logout_button.click()
                                                        print("Logout ")

                                                        # Move the key from activekey.txt to usekey.txt before closing the browser
                                                        try:
                                                            active_key_file = "desk/activekey.txt"
                                                            used_key_file = "desk/usekey.txt"
                                                            # Read all keys from activekey.txt
                                                            with open(active_key_file, "r") as akf:
                                                                active_keys = akf.readlines()
                                                            if active_keys:
                                                                used_key = active_keys[0].strip()
                                                                # Write the used key to usekey.txt
                                                                with open(used_key_file, "a") as ukf:
                                                                    ukf.write(used_key + "\n")
                                                                # Remove the used key from activekey.txt
                                                                with open(active_key_file, "w") as akf:
                                                                    akf.writelines(active_keys[1:])
                                                                print(f"Moved key {used_key} from activekey.txt to usekey.txt")
                                                            else:
                                                                print("No active key found to move.")
                                                        except Exception as e:
                                                            print(f"Error moving key from activekey.txt to usekey.txt: {e}")

                                                        # Close the browser
                                                        browser.quit()
                                                        print("Browser closed.")

                                                        # Re-open with new key (recursive call)
                                                        driver_path = chromedriver_paths[0]
                                                        profile_path = chrome_profiles[0]
                                                        url = read_url_from_file("desk/unlocked.txt")
                                                        open_chrome_instance(driver_path, profile_path, 0, url)
                                                        return  # Exit after re-opening

                                                    except Exception as e:
                                                        print(f"Error clicking logout button: {e}")
                                                except Exception as e:
                                                    print(f"Error clicking next button: {e}")

                                            except Exception as e:
                                                print(f"Error waiting for claim confirmation: {e}")
                                        except Exception as e:
                                            print(f"Error clicking claim button: {e}")
                                    else:
                                        print("No offer URL found in refer.txt")
                                    break
                                except Exception:
                                    print("Waiting for confirmation element...")
                                    # --- Begin: Retry login and sign flow ---
                                    time.sleep(5)  # Wait before retrying
                                    # Refresh the page to retry the login/sign flow
                                    browser.refresh()
                                    try:
                                        login_btn_xpath = "//button[contains(., 'Log in with Wallet')]"
                                        login_btn = WebDriverWait(browser, 10).until(
                                            EC.element_to_be_clickable((By.XPATH, login_btn_xpath))
                                        )
                                        login_btn.click()
                                        time.sleep(2)  # Wait for the button click to register
                                        print("Clicked 'Log in with Wallet' button.")
                                        # Wait for and click the "Rainbow" button by its text
                                        rainbow_btn_xpath = "//button[contains(., 'Rainbow')]"
                                        rainbow_btn = WebDriverWait(browser, 10).until(
                                            EC.element_to_be_clickable((By.XPATH, rainbow_btn_xpath))
                                        )
                                        rainbow_btn.click()
                                        print("Clicked 'Rainbow' button.")

                                        # Open a new tab and switch to it
                                        browser.execute_script("window.open('');")
                                        browser.switch_to.window(browser.window_handles[-1])
                                        print("Opened and switched to new tab.")

                                        # Open the extension approval page in the new tab
                                        approval_url = "chrome-extension://opfgelmcmbiajamepnmloijbpoleiama/popup.html"
                                        browser.get(approval_url)
                                        print("Opened approval page in new tab.")


                                        # Wait for "Sign" button, reload until available, then click
                                        sign_btn_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/button"
                                        sign_clicked = False
                                        max_attempts = 30
                                        for attempt in range(max_attempts):
                                            try:
                                                sign_btn = WebDriverWait(browser, 5).until(
                                                    EC.element_to_be_clickable((By.XPATH, sign_btn_xpath))
                                                )
                                                sign_btn.click()
                                                print("Clicked 'Sign' button.")
                                                sign_clicked = True

                                                # Wait for the success message to appear
                                                success_msg_xpath = "/html/body/div/div/div/div/div[2]/div/div[1]/div/div/div/div[2]"
                                                WebDriverWait(browser, 10).until(
                                                    EC.visibility_of_element_located((By.XPATH, success_msg_xpath))
                                                )
                                                print("Success message appeared.")
                                                #close the new tab after successful click
                                                browser.close()  # Close the new tab
                                                # Just switch back to the main tab, do not close the browser
                                                browser.switch_to.window(browser.window_handles[0])
                                                print("Switched back to main tab.")
                                                break  # Exit the loop after successful click
                                            except Exception as e:
                                                print(f"'Sign' button not found or not clickable (attempt {attempt+1}/{max_attempts})")
                                                browser.refresh()
                                                time.sleep(1)
                                        if not sign_clicked:
                                            print("'Sign' button not found after multiple reloads.")
                                    except Exception as e:
                                        print(f"Captcha Alredy Solved")
                                    # --- End: Retry login and sign flow ---
                                time.sleep(1)

                        except Exception as e:
                            print(f"Button not found or not clickable: ")
                    else:
                        print("No login URL found in desk/loginurl.txt.")
                except Exception as e:
                    print(f"Wallet unlock confirmation not detected: ")

        except Exception as e:
            print(f"SVG (wallet unlocked confirmation) not found or import failed:")



# Example usage (uncomment to run)
if __name__ == "__main__":
    driver_path = chromedriver_paths[0]
    profile_path = chrome_profiles[0]
    url = read_url_from_file("desk/unlocked.txt")
    open_chrome_instance(driver_path, profile_path, 0, url)

    # Prevent the script from closing the browser automatically
    input("Press Enter to exit and close the browser...")
