import click
from flask.cli import AppGroup

from main import bcrypt, db
from models.gardenplants import GardenPlant
from models.gardens import Garden
from models.plants import Plant
from models.users import User

db_commands = AppGroup("db")


def create_db():
    """Creates all database tables."""
    db.create_all()


@db_commands.command("create")
def create_db_command():
    """Creates all database tables."""
    create_db()
    click.echo(click.style("✨ All tables created. ✨", fg="green", bold=True))


def seed_db():
    """Seed the database with test data."""
    user1 = User(
        full_name="First Test Expert", email="test_expert@email.com", expert=True
    )
    user1.password = bcrypt.generate_password_hash("expert").decode("utf-8")

    user2 = User(full_name="First Test User", email="test_user@email.com", expert=False)
    user2.password = bcrypt.generate_password_hash("usseerr").decode("utf-8")

    user3 = User(
        full_name="Second Test User", email="test_user_2@email.com", expert=False
    )
    user3.password = bcrypt.generate_password_hash("usseerr").decode("utf-8")

    # This database query adds all of the above users to the database, and commits.
    # Committing essentially "saves" the action of the database.
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    expert_garden1 = Garden(creation_date="2023-01-01", garden_type="inside", user_id=1)
    expert_garden2 = Garden(
        creation_date="2023-03-03", garden_type="outside", user_id=1
    )
    user_garden = Garden(creation_date="2020-02-02", garden_type="terrarium", user_id=2)

    # This database query adds all of the above gardens to the database, and commits.
    # Committing essentially "saves" the action of the database.
    db.session.add_all([expert_garden1, expert_garden2, user_garden])
    db.session.commit()

    plant1 = Plant(
        name="aloe vera",
        common_name=["aloe", "chinese aloe"],
        cycle="perennial",
        watering="minimal",
    )
    plant2 = Plant(
        name="dracaena trifasciata",
        common_name=["snake plant"],
        cycle="biennial",
        watering="frequent",
    )

    # This database query adds all of the above plants to the database, and commits.
    db.session.add_all([plant1, plant2])
    db.session.commit()

    garden_plant_1 = GardenPlant(
        last_watered="2021-01-01",
        placement="sunshine",
        healthiness=5,
        garden_id=1,
        plant_id=1,
    )

    garden_plant_2 = GardenPlant(
        last_watered="2023-02-01",
        placement="inside",
        healthiness=10,
        garden_id=1,
        plant_id=1,
    )

    garden_plant_3 = GardenPlant(
        last_watered="2019-11-01",
        placement="sunshine",
        healthiness=7,
        garden_id=2,
        plant_id=2,
    )

    garden_plant_4 = GardenPlant(
        last_watered="2021-01-01",
        placement="indoors",
        healthiness=2,
        garden_id=3,
        plant_id=1,
    )
    # This database query adds all of the above garden plants to the database, and commits.
    db.session.add_all([garden_plant_1, garden_plant_2, garden_plant_3, garden_plant_4])
    db.session.commit()


@db_commands.command("seed")
def seed_db_command():
    seed_db()
    click.echo(
        click.style("🌱 All tables seeded. 🌱", fg="green", bold=True, italic=True)
    )


def delete_db():
    """Deletes all database tables."""
    db.drop_all()


@db_commands.command("drop")
def delete_db_command():
    delete_db()
    click.echo(click.style("🗑️ All tables dropped. 🗑️", fg="red", bold=True))
