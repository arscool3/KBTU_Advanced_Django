package binance

import (
	"math/rand"
	"time"
)

func init() {
	rand.Seed(time.Now().UnixNano())
}

func randFloat64InRange(min, max float64) float64 {
	return min + rand.Float64()*(max-min)
}
