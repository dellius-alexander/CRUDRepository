"""
Generate a key and IV
>>> openssl enc -aes-256-cbc -k secret -P -md sha1

Encrypt the password
>>> echo -n "yourpassword" | openssl enc -aes-256-cbc -base64 -K <key> -iv <iv>

# Decrypt the password
>>> echo -n "<encrypted_password>" | openssl enc -aes-256-cbc -d -base64 -K <key> -iv <iv>
"""

import subprocess
import re


PASSWORD = "yourpassword"

# Run the openssl command
command = ["openssl", "enc", "-aes-256-cbc", "-k", "secret", "-P", "-md", "sha256"]
result = subprocess.run(command, capture_output=True, text=True)

# Extract the output
output = result.stdout
print(f"Output: \n{output}")
# Parse the output to extract salt, key, and iv
salt = re.search(r"salt=([A-F0-9]+)", output).group(1)
key = re.search(r"key=([A-F0-9]+)", output).group(1)
iv = re.search(r"iv\s+=([A-F0-9]+)", output).group(1)

# Print the variables
print(f"Salt: {salt}")
print(f"Key: {key}")
print(f"IV: {iv}")

# Encrypt the password
command = ["openssl", "enc", "-aes-256-cbc", "-base64", "-K", key, "-iv", iv]
result = subprocess.run(command, input=PASSWORD, capture_output=True, text=True)
encrypted_password = result.stdout
print(f"Encrypted Password: {encrypted_password}")

# Decrypt the password
command = ["openssl", "enc", "-aes-256-cbc", "-d", "-base64", "-K", key, "-iv", iv]
result = subprocess.run(command, input=encrypted_password, capture_output=True, text=True)
decrypted_password = result.stdout
print(f"Decrypted Password: {decrypted_password}")


if __name__ == "__main__":
    pass
