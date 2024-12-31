import os

def execute_command(command):
    result = os.popen(command).read()
    return result

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    output = execute_command(user_input)
    print(f"Termux: {output}")