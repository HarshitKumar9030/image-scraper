from flask import Flask, request, jsonify, send_file, send_from_directory
import requests
import os
import json
from threading import Thread
from queue import Queue
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

BING_API_KEY = ''  # Replace with your actual Bing API key
SEARCH_URL = 'https://api.bing.microsoft.com/v7.0/images/search'
IMAGE_STORAGE_DIR = './image-storage'
METADATA_FILE = os.path.join(IMAGE_STORAGE_DIR, 'metadata.json')

os.makedirs(IMAGE_STORAGE_DIR, exist_ok=True)

if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'r') as file:
        metadata = json.load(file)
else:
    metadata = []

download_queue = Queue()

def download_image_task():
    while True:
        image_info = download_queue.get()
        if image_info is None:
            break

        try:
            img_url, img_path = image_info
            img_response = requests.get(img_url)
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
        except Exception as e:
            print(f"Error downloading image: {e}")
        finally:
            download_queue.task_done()

thread = Thread(target=download_image_task)
thread.daemon = True
thread.start()

@app.route('/api/download', methods=['POST'])
def search_images():
    query = request.json.get('query', '')
    headers = {'Ocp-Apim-Subscription-Key': BING_API_KEY}
    params = {'q': query, 'count': 10, 'imageType': 'photo'}

    try:
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()

        image_data = []
        valid_extensions = ['jpg', 'jpeg', 'png']  # Only valid image types
        for img in results.get('value', []):
            img_url = img['contentUrl']
            img_title = img.get('name', 'Untitled')
            img_id = img['imageId']
            img_ext = img_url.split('.')[-1].lower()
            if img_ext not in valid_extensions:
                print(f"Skipping invalid image format: {img_ext}")
                continue

            img_filename = f"{query}_{img_id}.{img_ext}"
            category_folder = os.path.join(IMAGE_STORAGE_DIR, query)
            img_path = os.path.join(category_folder, img_filename)

            os.makedirs(category_folder, exist_ok=True)

            download_queue.put((img_url, img_path))

            image_entry = {
                'id': img_id,
                'title': img_title,
                'url': f'/{query}/{img_filename}',
                'category': query
            }
            image_data.append(image_entry)

        metadata.extend(image_data)
        with open(METADATA_FILE, 'w') as file:
            json.dump(metadata, file)

        return jsonify({'message': 'Images are being downloaded', 'images': image_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fetch_image', methods=['GET'])
def fetch_image():
    category = request.args.get('category')
    if not category:
        return jsonify({'error': 'Category parameter is missing'}), 400

    category = category.lower()
    found_image = None

    for image in metadata:
        if image['category'].lower() == category:
            image_url = image['url'].lstrip('/')
            full_path = os.path.join(IMAGE_STORAGE_DIR, image_url)
            if os.path.exists(full_path):
                found_image = full_path
                break
            else:
                print(f"Image file does not exist at path: {full_path}")

    if found_image:
        return send_file(found_image, as_attachment=True)
    else:
        print(f"No images found for category: {category}")
        return jsonify({'error': 'No images available yet'}), 404


@app.route('/api/gallery', methods=['GET'])
def get_images():
    category = request.args.get('category', 'All').lower()

    if category == 'all':
        filtered_images = metadata
    else:
        filtered_images = [img for img in metadata if img['category'].lower() == category]

    return jsonify({'images': filtered_images})

@app.route('/images/<path:filename>')
def serve_image(filename):
    directory = os.path.join(IMAGE_STORAGE_DIR, os.path.dirname(filename))
    return send_from_directory(directory, os.path.basename(filename))

    category = request.args.get('category')
    if not category:
        return jsonify({'error': 'Category parameter is missing'}), 400

    category = category.lower()
    found_image = None

    for image in metadata:
        if image['category'].lower() == category:
            image_url = image['url'].lstrip('/')
            full_path = os.path.join(IMAGE_STORAGE_DIR, image_url)
            if os.path.exists(full_path):
                found_image = full_path
                break
            else:
                print(f"Image file does not exist at path: {full_path}")  

    if found_image:
        return send_file(found_image, as_attachment=True)
    else:
        print(f"No images found for category: {category}") 
        return jsonify({'error': 'No images available yet'}), 404


@app.route('/api/categories', methods=['GET'])


def fetch_categories():
    categories = []
    for subdir in os.listdir(IMAGE_STORAGE_DIR):
        subdir_path = os.path.join(IMAGE_STORAGE_DIR, subdir)
        if os.path.isdir(subdir_path):
            # Filter images from the metadata that belong to this category
            images_in_category = [img for img in metadata if img['category'].lower() == subdir.lower()]
            if images_in_category:
                # Select a random image from the category
                random_image = images_in_category[2] 
                categories.append({
                    'name': subdir,
                    'random_image_url': f'/images/{random_image["url"].lstrip("/")}',
                    'gallery_url': f'/gallery/{subdir}'
                })
    return jsonify({'categories': categories})

    
@app.route('/api/search_local', methods=['POST'])
def search_local_images():
    query = request.json.get('query', '').lower()
    matching_images = []

    for root, dirs, files in os.walk(IMAGE_STORAGE_DIR):
        for file in files:
            if query in file.lower():
                rel_dir = os.path.relpath(root, IMAGE_STORAGE_DIR)
                image_path = os.path.join(rel_dir, file)
                image_data = {
                    'url': f'/images/{image_path}',
                    'title': file,
                    'category': rel_dir.split(os.sep)[0]
                }
                matching_images.append(image_data)

    return jsonify({'images': matching_images})


# @app.route('/api/test', methods=['POST'])
# def test():
#         query = request.json.get('query', '').lower()
#         count = request.json.get('count', '')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)