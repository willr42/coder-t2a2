import click
from flask.cli import AppGroup

from main import db
from models.gardens import Garden
from models.gardenplants import GardenPlant
from models.plants import Plant
from models.users import User

db_commands = AppGroup("db")


@db_commands.command("create")
def create_db():
    """Creates all database tables."""
    db.create_all()
    click.echo(click.style("✨ All tables created. ✨", fg="green", bold=True))


@db_commands.command("drop")
def delete():
    """Deletes all database tables."""
    db.drop_all()
    click.echo(click.style("🗑️ All tables dropped. 🗑️", fg="red", bold=True))
