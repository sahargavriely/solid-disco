class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = int(user_id)
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f"Thought(user_id={self.user_id!r}, " \
                f"timestamp={self.timestamp!r}, " \
                f"thought={self.thought!r})"

    def __str__(self):
        return f"[{self.timestamp}] user {self.user_id}: {self.thought}"

    def __eq__(self, other):
        return isinstance(other, Thought) and \
                self.user_id == other.user_id and \
                self.timestamp == other.timestamp and \
                self.thought == other.thought

    def serialize(self):
        from struct import pack
        thought = self.thought.encode("utf-8")
        return pack(f"<QQI{len(thought)}s", self.user_id,
                    int(self.timestamp.strftime("%s")), len(thought), thought)

    @classmethod
    def deserialize(cls, data):
        from struct import unpack
        user_id, timestamp, thought_len = unpack("<QQI", data[:20])
        thought = unpack(f"<{thought_len}s", data[20:])[0].decode('utf-8')
        from datetime import datetime
        return Thought(user_id, datetime.fromtimestamp(timestamp), thought)
