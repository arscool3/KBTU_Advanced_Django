package org.example.http_client

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.features.json.*
import io.ktor.client.features.json.serializer.*

class HttpClientWrapper {

    private val serializer by lazy {
        KotlinxSerializer(
            json = kotlinx.serialization.json.Json{
                ignoreUnknownKeys = true
            }
        )
    }

    val httpClient by lazy {
        HttpClient {
            engine{ CIO}
            install(JsonFeature){
                serializer = this@HttpClientWrapper.serializer
            }
        }
    }
}