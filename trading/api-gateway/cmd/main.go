package main

import (
	api_gateway "api-gateway"
	"fmt"
	"io"
	"net/http"
	"time"
)

func main() {
	producer := api_gateway.NewProducer()
	producer.Run()

	url := "http://localhost:8080/binance?curr1=btc&curr2=usdt&from=2024-04-10T15:04:05Z&to=2024-04-10T15:04:25Z"
	for {
		resp, err := http.Get(url)
		if err != nil {
			fmt.Println("Error:", err)
			return
		}

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			fmt.Println("Error reading response body:", err)
			return
		}

		fmt.Println("Response Body:", string(body))
		producer.SendMessage("test-topic", string(body))

		time.Sleep(3 * time.Second)
	}
}
