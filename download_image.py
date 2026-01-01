"""
Script to download and display an image from a URL while avoiding HTTP 403/429 errors.
Handles rate limiting and Wikimedia-specific requirements.
"""

import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import time

def download_and_display_image(url, max_retries=5, initial_delay=2):
    """
    Download and display an image from a URL with proper headers and retry logic.
    Handles both 403 Forbidden and 429 Too Many Requests errors.

    Args:
        url (str): The URL of the image to download
        max_retries (int): Maximum number of retry attempts for rate limiting
        initial_delay (int): Initial delay in seconds for exponential backoff
    """
    # Proper User-Agent for Wikimedia and other services
    # Wikimedia requires identification and contact info in User-Agent
    headers = {
        'User-Agent': 'Python Image Downloader/1.0 (Educational/Research; Python requests)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'DNT': '1'
    }

    # Retry logic with exponential backoff
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")

            # Make the request with headers and allow redirects
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)

            # Handle rate limiting (429) with exponential backoff
            if response.status_code == 429:
                if attempt < max_retries - 1:
                    print(f"⚠ Rate limited (429). Waiting {delay} seconds before retry...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                    continue
                else:
                    print(f"✗ Rate limit exceeded after {max_retries} attempts")
                    print(f"Error: {response.text}")
                    return None

            # Raise an exception for other bad status codes
            response.raise_for_status()

            # Open the image from the response content
            img = Image.open(BytesIO(response.content))

            # Display the image
            plt.figure(figsize=(12, 9))
            plt.imshow(img)
            plt.axis('off')
            plt.title('Downloaded Image')
            plt.tight_layout()
            plt.show()

            print(f"✓ Image successfully downloaded and displayed!")
            print(f"Final URL: {response.url}")
            print(f"Image size: {img.size}")
            print(f"Image mode: {img.mode}")

            return img

        except requests.exceptions.HTTPError as e:
            print(f"✗ HTTP Error: {e}")
            print(f"Status Code: {response.status_code}")
            if response.status_code != 429:
                print(f"Response: {response.text[:200]}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Request Error: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                return None
        except Exception as e:
            print(f"✗ Error: {e}")
            return None

    return None

if __name__ == "__main__":
    # The URL from the user
    image_url = "http://bit.ly/46xv3sL"

    print(f"Downloading image from: {image_url}")
    print("-" * 50)

    # Download and display the image
    image = download_and_display_image(image_url)

    # Optional: Save the image locally
    if image:
        output_path = "downloaded_image.png"
        image.save(output_path)
        print(f"✓ Image saved to: {output_path}")
