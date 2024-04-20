package org.example.kafka_producer

import org.apache.kafka.clients.producer.KafkaProducer
import java.util.*

class KafkaProducer {
    private val properties by lazy {
        Properties().apply {
            put("bootstrap.servers", "localhost:9092")
            put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
            put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
        }
    }

    val producer by lazy { KafkaProducer<String, String>(properties) }
}