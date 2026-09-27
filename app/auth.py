import bcrypt

from app.database import get_connection


def register_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        password_bytes = password.encode("utf-8")

        hashed_password = bcrypt.hashpw(
            password_bytes,
            bcrypt.gensalt()
        )

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            RETURNING id
            """,
            (username, hashed_password.decode("utf-8"))
        )

        user_id = cursor.fetchone()[0]

        connection.commit()

        return {
            "success": True,
            "user_id": user_id
        }

    except Exception:

        connection.rollback()

        return {
            "success": False,
            "message": "Username already exists"
        }

    finally:

        cursor.close()
        connection.close()


def login_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, password
        FROM users
        WHERE username = %s
        """,
        (username,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:

        return {
            "success": False,
            "message": "Invalid username or password"
        }

    stored_password = user[2]

    password_match = bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password.encode("utf-8")
    )

    if password_match:

        return {
            "success": True,
            "user_id": user[0],
            "username": user[1]
        }

    return {
        "success": False,
        "message": "Invalid username or password"
    }