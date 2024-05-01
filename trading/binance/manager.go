package binance

import (
	"errors"
	"time"
)

var (
	ErrNoSuchCurrency = errors.New("no such currency in the binance")
)

type Manager struct {
	currencies map[Currency]PriceRange
}

type Currency struct {
	Name string
}

type PriceRange struct {
	min float64
	max float64
}

func (m Manager) GetCurrencyPrice(c Currency) (float64, error) {
	priceRange, ok := m.currencies[c]
	if !ok {
		return 0, ErrNoSuchCurrency
	}
	return randFloat64InRange(priceRange.min, priceRange.max), nil
}

func (m *Manager) GetPricesInSecondsRange(startTime, endTime time.Time) map[string]float64 {
	duration := int64(endTime.Sub(startTime).Seconds())

	prices := make(map[string]float64)
	for i := int64(0); i < duration; i++ {
		currentTime := startTime.Add(time.Duration(i) * time.Second)
		prices[currentTime.Format(time.RFC3339)] = randFloat64InRange(100.0, 1000.0)
	}

	return prices
}

func NewManager() *Manager {
	return &Manager{
		currencies: make(map[Currency]PriceRange),
	}
}

func NewCurrency(name string) Currency {
	return Currency{Name: name}
}

func NewPriceRange(min, max float64) PriceRange {
	return PriceRange{min: min, max: max}
}
