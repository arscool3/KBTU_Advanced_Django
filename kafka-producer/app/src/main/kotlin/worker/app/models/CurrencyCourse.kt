package worker.app.models

import kotlinx.serialization.SerialName

@kotlinx.serialization.Serializable
data class CurrencyCourse(
    @SerialName("first_currency")
    val firstCurrency: String,
    @SerialName("second_currency")
    val secondCurrency: String,
    val rates: List<Float>,
    val interval: Interval
)

@kotlinx.serialization.Serializable
data class Interval(
    @SerialName("start_date")
    val startDate: String,
    @SerialName("end_date")
    val endDate: String
)