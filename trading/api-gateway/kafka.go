package api_gateway

import (
	"errors"
	"github.com/IBM/sarama"
	"log"
)

type Producer struct {
	config *sarama.Config
	client sarama.AsyncProducer
}

func NewProducer() *Producer {
	return &Producer{
		config: sarama.NewConfig(),
	}
}

func (p *Producer) Run() {
	p.config.Producer.Return.Successes = true

	var err error
	p.client, err = sarama.NewAsyncProducer([]string{"localhost:9092"}, p.config)
	if err != nil {
		log.Fatalf("Error creating producer: %v", err)
	}

	// Prints successes
	go func() {
		for range p.client.Successes() {
			log.Println("Message sent successfully")
		}
	}()

	// Prints errors
	go func() {
		for err := range p.client.Errors() {
			log.Printf("Failed to send message: %v", err)
		}
	}()
}

func (p *Producer) SendMessage(topic, message string) error {
	if p.client == nil {
		return errors.New("producer client is not initialized")
	}

	msg := &sarama.ProducerMessage{
		Topic: "test-topic",
		Value: sarama.StringEncoder(message),
	}

	select {
	case p.client.Input() <- msg:
		return nil
	default:
		return errors.New("failed to send message: producer channel closed")
	}
	return nil
}
