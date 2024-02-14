import subprocess
import sys
import re


# Définition des variables
hostname = 'IP-VM-Ubuntu'
username = 'XXXXX'
password = 'XXXXX'
db_name = 'XXXXX'
db_user = 'XXXXX'
db_password = 'XXXXX'
wp_admin_user = 'XXXXX'
wp_admin_password = 'XXXXX'
wp_url = 'http://ip-vm-ubuntu'
#wp_url = 'http://xxx.com'

# Afficher le contenu des variables de la commande
print("Contenu des variables de la commande configure_db_cmd :")
print(f"db_name : {db_name}")
print(f"db_user : {db_user}")
print(f"db_password : {db_password}")

def validate_input(text):
    # Valide une entrée de texte pour s'assurer qu'elle ne contient que des caractères alphanumériques, des tirets et des points.
    return re.match(r'^[a-zA-Z0-9.-]+$', text) is not None

def validate_url(url):
    # Valide une URL, y compris les adresses IP et les noms de domaine
    return re.match(r'^(http|https)://(?:www\.)?(\w+\.\w{2,}|(?:\d{1,3}\.){3}\d{1,3})$', url) is not None


# Ajoutez des messages de journalisation
def log_info(message):
    print(f"[INFO] {message}")

def log_error(message):
    print(f"[ERROR] {message}")

# Vérification des dépendances et installation si nécessaire
def check_dependencies():
    try:
        import paramiko
    except ImportError:
        print("Paramiko library is not installed. Installing...")
        # Exécutez cette commande avec sudo
        subprocess.run(["sudo", sys.executable, "P6_InstallDependencies.py"])

def configure_apache_virtualhost(domain, document_root):
    # Lecture du modèle de configuration Apache
    with open('template_virtualhost.conf', 'r') as f:
        template = f.read()

    # Remplacement des marqueurs de substitution par les valeurs spécifiques
    config = template.replace('{{DOMAIN}}', domain)
    config = config.replace('{{DOCUMENT_ROOT}}', document_root)

    # Écriture de la configuration dans un fichier
    with open('/etc/apache2/sites-available/{}.conf'.format(domain), 'w') as f:
        f.write(config)

    # Activation du site
    subprocess.run(['a2ensite', domain])

    # Redémarrage du service Apache
    subprocess.run(['systemctl', 'restart', 'apache2'])
def install_wp_cli():
    try:
        # Télécharger le script d'installation de WP-CLI
        subprocess.run("curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar", shell=True, check=True)
        
        # Rendre le script exécutable
        subprocess.run("chmod +x wp-cli.phar", shell=True, check=True)
        
        # Déplacer le script dans un répertoire accessible
        subprocess.run("sudo mv wp-cli.phar /usr/local/bin/wp", shell=True, check=True)
        
        print("WP-CLI installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Appel de la fonction install_wp_cli pour installer WP-CLI
install_wp_cli()

# Fonction pour installer curl
def install_curl():
    try:
        print("Installing curl...")
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'curl'], check=True)
        print("curl installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing curl: {e}")

# Appeler la fonction d'installation de curl
install_curl()

def create_database_if_not_exists(db_name):
    try:
        # Commande pour vérifier si la base de données existe
        check_db_cmd = f"sudo mysql -e 'SHOW DATABASES;' | grep -o '{db_name}'"

        # Exécuter la commande et capturer la sortie
        result = subprocess.run(check_db_cmd, shell=True, capture_output=True)

        # Vérifier si la base de données existe en vérifiant la sortie de la commande
        if db_name in result.stdout.decode():
            print(f"The database '{db_name}' exists. Removing it...")

            # Commande pour supprimer la base de données
            remove_db_cmd = f"sudo mysql -e 'DROP DATABASE IF EXISTS {db_name};'"
            subprocess.run(remove_db_cmd, shell=True, check=True)

            print(f"The database '{db_name}' has been successfully removed.")
        else:
            print(f"The database '{db_name}' does not exist.")
    except subprocess.CalledProcessError as e:
        print(f"Error while checking or removing database: {e}")

def remove_database_if_exists(db_name):
    try:
        # Vérifier si la base de données existe
        check_db_cmd = f'sudo mysql -e "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = \'{db_name}\';"'
        result = subprocess.run(check_db_cmd, shell=True, capture_output=True)
        
        # Si la base de données existe, la supprimer
        if db_name in result.stdout.decode():
            print(f"The database '{db_name}' exists. Removing it...")
            remove_db_cmd = f"sudo mysql -e 'DROP DATABASE {db_name};'"
            subprocess.run(remove_db_cmd, shell=True, check=True)
            print(f"The database '{db_name}' has been successfully removed.")
        else:
            print(f"The database '{db_name}' does not exist.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
 

def db_setup(db_name, db_user, db_password):
    """
    Configure la base de données avec les informations fournies.
    """
    try:
        # Commande pour créer la base de données si elle n'existe pas
        subprocess.run([
            "sudo", "mysql", "-e", f"CREATE DATABASE IF NOT EXISTS {db_name};"
        ], check=True)

        # Commande pour créer l'utilisateur de la base de données
        subprocess.run([
            "sudo", "mysql", "-e",
            f"CREATE USER '{db_user}'@'localhost' IDENTIFIED WITH mysql_native_password BY '{db_password}';"
        ], check=True)

        # Commande pour accorder tous les privilèges à l'utilisateur sur la base de données
        subprocess.run([
            "sudo", "mysql", "-e",
            f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'localhost' WITH GRANT OPTION;"
        ], check=True)

        # Commande pour recharger les privilèges
        subprocess.run([
            "sudo", "mysql", "-e", "FLUSH PRIVILEGES;"
        ], check=True)

        print("Database setup completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def install_wordpress(hostname, username, password, db_name, db_user, db_password, wp_admin_user, wp_admin_password, wp_url):
    try:
        # Appeler la fonction pour créer la base de données si elle n'existe pas
        create_database_if_not_exists('wordpress_db')

        # Supprimer la base de données si elle existe déjà
        remove_database_if_exists('wordpress_db')

        # Installer MySQL/MariaDB si ce n'est pas déjà fait
        # Vérifier si MySQL/MariaDB est déjà installé
        check_mysql_cmd = ['dpkg', '-l', 'mysql-server']
        result = subprocess.run(check_mysql_cmd, capture_output=True)
        
        # Si MySQL/MariaDB n'est pas installé, l'installer
        if 'mysql-server' not in result.stdout.decode():
            print("MySQL/MariaDB is not installed. Installing it...")
            install_mysql_cmd = ['sudo', 'apt-get', 'update']
            install_mysql_cmd2 = ['sudo', 'apt-get', 'install', '-y', 'mysql-server']
            subprocess.run(install_mysql_cmd, check=True)
            subprocess.run(install_mysql_cmd2, check=True)
            print("MySQL/MariaDB has been installed successfully.")
        else:
            print("MySQL/MariaDB is already installed.")
        
                
        #Configure la base de données avec les informations fournies. 
        db_setup(db_name, db_user, db_password)
                
        # Installer Apache, PHP et autres dépendances
        install_dependencies_cmd = ['sudo', 'apt-get', 'install', '-y', 'apache2', 'php', 'libapache2-mod-php', 'php-mysql']
        subprocess.run(install_dependencies_cmd, check=True)

        # Télécharger et installer WordPress
        download_wp_cmd = 'wget https://wordpress.org/latest.tar.gz && tar -xzvf latest.tar.gz'
        install_wp_cmd = f"sudo cp -R wordpress/* /var/www/html/ && sudo chown -R www-data:www-data /var/www/html/ && sudo chmod -R 755 /var/www/html/"
        subprocess.run(download_wp_cmd + ' && ' + install_wp_cmd, shell=True, check=True)

        # Configurer WordPress
        wp_config_cmd = f"sudo cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php && sudo sed -i 's/database_name_here/{db_name}/' /var/www/html/wp-config.php && sudo sed -i 's/username_here/{db_user}/' /var/www/html/wp-config.php && sudo sed -i 's/password_here/{db_password}/' /var/www/html/wp-config.php"
        subprocess.run(wp_config_cmd, shell=True, check=True)

        # Configurer les permissions
        set_permissions_cmd = 'sudo find /var/www/html/ -type d -exec chmod 755 {} \; && sudo find /var/www/html/ -type f -exec chmod 644 {} \;'
        subprocess.run(set_permissions_cmd, shell=True, check=True)

        # Ajouter les informations de l'administrateur WordPress
        wp_admin_cmd = f"sudo -u www-data wp --path=/var/www/html/ core install --url={wp_url} --title='My WordPress Site' --admin_user={wp_admin_user} --admin_password={wp_admin_password} --admin_email=nohas1967@gmail.com"
        subprocess.run(wp_admin_cmd, shell=True, check=True)

        print("WordPress installation completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")



# Vérification des dépendances et installation si nécessaire
check_dependencies()

# Validation des entrées
if not all(map(validate_input, [hostname, db_name, db_user, wp_admin_user])):
    log_error("Invalid input. Please check your hostname, database name, database user, and WordPress admin user.")
    sys.exit(1)

if not validate_url(wp_url):
    log_error("Invalid WordPress URL.")
    sys.exit(1)
    

# Installation de WordPress
install_wordpress(
    hostname='localhost',
    username='root',
    password='root_password',
    db_name='wordpress_db',
    db_user='wordpress_user',
    db_password='user_password',
    wp_admin_user='admin',
    wp_admin_password='admin_password',
    wp_url='http://localhost'
)

