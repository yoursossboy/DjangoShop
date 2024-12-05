import os
import subprocess
import sys

PREFIX = "[DJANGO_SHOP]"
INFO_MESSAGE = f"INFO : {PREFIX}"
WARNING_MESSAGE = f"WARNING : {PREFIX}"
ERROR_MESSAGE = f"ERROR : {PREFIX}"

SUPERUSER_NAME = "admin"
SUPERUSER_EMAIL = ""
SUPERUSER_PASSWORD = "123"

def install_requirements():
    """Устанавка зависимостей из requirements.txt."""

    print(INFO_MESSAGE, "Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print(INFO_MESSAGE, "Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(ERROR_MESSAGE, f"Failed to install requirements: {e}")
        sys.exit(1)

def run_django_commands(project_dir: str):
    """Выполнение команд Django."""

    print(INFO_MESSAGE, "Running Django commands...")
    
    # Проверка, установлен ли Django
    try:
        import django
    except ImportError:
        print(ERROR_MESSAGE, "Django is not installed. Please check requirements installation.")
        sys.exit(1)
    
    try:
        # Применение миграций
        subprocess.check_call([sys.executable, "manage.py", "migrate"], cwd=project_dir)
        print(INFO_MESSAGE, "Migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        print(ERROR_MESSAGE, f"Failed to run migrations: {e}")
        sys.exit(1)

def create_superuser(project_dir):
    """Создание суперпользователя, если он еще не существует."""

    print(INFO_MESSAGE, "Creating superuser...")
    import django
    from django.conf import settings

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")
    sys.path.append(project_dir)
    django.setup()

    from django.contrib.auth import get_user_model

    User = get_user_model()
    username = SUPERUSER_NAME
    email = SUPERUSER_EMAIL
    password = SUPERUSER_PASSWORD

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(INFO_MESSAGE, f"Superuser '{username}' created successfully.")
    else:
        print(WARNING_MESSAGE, f"Superuser '{username}' already exists.")

if __name__ == "__main__":
    # Проверка, есть ли requirements.txt
    if not os.path.exists("requirements.txt"):
        print(ERROR_MESSAGE, "requirements.txt not found. Please ensure the file exists in the current directory.")
        sys.exit(1)

    # Устанавка зависимостей
    install_requirements()

    # Проверка, существует ли папка проекта Django
    project_dir = "myshop"
    manage_py_path = os.path.join(project_dir, "manage.py")
    if not os.path.exists(manage_py_path):
        print(ERROR_MESSAGE, f"manage.py not found in {project_dir}. Please ensure you are in the correct project structure.")
        sys.exit(1)

    # Выполнение миграций и создание суперпользователя
    run_django_commands(project_dir)
    create_superuser(project_dir)

    print(INFO_MESSAGE, "Setup completed successfully!")