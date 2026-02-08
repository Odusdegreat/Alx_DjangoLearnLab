DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",

        # ✅ Separate test database file
        "TEST": {
            "NAME": BASE_DIR / "test_db.sqlite3",
        },
    }
}
