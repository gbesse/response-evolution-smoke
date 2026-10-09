package main

import (
    "encoding/json"
    "os"
)

func main() {
    var response struct { Items []string `json:"items"` }
    decoder := json.NewDecoder(os.Stdin)
    decoder.DisallowUnknownFields()
    if err := decoder.Decode(&response); err != nil { os.Exit(2) }
}
