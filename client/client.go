package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "time"
)

const (
    serverURL = "http://localhost:8000/client/checkin" // change this to your server URL
    deviceID  = "device123"
)

func checkin() {
    data := map[string]string{
        "device_id": deviceID,
    }

    jsonData, err := json.Marshal(data)
    if err != nil {
        fmt.Println("Error marshaling JSON:", err)
        return
    }

    resp, err := http.Post(serverURL, "application/json", bytes.NewBuffer(jsonData))
    if err != nil {
        fmt.Println("Error sending POST:", err)
        return
    }
    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println("Error reading response:", err)
        return
    }

    fmt.Printf("[+] Checked in. Server response: %s\n", string(body))
}

func main() {
    fmt.Println("[+] Client started.")

    for {
        checkin()
        time.Sleep(5 * time.Second)
    }
}
