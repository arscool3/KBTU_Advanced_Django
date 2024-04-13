CREATE TABLE IF NOT EXISTS prices (
      id SERIAL PRIMARY KEY,
      curr1 VARCHAR(255) NOT NULL,
      curr2 VARCHAR(255) NOT NULL,
      mean_price FLOAT NOT NULL,
      from_time TIMESTAMP WITH TIME ZONE NOT NULL,
      to_time TIMESTAMP WITH TIME ZONE NOT NULL
);
