import httpx
from httpx_retries import Retry, RetryTransport

timeout = httpx.Timeout(connect=10.0, read=30.0, write=30.0, pool=5.0)

retry = Retry(total=3, backoff_factor=0.5)
retry_transport = RetryTransport(retry=retry)

url = "https://api.github.com"
file_path = "output_file.txt"

with httpx.Client(timeout=timeout, transport=retry_transport) as client:
  with client.stream("GET", url) as response:
    response.raise_for_status()
    with open(file_path, "wb") as f:
      for chunk in response.iter_bytes(chunk_size=1000):
        print(chunk)
        print(f"Downloaded {len(chunk)} bytes")
        f.write(chunk)

print(f"Downloaded successfully to {file_path}")
