package binance.example.plugins

import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.netty.handler.codec.json.JsonObjectDecoder
import java.util.*
import kotlin.random.Random
import kotlin.time.Duration.Companion.hours
import kotlin.time.Duration.Companion.minutes

fun Application.configureRouting() {
    routing {
        get("/") {
            call.respondText(generateJson(), contentType = io.ktor.http.ContentType.Application.Json)
        }
    }
}

fun generateRandFloat(): Float{
    return MIN_VALUE + Random.nextFloat() * (MAX_VALUE - MIN_VALUE)
}

fun generateJson(): String{
    return """
        {
            "first_currency": "$FIRST_CURRENCY",
            "second_currency": "$SECOND_CURRENCY",
            "rates": ${
                listOf(1, 2, 3, 4, 5).map { generateRandFloat() }
            },
            "interval": {
                "start_date": "${Date()}",
                "end_date": "${Date(1.hours.inWholeMilliseconds + System.currentTimeMillis())}"
            } 
        }
    """.trimIndent()
}

private const val MIN_VALUE = 500f
private const val MAX_VALUE = 600f
private const val FIRST_CURRENCY = "BTC"
private const val SECOND_CURRENCY = "ETH"