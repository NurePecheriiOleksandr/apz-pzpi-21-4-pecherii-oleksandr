import os
import subprocess
from datetime import datetime

def get_backup_directory():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    app_directory = os.path.dirname(script_directory)
    backup_directory = os.path.join(app_directory, 'backups')
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
    return backup_directory

def backup_database(host, port, database, user, password):
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_directory = get_backup_directory()
        backup_file = os.path.join(backup_directory, f'backup_{timestamp}.sql')

        # Full path to pg_dump executable
        pg_dump_path = 'C:\\Program Files\\PostgreSQL\\16\\bin\\pg_dump.exe'

        # Command to perform schema and data backup using pg_dump
        pg_dump_command = [
            pg_dump_path,
            '-h', host,
            '-p', port,
            '-U', user,
            '-d', database,
            '-Fc',
            '-f', backup_file
        ]

        subprocess.run(pg_dump_command, check=True)

        print(f"Backup successful. Backup file saved as: {backup_file}")

    except subprocess.CalledProcessError as error:
        print("Error while backing up PostgreSQL database:", error)
