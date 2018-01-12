CREATE TABLE User (
  id        INTEGER PRIMARY KEY,  -- Discord的ID号
  username  VARCHAR(32),
  nickname  VARCHAR(32),
  time      DATETIME              -- Discord的加入时间
);

CREATE TABLE Tag (
  id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(32)
);

CREATE TABLE User_Tag (
  uid  INTEGER REFERENCES User(id),
  tid  INTEGER REFERENCES Tag(id),
  PRIMARY KEY (uid, tid)
);

CREATE TABLE Question (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  uid     INTEGER REFERENCES User(id),
  content TEXT,
  time    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE KeyWord (
  id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(32)
);

CREATE TABLE Question_KeyWord (
  qid  INTEGER REFERENCES Question(id),
  kwid INTEGER REFERENCES KeyWord(id),
  PRIMARY KEY (qid, kwid)
);

CREATE TABLE Answer (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  uid     INTEGER REFERENCES User(id),
  qid     INTEGER REFERENCES Question(id),
  content TEXT,
  time    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
