import os
import urllib.request
import ssl

def download_background():
    # Create images directory if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")
    
    # URL for a free-to-use cloud background
    image_url = "https://img.freepik.com/free-vector/realistic-cloudy-sky-background_23-2149113060.jpg"
    
    # Path to save the image
    image_path = os.path.join("images", "background.jpg")
    
    print(f"Downloading cloud background image from {image_url}...")
    
    try:
        # Create SSL context to handle HTTPS
        context = ssl._create_unverified_context()
        
        # Download the image
        urllib.request.urlretrieve(image_url, image_path)
        print(f"Cloud background image successfully downloaded to {image_path}")
    except Exception as e:
        print(f"Error downloading image: {e}")
        print("Please try downloading a cloud image manually and save it as 'images/background.jpg'")

if __name__ == "__main__":
    download_background()
