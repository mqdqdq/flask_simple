DROP TABLE IF EXISTS rooms;

CREATE TABLE IF NOT EXISTS rooms (
    room_id TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    user_count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (room_id)
);


DROP TABLE IF EXISTS chats;

CREATE TABLE IF NOT EXISTS chats (
    chat_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    room_id TEXT NOT NULL,
    chat_text TEXT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms (room_id)
);