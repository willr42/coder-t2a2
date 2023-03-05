import click
from flask.cli import AppGroup

from main import db

db_commands = AppGroup("db")


@db_commands.command("create")
def create_db():
    """Creates all database tables."""
    db.create_all()
    click.echo(click.style("✨ All tables created. ✨", fg="green", bold=True))


@db_commands.command("drop")
def delete():
    db.drop_all()
    click.echo(click.style("🗑️ All tables dropped. 🗑️", fg="red", bold=True))
