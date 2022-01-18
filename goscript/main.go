package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

type apiResp struct {
	Positions []position `json:positions`
}

type position struct {
	Count int `json:count`
	Id    int `json:id`
}

const ksJobsApiFmt = "https://kroger.eightfold.ai/api/apply/v2/jobs?domain=kroger.com&domain=kroger.com&start=%d&num=10&location=colorado&query=temporary"

var client = &http.Client{}

func main() {
	start := 0

	ids := make([]int, 0, 100)
	more := true
	for more {
		newIds := oneCall(start)
		ids = append(ids, newIds...)
		more = len(newIds) > 0
		start = start + 10
	}

	fmt.Printf("Got %d total positions", len(ids))

	outUrlFmt := "https://kroger.eightfold.ai/careers?pid=%d\n"
	for i := 0; i < len(ids); i++ {
		fmt.Printf(outUrlFmt, ids[i])
	}
}

func oneCall(start int) (ids []int) {
	req, err := http.NewRequest("GET", fmt.Sprintf(ksJobsApiFmt, start), nil)
	req.Header.Set("User-Agent", "curl\\7.64.1")
	if err != nil {
		fmt.Printf("Failed to create API request! %+v\n", err)
		os.Exit(1)
	}

	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Failed to hit jobs API! %+v\n", err)
		os.Exit(1)
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Could not read resp body: %+v\n", err)
		os.Exit(1)
	}
	//	fmt.Printf("Raw:\n%s\n", body)

	var respObj apiResp
	err = json.Unmarshal(body, &respObj)
	if err != nil {
		fmt.Printf("Failed to unmarshal response body: %+v\n", err)
		os.Exit(1)
	}
	//	fmt.Printf("Body:\n%+v\n", respObj)
	positions := respObj.Positions

	//	fmt.Printf("Got these positions: %+v\n", positions)

	ids = make([]int, 0, 10)

	for i := 0; i < len(positions); i++ {
		ids = append(ids, positions[i].Id)
	}

	return
}
