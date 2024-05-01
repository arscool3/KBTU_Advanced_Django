package main

import (
	"binance"
	"github.com/valyala/fasthttp"
	"log"
)

type Server struct {
	server *fasthttp.Server
	notify chan error
}

func main() {
	router := binance.NewRouter()
	server := Server{
		server: &fasthttp.Server{
			Handler: *router.InitRouter(),
		},
		notify: make(chan error, 1),
	}
	log.Println("Binance listening on port :8080")
	server.Start()
	<-server.notify
}

func (s *Server) Start() {
	go func() {
		s.notify <- s.server.ListenAndServe(":8080")
		close(s.notify)
	}()
}
