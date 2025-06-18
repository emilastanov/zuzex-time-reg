from jinja2 import Environment, FileSystemLoader
from nacl import encoding, public
from dotenv import load_dotenv
import subprocess
import requests
import click
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PROJECT_NAME = os.getenv("PROJECT_NAME")
DOCKER_PASS = os.getenv("DOCKER_PASS")
DOCKER_USER = os.getenv("DOCKER_USER")
PROJECT_PATH = os.getenv("PROJECT_PATH")
USERNAME = os.getenv("USERNAME")
HOST = os.getenv("HOST")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR = os.path.join(BASE_DIR, "core", "generator_templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

GITHUB_API = "https://api.github.com"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else None,
    "Accept": "application/vnd.github+json",
}


def get_gh_username():
    url = f"{GITHUB_API}/user"
    resp = requests.get(url, headers=headers)

    return resp.json()["login"]


def get_gh_repo_by_name(repo_full_name):
    url = f"{GITHUB_API}/repos/{repo_full_name}"
    resp = requests.get(url, headers=headers)

    return resp.json(), resp.status_code


def create_repo(repo_name, private=True):
    data = {"name": repo_name, "private": private}
    resp = requests.post(f"{GITHUB_API}/user/repos", json=data, headers=headers)
    if resp.status_code == 201:
        click.echo(f"✅ Репозиторий '{repo_name}' успешно создан.")
    else:
        click.echo(f"❌ Ошибка создания репозитория: {resp.status_code} {resp.text}")


def add_var(name, value):
    if not GITHUB_TOKEN:
        click.echo("❌ GITHUB_TOKEN не задан.")
        return

    username = get_gh_username()

    res = requests.post(
        f"{GITHUB_API}/repos/{username}/{PROJECT_NAME}/actions/variables",
        headers=headers,
        json={"name": name, "value": value},
    )

    if res.status_code in (201, 204):
        click.echo(f"✅ Параметр '{name}' добавлен в '{PROJECT_NAME}'.")
    elif res.status_code == 409:
        requests.patch(
            f"{GITHUB_API}/repos/{username}/{PROJECT_NAME}/actions/variables/{name}",
            headers=headers,
            json={"name": name, "value": value},
        )
        click.echo(f"✅ Параметр '{name}' обновлен в '{PROJECT_NAME}'.")
    else:
        click.echo(f"❌ Ошибка при добавлении параметра: {res.status_code} {res.text}")


def add_secret(secret_name, secret_value):
    """Добавляет секрет в GitHub репозиторий."""
    if not GITHUB_TOKEN:
        click.echo("❌ GITHUB_TOKEN не задан.")
        return

    username = get_gh_username()

    # 1. Получение ключа
    resp = requests.get(
        f"{GITHUB_API}/repos/{username}/{PROJECT_NAME}/actions/secrets/public-key",
        headers=headers,
    )
    if resp.status_code != 200:
        click.echo(f"❌ Ошибка при получении ключа: {resp.status_code} {resp.text}")
        return

    key_data = resp.json()
    public_key = key_data["key"]
    key_id = key_data["key_id"]

    # 2. Шифрование значения
    public_key_obj = public.PublicKey(
        public_key.encode("utf-8"), encoding.Base64Encoder()
    )
    sealed_box = public.SealedBox(public_key_obj)
    encrypted = sealed_box.encrypt(
        secret_value.encode("utf-8"), encoder=encoding.Base64Encoder()
    ).decode("utf-8")

    # 3. Отправляем зашифрованный секрет
    res = requests.put(
        f"{GITHUB_API}/repos/{username}/{PROJECT_NAME}/actions/secrets/{secret_name}",
        headers=headers,
        json={"encrypted_value": encrypted, "key_id": key_id},
    )

    if res.status_code in (201, 204):
        click.echo(f"✅ Секрет '{secret_name}' добавлен в '{PROJECT_NAME}'.")
    else:
        click.echo(f"❌ Ошибка при добавлении секрета: {res.status_code} {res.text}")


@click.group()
def cli():
    pass


@cli.command(name="gen-keyboard")
@click.argument("name")
def gen_keyboard(name):
    """Создать заготовку клавиатуры."""
    keyboard_name = name.lower()

    keyboard_template = env.get_template("keyboard.py.jinja")
    button_handler_template = env.get_template("button_handler.py.jinja")

    rendered = keyboard_template.render(name=keyboard_name)
    handler_rendered = button_handler_template.render()

    output_dir = os.path.join(BASE_DIR, "keyboards")
    handler_output_dir = os.path.join(BASE_DIR, "button_handlers")

    output_path = os.path.join(output_dir, f"{keyboard_name}.py")
    handler_output_path = os.path.join(handler_output_dir, f"{keyboard_name}.py")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    with open(handler_output_path, "w", encoding="utf-8") as f:
        f.write(handler_rendered)

    click.echo("✅ Keyboard template created.")


@cli.command(name="gen-command")
@click.argument("name")
def gen_command(name):
    """Создать заготовку обработчика."""
    command_name = name.lower()

    template = env.get_template("command.py.jinja")
    rendered = template.render(name=command_name)

    output_dir = os.path.join(BASE_DIR, "commands")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{command_name}.py")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    click.echo("✅ Command handler created.")


@cli.command(name="gen-model")
@click.argument("name")
def gen_model(name):
    """Создать модель"""
    model_name = name.capitalize()
    table_name = name.lower() + "s"

    template = env.get_template("model.py.jinja")
    rendered = template.render(name=model_name, table_name=table_name)

    output_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{model_name}.py")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    click.echo(f"✅ Model '{model_name}' created")


@cli.command(name="find-or-create-repo")
def find_repo():
    """Проверяет, существует ли репозиторий в GitHub (формат: owner/repo)"""

    username = get_gh_username()

    repo, code = get_gh_repo_by_name(f"{username}/{PROJECT_NAME}")
    repo_url = f"https://github.com/{username}/{PROJECT_NAME}.git"

    commands = [
        ["git", "branch", "-M", "main"],
        ["git", "remote", "add", "origin", repo_url],
    ]

    if code == requests.codes.NOT_FOUND:
        click.echo(f"❌ Репозиторий '{PROJECT_NAME}' не найден.")
        is_public = click.confirm("Сделать репозиторий публичным?", default=False)
        create_repo(PROJECT_NAME, private=not is_public)
    else:
        click.echo(f"✅ Репозиторий '{PROJECT_NAME}' существует.")

    for cmd in commands:
        click.echo(f"➤ Выполняется: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            click.echo(f"❌ Ошибка: {result.stderr.strip()}")
            break
        else:
            click.echo(f"✅ Успешно: {result.stdout.strip()}")


def send_env():
    with open(".env", "r") as file:
        content = file.read()
        add_secret("ENV", content)


@cli.command(name="sync-env-file")
def sync_env_file():
    send_env()


@cli.command(name="send-secrets")
def send_secrets():
    send_env()
    add_secret("DOCKER_USER", DOCKER_USER)
    add_secret("DOCKER_PASS", DOCKER_PASS)

    with open(".ssh_key", "r") as file:
        content = file.read()
        add_secret("SSH_PRIVATE_KEY", content)

    add_var("PROJECT_PATH", PROJECT_PATH)
    add_var("USERNAME", USERNAME)
    add_var("HOST", HOST)


if __name__ == "__main__":
    cli()
