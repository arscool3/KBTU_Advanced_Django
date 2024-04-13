package algo_service

import "database/sql"

type Database struct {
	DB  *sql.DB
	DSN string
}

func NewDatabase(DSN string) *Database {
	return &Database{
		DSN: DSN,
	}
}

func (d *Database) Connect() error {
	db, err := sql.Open("pgx", d.DSN)
	if err != nil {
		return err
	}

	d.DB = db
	return nil
}

func (d *Database) Close() {
	d.DB.Close()
}

func (d *Database) Query(query string, args ...interface{}) (*sql.Rows, error) {
	return d.DB.Query(query, args...)
}
