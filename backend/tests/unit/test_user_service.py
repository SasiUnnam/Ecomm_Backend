from app.controllers.user_controller import create_user, get_user, update_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def test_create_user_persists_and_hashes_password(db_session):
    payload = UserCreate(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        password="StrongPass123!",
        role="user",
        phone="+123456789",
    )

    user = create_user(payload, db_session)

    assert user.email == "jane@example.com"
    assert user.password_hash is not None
    assert db_session.query(User).filter_by(email="jane@example.com").count() == 1


def test_update_user_changes_email_and_fields(db_session):
    created = create_user(
        UserCreate(
            first_name="John",
            last_name="Smith",
            email="john@example.com",
            password="StrongPass123!",
            role="user",
        ),
        db_session,
    )

    updated = update_user(
        created.id,
        UserUpdate(first_name="Updated", email="updated@example.com", is_active=False),
        db_session,
    )

    assert updated.first_name == "Updated"
    assert updated.email == "updated@example.com"
    assert updated.is_active is False
    assert get_user(created.id, db_session).email == "updated@example.com"
