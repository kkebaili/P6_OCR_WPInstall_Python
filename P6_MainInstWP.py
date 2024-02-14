import os
import subprocess

def is_wordpress_installed():
    return os.path.exists("/var/www/html/wordpress")

def main():
    if is_wordpress_installed():
        print("WordPress is already installed. Performing clean uninstallation...")
        subprocess.run(["sudo", "python3", "P6_UninstallWPython.py"])
    else:
        print("WordPress is not installed. Proceeding with installation...")
        subprocess.run(["sudo", "python3", "P6_InstallWP.py"])

if __name__ == "__main__":
    main()