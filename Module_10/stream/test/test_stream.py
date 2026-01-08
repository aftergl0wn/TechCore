from app.kafka.stream import app, book_views_topic, views_table


def test_faust():
    assert "analytics-streaming" in app.label
    assert book_views_topic.get_topic_name() == "book_views"
    assert views_table.name == "views_count"
    assert "count_views" in list(app.agents.keys())[0]
