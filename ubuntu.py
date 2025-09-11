import requests
import os
from urllib.parse import urlparse

def fetch_image():

    image_url = input("Enter image url: ").strip()
    try:
        folder = "Fetched Images"
        os.makedirs(folder, exist_ok=True)

        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"
        
        filepath = os.path.join(folder, filename)

        print("Downloading...")
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(image_url, headers=headers, timeout=10)
        r.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(r.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        print("\nConnection strengthened. Community enriched.")

    except requests.exceptions.MissingSchema:
        print("Error: Invalid URL. Please include http:// or https://")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch image. Details: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

fetch_image()