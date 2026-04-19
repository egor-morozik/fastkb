class Settings:
    db_path = "fastkb.db"
    memory_mode = False
    search_limit = 5
    batch_size = 200

    def configure(self, memory=False, limit=5):
        self.db_path = ":memory:" if memory else "fastkb.db"
        self.memory_mode = memory
        self.search_limit = int(limit)


config = Settings()
