package org.example

import io.ktor.client.request.*
import io.ktor.http.*
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.apache.kafka.clients.producer.ProducerRecord
import org.example.http_client.HttpClientWrapper
import org.example.kafka_producer.KafkaProducer
import org.example.models.CurrencyCourse
import kotlin.time.Duration.Companion.minutes

class App {
}

fun main() {

    val client = HttpClientWrapper()
    val producer = KafkaProducer()
    // Coroutine scope for asynchronous programming
    runBlocking {
        endlessFlow().map {
            getRates(client)
        }.map {
            submitToProducer(producer, it)
        }.launchIn(this)
    }
}

suspend fun getRates(client: HttpClientWrapper): CurrencyCourse{
    return client.httpClient.get<CurrencyCourse>{
        url("http://127.0.0.1:8080/")
        accept(ContentType.Application.Json)
    }
}

fun submitToProducer(producer: KafkaProducer, course: CurrencyCourse){
    producer.producer.send(ProducerRecord("currency", course.firstCurrency + course.secondCurrency, Json.encodeToString(course)))

}

fun endlessFlow() = flow<Unit> {
    emit(Unit)
    while(true){
        delay(1.minutes.inWholeMilliseconds)
        emit(Unit)
    }
}