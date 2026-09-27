from sqlalchemy import Column, Integer, Float, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String, nullable=False)
    intensity = Column(String, nullable=False)


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_user(user_id, username, age, weight, goal, intensity):
    db = SessionLocal()

    try:
        user = User(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()


def save_plan(user_id, original_plan, nutrition_tip):
    db = SessionLocal()

    try:
        plan = Plan(
            user_id=user_id,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip,
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return plan

    finally:
        db.close()


def update_plan(user_id, updated_plan):
    db = SessionLocal()

    try:
        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .order_by(Plan.id.desc())
            .first()
        )

        if plan:
            plan.updated_plan = updated_plan
            db.commit()
            db.refresh(plan)

        return plan

    finally:
        db.close()


def get_original_plan(user_id):
    db = SessionLocal()

    try:
        plan = (
            db.query(Plan)
            .filter(Plan.user_id == user_id)
            .order_by(Plan.id.desc())
            .first()
        )

        return plan.original_plan if plan else None

    finally:
        db.close()


def get_user(user_id):
    db = SessionLocal()

    try:
        return (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

    finally:
        db.close()


def get_all_users():
    db = SessionLocal()

    try:
        return db.query(User).all()

    finally:
        db.close()


def get_all_plans():
    db = SessionLocal()

    try:
        return db.query(Plan).all()

    finally:
        db.close()