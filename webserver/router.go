package main

import (
	"fmt"
	"net/http"
)

type Router struct{}

func (r Router) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	path := req.URL.Path
	method := req.Method
	handler := r.getHandler(method, path)
	handler(w, req)
}

func (r *Router) getHandler(method string, path string) func(http.ResponseWriter, *http.Request) {
	return NotFoundError
}

func NotFoundError(w http.ResponseWriter, req *http.Request) {
	w.WriteHeader(http.StatusNotFound)
	fmt.Fprint(w, "404 - Not found")
}
