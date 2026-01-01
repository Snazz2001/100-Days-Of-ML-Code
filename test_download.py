"""
Quick test script to verify the image download fix works
"""

import requests
from PIL import Image
from io import BytesIO
import time

def test_download(url, max_retries=3):
    """Test downloading with proper headers and retry logic."""
    headers = {
        'User-Agent': 'Python Image Downloader/1.0 (Educational/Research; Python requests)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
    }

    delay = 2
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)

            if response.status_code == 429:
                if attempt < max_retries - 1:
                    print(f"⚠ Rate limited. Waiting {delay}s...")
                    time.sleep(delay)
                    delay *= 2
                    continue
                else:
                    print("✗ Rate limit exceeded")
                    return False

            response.raise_for_status()
            img = Image.open(BytesIO(response.content))

            print(f"✓ SUCCESS!")
            print(f"Final URL: {response.url}")
            print(f"Image size: {img.size}")
            print(f"Image mode: {img.mode}")

            # Save the image
            img.save('test_image.png')
            print(f"✓ Saved as test_image.png")
            return True

        except Exception as e:
            print(f"✗ Error: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2

    return False

if __name__ == "__main__":
    url = "http://bit.ly/46xv3sL"
    print(f"Testing download from: {url}")
    print("-" * 60)
    success = test_download(url, max_retries=5)
    print("-" * 60)
    if success:
        print("✓ Test PASSED - Image downloaded successfully!")
    else:
        print("✗ Test FAILED - Could not download image")
