DROP TABLE IF EXISTS rooms;

CREATE TABLE IF NOT EXISTS rooms (
    room_id TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    game_content JSON NOT NULL,
    game_type TEXT NOT NULL,
    rematch_requests INTEGER DEFAULT 0 NOT NULL,
    current_users INTEGER DEFAULT 0 NOT NULL,
    room_closed INTEGER DEFAULT 0 NOT NULL,
    PRIMARY KEY (room_id)
);