from celery_app import celery_app


def test_celery():
    assert celery_app.main == "app"
