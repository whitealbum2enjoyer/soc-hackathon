-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    JNumber TEXT NOT NULL UNIQUE,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    IsActive INTEGER DEFAULT 1
);

-- Rooms Table
CREATE TABLE IF NOT EXISTS Rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number TEXT NOT NULL UNIQUE,
    floor_level INTEGER NOT NULL,
    capacity INTEGER DEFAULT 6
);

-- Occupancy Table
-- Tracks check-in and check-out events
CREATE TABLE IF NOT EXISTS Occupancy (
    occupancy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    status TEXT NOT NULL, -- 'Checked In' or 'Checked Out'
    check_in_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
);

-- Seed Initial Data
INSERT OR IGNORE INTO Rooms (room_number, floor_level) VALUES ('101', 1);
INSERT OR IGNORE INTO Rooms (room_number, floor_level) VALUES ('201', 2);
INSERT OR IGNORE INTO Rooms (room_number, floor_level) VALUES ('301', 3);
INSERT OR IGNORE INTO Rooms (room_number, floor_level) VALUES ('305', 3);

INSERT OR IGNORE INTO Users (JNumber) VALUES ('J00741314');
INSERT OR IGNORE INTO Users (JNumber) VALUES ('J00773744');
INSERT OR IGNORE INTO Users (JNumber) VALUES ('J00786766');