package algo_service

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/IBM/sarama"
	"log"
	"time"
)

type Consumer struct {
	config *sarama.Config
	client sarama.Consumer
	repo   *Database
}

func NewConsumer(db *Database) *Consumer {
	config := sarama.NewConfig()
	config.Consumer.Return.Errors = true

	consumer, err := sarama.NewConsumer([]string{"localhost:9092"}, config)
	if err != nil {
		log.Fatalf("Error creating consumer: %v", err)
	}

	c := &Consumer{
		config: config,
		client: consumer,
		repo:   db,
	}

	return c
}

func (c *Consumer) Run() {
	c.config.Consumer.Return.Errors = true

	partitions, err := c.client.Partitions("test-topic")
	if err != nil {
		log.Fatalf("Error fetching partitions: %v", err)
	}

	for _, partition := range partitions {
		partitionConsumer, err := c.client.ConsumePartition("test-topic", partition, sarama.OffsetOldest)
		if err != nil {
			log.Fatalf("Error creating partition consumer: %v", err)
		}

		for msg := range partitionConsumer.Messages() {
			//log.Printf("Received message: %s", msg.Value)
			go c.handleMessage(msg.Value)
		}
	}
}

type CurrencyPrices struct {
	Curr1  string             `json:"curr_1"`
	Curr2  string             `json:"curr_2"`
	Prices map[string]float64 `json:"Prices"`
}

func (c *Consumer) handleMessage(msg []byte) {
	fmt.Println("MSG: ", string(msg))

	var data CurrencyPrices
	err := json.Unmarshal(msg, &data)
	if err != nil {
		log.Println(string(msg))
		log.Println("Error parsing message:", err)
		log.Println()
		return
	}

	calculatedMean := CalculateMean(data)

	fmt.Println("\n --- New Message")
	fmt.Println(calculatedMean)

	ctx, _ := context.WithTimeout(context.Background(), 5*time.Second)
	go c.repo.AddPrice(ctx, calculatedMean)
}
