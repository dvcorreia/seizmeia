CREATE TABLE users (
    id integer,
    username text,
    email text NOT NULL,

    credit integer DEFAULT 0,

    PRIMARY KEY (id),
    UNIQUE (username, email)
);

CREATE TABLE offers (
    id integer,
    issuer integer,
    amount integer NOT NULL,

    FOREIGN KEY (issuer) REFERENCES users(id),
    PRIMARY KEY (id)
);

CREATE TABLE events (
    id integer,
    name text NOT NULL,
    description text,
    issuer integer,

    starting_at timestamp,
    ending_at timestamp,

    max_amount integer,
    max_per_person integer,

    FOREIGN KEY (issuer) REFERENCES users(id),
    PRIMARY KEY (id)
);

CREATE TABLE tab (
    id integer,
    user_id integer,
    amount integer NOT NULL,
    at timestamp DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (id)
);
