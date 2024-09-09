
# 📸 Image Scraper

Welcome to **Image Scraper**! This project allows you to search and download images from the web using the Bing Image Search API. You can specify search queries and the number of images you want to download, and the app will handle fetching and downloading them for you! 🎉

## 🚀 Getting Started

To get started, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/harshitkumar9030/image-scraper.git
cd image-scraper
```

### 2. Install Dependencies

Ensure you have **Python 3.x** and **pip** installed. Then, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up the Bing API Key 🔑

You need to obtain a Bing API key from Azure:

1. Go to the [Azure Portal](https://portal.azure.com/).
2. Search for "Bing Search" and create a new resource.
3. Navigate to the **Keys and Endpoint** section to obtain your API key.

Then, **replace the hardcoded API key** in the `main.py` file:

```python
BING_API_KEY = 'your_bing_api_key_here'
```

### 4. Create `image_storage` Directory 📂

Make sure to create an `image_storage` folder in the root directory of the project:

```bash
mkdir image-storage
```

This folder will be used to store downloaded images.

### 5. Run the Application

Run the server using:

```bash
python main.py
```

The server should be up and running at `http://localhost:5000`.

### 6. Next.js App Setup

To set up the Next.js app located in `./image_app`, navigate to the directory and install the dependencies:

```bash
cd image_app
npm install
npm run dev
```

This will start the Next.js app, which should be accessible at `http://localhost:3000`.

## 🛠 Features

- **Search and Download Images**: Enter a search query and specify the number of images to download. The app fetches images using the Bing API.
- **Automatic and Manual Download**: Images can be automatically downloaded or manually selected.
- **Grid and List View**: Choose between grid and list view to display images.

## 🐞 Known Issues

- The download page may be a bit buggy, but it works after all! 😉 I'm working on a fix soon. 

## 📝 Future Improvements

- Improve error handling and ensure smoother image fetching.
- Enhance the user interface with additional functionalities and animations.

## 📫 Contact

I'm Harshit! Feel free to connect with me:

- **Instagram**: [_harshit.xd](https://instagram.com/_harshit.xd)
- **Portfolio**: [leoncyriac.me](https://leoncyriac.me)

## ⭐️ Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

Happy Scraping! 🎉
