from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models import Student, Grade, Subject, Group
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:dbpassword@localhost:5432/postgres"
)


def get_top_students_by_avg_grade(session: Session):
    return (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )


def get_best_student_in_subject(session: Session, subject_id):
    return (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )


def get_avg_grade_by_group_in_subject(session: Session, subject_id):
    return (
        session.query(Group.name, func.avg(Grade.grade).label("average_grade"))
        .select_from(Group)
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )


def get_avg_grade_across_all_students(session: Session):
    return session.query(func.avg(Grade.grade)).scalar()


def get_courses_by_teacher(session: Session, teacher_id):
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()


def get_students_in_group(session: Session, group_name):
    return (
        session.query(Student.name).join(Group).filter(Group.name == group_name).all()
    )


def get_grades_for_group_in_subject(session: Session, group_name, subject_id):
    return (
        session.query(Student.name, Grade.grade, Grade.date_received)
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Group.name == group_name, Grade.subject_id == subject_id)
        .all()
    )


def get_avg_grade_given_by_teacher(session: Session, teacher_id):
    return (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )


def get_courses_attended_by_student(session: Session, student_id):
    return (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )


def get_courses_taught_by_teacher_to_student(session: Session, student_id, teacher_id):
    return (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )


if __name__ == "__main__":
    with Session(engine) as session:
        print(get_top_students_by_avg_grade(session))
        print(get_best_student_in_subject(session, 1))
        print(get_avg_grade_by_group_in_subject(session, 1))
        print(get_avg_grade_across_all_students(session))
        print(get_courses_by_teacher(session, 1))
        print(get_students_in_group(session, "Group 1"))
        print(get_grades_for_group_in_subject(session, "Group 1", 1))
        print(get_avg_grade_given_by_teacher(session, 1))
        print(get_courses_attended_by_student(session, 1))
        print(get_courses_taught_by_teacher_to_student(session, 1, 1))
