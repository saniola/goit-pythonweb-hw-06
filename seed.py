import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Group, Student, Teacher, Subject, Grade

DATABASE_URL = "postgresql+psycopg2://postgres:dbpassword@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

fake = Faker()


def seed_database():
    session = Session()

    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()

    teachers = [
        Teacher(name=f"{fake.first_name()} {fake.last_name()}") for _ in range(4)
    ]
    session.add_all(teachers)
    session.commit()

    subjects = [
        Subject(name=f"Subject {i}", teacher=random.choice(teachers))
        for i in range(1, 9)
    ]
    session.add_all(subjects)
    session.commit()

    students = [
        Student(
            name=f"{fake.first_name()} {fake.last_name()}",
            group=random.choice(groups),
        )
        for _ in range(50)
    ]
    session.add_all(students)
    session.commit()

    for student in students:
        for _ in range(20):
            grade = Grade(
                student=student,
                subject=random.choice(subjects),
                grade=random.uniform(60, 100),
                date_received=fake.date_between(start_date="-1y", end_date="today"),
            )
            session.add(grade)

    session.commit()
    session.close()


if __name__ == "__main__":
    seed_database()
