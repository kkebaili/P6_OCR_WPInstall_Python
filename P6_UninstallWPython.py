import os
import subprocess

# Définition des variables
hostname = 'IP-VM-Ubuntu'
username = 'XXXXX'
password = 'XXXXX'
db_name = 'XXXXX'
db_user = 'XXXXX'
db_password = 'XXXXX'
wp_admin_user = 'XXXXX'
wp_admin_password = 'XXXXX'
wp_url = 'http://IP-VM-Ubuntu'

def create_user(username, password):
    try:
        # Vérifier si l'utilisateur existe déjà
        check_user_cmd = f"sudo mysql -e 'SELECT User FROM mysql.user WHERE User=\'{username}\' AND Host=\'localhost\';'"
        result = subprocess.run(check_user_cmd, shell=True, capture_output=True, check=True)
        
        if username not in result.stdout.decode():
            # L'utilisateur n'existe pas, donc nous pouvons le créer
            create_user_cmd = f"sudo mysql -e 'CREATE USER \'{username}\'@\'localhost\' IDENTIFIED BY \'{password}\';'"
            grant_privileges_cmd = f"sudo mysql -e 'GRANT ALL PRIVILEGES ON *.* TO \'{username}\'@\'localhost\';'"
            flush_privileges_cmd = "sudo mysql -e 'FLUSH PRIVILEGES;'"
            
            subprocess.run(create_user_cmd, shell=True, check=True)
            subprocess.run(grant_privileges_cmd, shell=True, check=True)
            subprocess.run(flush_privileges_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing MySQL commands: {e}")

def drop_database(database_name):
    # Vérifier si la base de données existe avant de la supprimer
    check_db_cmd = f"sudo mysql -e 'SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = \"{database_name}\";'"
    result = subprocess.run(check_db_cmd, shell=True, capture_output=True)
    
    if database_name in result.stdout.decode():
        # La base de données existe, nous pouvons donc la supprimer
        drop_db_cmd = f"sudo mysql -e 'DROP DATABASE IF EXISTS {database_name};'"
        subprocess.run(drop_db_cmd, shell=True, check=True)
        print(f"Database '{database_name}' has been dropped successfully.")
    else:
        print(f"Database '{database_name}' does not exist.")

def remove_wordpress():
    # Supprimer les fichiers latest.tar.gz.* dans le répertoire /home/ubuntu/Download
    subprocess.run("sudo rm -f /home/ubuntu/Downloads/latest.tar.gz*", shell=True, check=False)

    # Vérifier si le répertoire WordPress existe dans /home/ubuntu/Downloads
    if os.path.exists("/home/ubuntu/Downloads/wordpress"):
        # Le répertoire WordPress existe, nous pouvons le supprimer
        subprocess.run("sudo rm -rf /home/ubuntu/Downloads/wordpress", shell=True, check=True)
        print("WordPress directory has been removed successfully.")
    else:
        print("WordPress directory does not exist.")

    # Supprimer le VirtualHost Apache pour WordPress s'il existe
    subprocess.run("sudo rm -f /etc/apache2/sites-available/000-default.conf", shell=True, check=False)

    # Désactiver le module rewrite Apache s'il est activé
    subprocess.run("sudo a2dismod rewrite", shell=True, check=False)

    # Redémarrer Apache
    subprocess.run("sudo systemctl restart apache2", shell=True, check=False)

    # Supprimer les fichiers WordPress s'ils existent
    subprocess.run("sudo rm -rf /var/www/html/wordpress", shell=True, check=False)


def remove_php():
    # Vérifier si le package PHP est installé
    check_php_cmd = "dpkg-query -l | grep php"
    result = subprocess.run(check_php_cmd, shell=True, capture_output=True)
    
    if result.returncode == 0:
        # Le package PHP est installé, nous pouvons le supprimer
        subprocess.run("sudo apt remove --purge -y php libapache2-mod-php php-mysql", shell=True, check=True)
        print("PHP package has been removed successfully.")
    else:
        print("PHP package is not installed.")

def remove_mysql():
    # Vérifier si MySQL est installé
    check_mysql_cmd = "dpkg-query -l | grep mysql-server"
    result = subprocess.run(check_mysql_cmd, shell=True, capture_output=True)
    
    if result.returncode == 0:
        # MySQL est installé, nous pouvons le supprimer
        subprocess.run("sudo apt remove --purge -y mysql-server", shell=True, check=True)
        subprocess.run("sudo apt autoremove -y", shell=True, check=True)
        subprocess.run("sudo apt autoclean", shell=True, check=True)
        print("MySQL has been removed successfully.")
    else:
        print("MySQL is not installed.")

def main():
    create_user(db_user, db_password)
    drop_database(db_name)
    remove_wordpress()
    remove_php()
    remove_mysql()

    print("WordPress et ses dépendances ont été désinstallés avec succès !")

if __name__ == "__main__":
    main()
