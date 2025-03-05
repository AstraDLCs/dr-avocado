from agno.storage.agent.sqlite import SqliteAgentStorage

def load_social_media_storage():
    storage=SqliteAgentStorage(
        table_name="social_media_sessions",
        db_file= './storage/social_sessions.db'
    )
    return storage