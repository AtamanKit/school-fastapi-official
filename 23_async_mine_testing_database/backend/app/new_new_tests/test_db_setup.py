from app.database import Base


def test_table_presence():
    assert len(Base.metadata.tables) > 0
