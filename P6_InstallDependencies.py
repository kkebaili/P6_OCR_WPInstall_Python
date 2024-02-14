# P6_InstallDependencies.py

import subprocess
import sys

def install_python():
    print("Python is required. Installing...")
    subprocess.run(["apt", "update"])
    subprocess.run(["apt", "install", "-y", "python3"])

def install_paramiko():
    print("Paramiko library is required. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "paramiko"])

def main():
    install_python()
    install_paramiko()

if __name__ == "__main__":
    main()