"""
Script to download and display an image from a URL while avoiding HTTP 403 errors.
The key is to add proper headers to mimic a browser request.
"""

import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def download_and_display_image(url):
    """
    Download and display an image from a URL with proper headers to avoid 403 errors.

    Args:
        url (str): The URL of the image to download
    """
    # Add headers to mimic a browser request and avoid 403 errors
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        # Make the request with headers
        response = requests.get(url, headers=headers, timeout=10)

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Open the image from the response content
        img = Image.open(BytesIO(response.content))

        # Display the image
        plt.figure(figsize=(10, 8))
        plt.imshow(img)
        plt.axis('off')
        plt.title('Downloaded Image')
        plt.tight_layout()
        plt.show()

        print(f"✓ Image successfully downloaded and displayed!")
        print(f"Image size: {img.size}")
        print(f"Image mode: {img.mode}")

        return img

    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
        print(f"Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

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
