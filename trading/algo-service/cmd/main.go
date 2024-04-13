package main

import (
	algoservice "algo-service"
	"log"
)

func main() {
	repo := algoservice.NewDatabase("host=localhost port=5432 user=postgres password=123 dbname=postgres sslmode=disable")
	err := repo.Connect()
	if err != nil {
		log.Fatal(err)
	}

	consumer := algoservice.NewConsumer(repo)
	consumer.Run()
}
