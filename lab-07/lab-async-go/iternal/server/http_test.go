package server

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestHTTPServerBasic(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "Hello, World!")
	}))
	defer server.Close()

	resp, err := http.Get(server.URL)
	if err != nil {
		t.Fatalf("Failed to get response: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status %d, got %d", http.StatusOK, resp.StatusCode)
	}

	body, _ := io.ReadAll(resp.Body)
	if string(body) != "Hello, World!" {
		t.Errorf("Expected 'Hello, World!', got %s", string(body))
	}
}

func TestHTTPServerConcurrentRequests(t *testing.T) {
	requestCount := int64(0)

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		atomic.AddInt64(&requestCount, 1)
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "OK")
	}))
	defer server.Close()

	var wg sync.WaitGroup
	numRequests := 100

	for i := 0; i < numRequests; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			resp, _ := http.Get(server.URL)
			if resp != nil {
				resp.Body.Close()
			}
		}()
	}

	wg.Wait()

	if requestCount != int64(numRequests) {
		t.Errorf("Expected %d requests, got %d", numRequests, requestCount)
	}
}

func TestHTTPServerMultipleEndpoints(t *testing.T) {
	mux := http.NewServeMux()

	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "root")
	})
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "ok")
	})

	server := httptest.NewServer(mux)
	defer server.Close()

	tests := []struct {
		path     string
		expected string
	}{
		{"/", "root"},
		{"/health", "ok"},
	}

	for _, tt := range tests {
		resp, _ := http.Get(server.URL + tt.path)
		body, _ := io.ReadAll(resp.Body)
		resp.Body.Close()

		if string(body) != tt.expected {
			t.Errorf("Path %s: expected %s, got %s", tt.path, tt.expected, string(body))
		}
	}
}

func TestHTTPServerResponseTime(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(100 * time.Millisecond)
		fmt.Fprint(w, "delayed response")
	}))
	defer server.Close()

	start := time.Now()
	resp, _ := http.Get(server.URL)
	resp.Body.Close()
	elapsed := time.Since(start)

	if elapsed < 100*time.Millisecond {
		t.Errorf("Expected at least 100ms, got %v", elapsed)
	}
}

func TestHTTPServerStatusCodes(t *testing.T) {
	mux := http.NewServeMux()

	mux.HandleFunc("/ok", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	})
	mux.HandleFunc("/notfound", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	})
	mux.HandleFunc("/error", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
	})

	server := httptest.NewServer(mux)
	defer server.Close()

	tests := []struct {
		path   string
		status int
	}{
		{"/ok", http.StatusOK},
		{"/notfound", http.StatusNotFound},
		{"/error", http.StatusInternalServerError},
	}

	for _, tt := range tests {
		resp, _ := http.Get(server.URL + tt.path)
		if resp.StatusCode != tt.status {
			t.Errorf("Path %s: expected status %d, got %d", tt.path, tt.status, resp.StatusCode)
		}
		resp.Body.Close()
	}
}

func TestHTTPServerHeaders(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Custom-Header", "test-value")
		fmt.Fprint(w, "response")
	}))
	defer server.Close()

	resp, _ := http.Get(server.URL)
	defer resp.Body.Close()

	if resp.Header.Get("X-Custom-Header") != "test-value" {
		t.Error("Custom header not found in response")
	}
}

func TestHTTPServerTimeout(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(2 * time.Second)
		fmt.Fprint(w, "response")
	}))
	defer server.Close()

	client := &http.Client{Timeout: 500 * time.Millisecond}
	_, err := client.Get(server.URL)

	if err == nil {
		t.Error("Expected timeout error")
	}
}

func TestHTTPServerRequestBody(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		body, _ := io.ReadAll(r.Body)
		fmt.Fprintf(w, "received: %s", string(body))
	}))
	defer server.Close()

	resp, _ := http.Post(server.URL, "text/plain", nil)
	defer resp.Body.Close()
}

func TestHTTPServerConcurrentShutdown(t *testing.T) {
	requestCount := int64(0)

	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		atomic.AddInt64(&requestCount, 1)
		time.Sleep(50 * time.Millisecond)
		fmt.Fprint(w, "OK")
	})

	server := httptest.NewServer(mux)

	var wg sync.WaitGroup
	for i := 0; i < 20; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			http.Get(server.URL)
		}()
	}

	wg.Wait()
	server.Close()

	if requestCount != 20 {
		t.Errorf("Expected 20 requests, got %d", requestCount)
	}
}

func BenchmarkHTTPServer(b *testing.B) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "OK")
	}))
	defer server.Close()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		http.Get(server.URL)
	}
}

func BenchmarkHTTPServerConcurrent(b *testing.B) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "OK")
	}))
	defer server.Close()

	b.ResetTimer()
	var wg sync.WaitGroup
	for i := 0; i < b.N; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			http.Get(server.URL)
		}()
	}
	wg.Wait()
}

func TestHTTPServerContext(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		select {
		case <-r.Context().Done():
			w.WriteHeader(http.StatusRequestTimeout)
			return
		default:
			fmt.Fprint(w, "OK")
		}
	})

	server := httptest.NewServer(mux)
	defer server.Close()

	resp, _ := http.Get(server.URL)
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status OK, got %d", resp.StatusCode)
	}
	resp.Body.Close()
}

func TestHTTPServerLargePayload(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Отправляем большой ответ
		for i := 0; i < 1000; i++ {
			fmt.Fprintf(w, "Line %d\n", i)
		}
	}))
	defer server.Close()

	resp, _ := http.Get(server.URL)
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	if len(body) == 0 {
		t.Error("Expected non-empty response body")
	}
}

func ExampleHTTPServer() {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "Hello from server")
	}))
	defer server.Close()

	resp, _ := http.Get(server.URL)
	body, _ := io.ReadAll(resp.Body)
	resp.Body.Close()

	fmt.Println(string(body))
	// Output: Hello from server
}
