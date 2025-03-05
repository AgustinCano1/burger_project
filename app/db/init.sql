-- Habilitar claves foráneas en SQLite
PRAGMA foreign_keys = ON;

-- Table of Burgers
CREATE TABLE BURGER (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    active INTEGER DEFAULT 1
);

-- Table of Ingredients
CREATE TABLE INGREDIENTS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    active INTEGER DEFAULT 1
);

-- Intermediate Table: Ingredients of each Burger
CREATE TABLE BURGERS_INGREDIENTS (
    id TEXT NOT NULL,
    burger_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    PRIMARY KEY (id),
    FOREIGN KEY (burger_id) REFERENCES BURGER(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES INGREDIENTS(id) ON DELETE CASCADE
);

-- Table of Promotions
CREATE TABLE PROMOTIONS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    burger_id INTEGER NOT NULL,
    discount REAL NOT NULL,
    percentage_discount INTEGER DEFAULT 0,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    FOREIGN KEY (burger_id) REFERENCES BURGER(id) ON DELETE CASCADE
);

-- Table of Stores
CREATE TABLE STORES (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    is_24hrs INTEGER DEFAULT 0,
    has_drive_thru INTEGER DEFAULT 0,
    monday INTEGER DEFAULT 0,
    tuesday INTEGER DEFAULT 0,
    wednesday INTEGER DEFAULT 0,
    thursday INTEGER DEFAULT 0,
    friday INTEGER DEFAULT 0,
    saturday INTEGER DEFAULT 0,
    sunday INTEGER DEFAULT 0
);

-- Intermediate Table: Burgers available in each Store
CREATE TABLE STORES_BURGERS (
    id TEXT NOT NULL,
    store_id INTEGER NOT NULL,
    burger_id INTEGER NOT NULL,
    active INTEGER DEFAULT 1,
    PRIMARY KEY (id),
    FOREIGN KEY (store_id) REFERENCES STORES(id) ON DELETE CASCADE,
    FOREIGN KEY (burger_id) REFERENCES BURGER(id) ON DELETE CASCADE
);
