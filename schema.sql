DROP TABLE IF EXISTS budgets;
CREATE TABLE budgets
(
    budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    progress DECIMAL NOT NULL,
    goal DECIMAL NOT NULL,
    deadline INTEGER,
    releaseDate DATE NOT NULL,
    currentDate DATE ,
    deadlineDate DATE,
    completed BOOLEAN,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    joinDate DATE NOT NULL
);

SELECT * From budgets;

Delete From budgets
WHERE name = 'Dog';

SELECT * FROM budgets
ORDER BY progress;