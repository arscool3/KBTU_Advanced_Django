package algo_service

import "sort"

type CurrencyMean struct {
	Curr1     string  `json:"curr_1"`
	Curr2     string  `json:"curr_2"`
	MeanPrice float64 `json:"mean_price"`
	FromTime  string  `json:"from_time"`
	ToTime    string  `json:"to_time"`
}

func CalculateMean(data CurrencyPrices) CurrencyMean {
	var sum float64
	count := 0

	for _, price := range data.Prices {
		sum += price
		count++
	}

	mean := sum / float64(count)

	timestamps := make([]string, 0, len(data.Prices))
	for timestamp := range data.Prices {
		timestamps = append(timestamps, timestamp)
	}

	sort.Strings(timestamps)

	fromTime := timestamps[0]
	toTime := timestamps[len(timestamps)-1]

	return CurrencyMean{
		Curr1:     data.Curr1,
		Curr2:     data.Curr2,
		MeanPrice: mean,
		FromTime:  fromTime,
		ToTime:    toTime,
	}
}
