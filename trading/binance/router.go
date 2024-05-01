package binance

import (
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/valyala/fasthttp"
	"net/http"
	"time"
)

type Router struct {
	binance Manager
}

func NewRouter() *Router {
	return &Router{}
}

func (r *Router) InitRouter() *fasthttp.RequestHandler {
	router := fiber.New()
	router.Use(logger.New(logger.Config{DisableColors: false}))

	router.Get("/binance", r.getPricesInRange)

	handler := router.Handler()
	return &handler
}

type PricesInRangeResponse struct {
	Curr1  string             `json:"curr_1"`
	Curr2  string             `json:"curr_2"`
	Prices map[string]float64 `json:"Prices"`
}

func (r *Router) getPricesInRange(ctx *fiber.Ctx) error {
	curr1 := ctx.Query("curr1")
	curr2 := ctx.Query("curr2")
	timeFrom := ctx.Query("from")
	timeTo := ctx.Query("to")

	if curr1 == "" || curr2 == "" {
		ctx.Status(http.StatusBadRequest)
		return nil
	}

	startTime, err := time.Parse(time.RFC3339, timeFrom)
	if err != nil {
		ctx.Status(http.StatusBadRequest)
		return err
	}
	endTime, err := time.Parse(time.RFC3339, timeTo)
	if err != nil {
		ctx.Status(http.StatusBadRequest)
		return err
	}

	prices := r.binance.GetPricesInSecondsRange(startTime, endTime)

	response := &PricesInRangeResponse{
		Curr1:  curr1,
		Curr2:  curr2,
		Prices: prices,
	}

	ctx.JSON(response)
	return nil
}
