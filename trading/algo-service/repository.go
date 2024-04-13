package algo_service

import (
	"context"
	_ "github.com/jackc/pgx/v5/stdlib"
)

func (d *Database) AddPrice(ctx context.Context, cm CurrencyMean) {
	query := `
		INSERT INTO prices (curr1, curr2, mean_price, from_time, to_time)
		VALUES ($1, $2, $3, $4, $5)
	`

	_, err := d.DB.Query(query, cm.Curr1, cm.Curr2, cm.MeanPrice, cm.FromTime, cm.ToTime)
	if err != nil {
		return
	}

	return
}
