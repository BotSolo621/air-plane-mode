package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	deviceName := "kit kat"
	url := fmt.Sprintf("http://127.0.0.1:8000/ping/%s", deviceName)

	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer resp.Body.Close()

	// Read the response
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Read error:", err)
		return
	}

	fmt.Println("Server response:", string(body))
}
