'''Multiprocessing not supported in notebook so moving on to simple .py file to implement multiprogramming concepts'''

import requests
import time
import multiprocessing
import os

# URL 
url = "https://picsum.photos/2000/3000"


# Function to download an image
def download_image(index):
    directory=f"C:/Users/NikhilJain/py-wiz/src/Day7/images/"
    os.makedirs(directory,exist_ok=True)     
    response = requests.get(url)
    filename=os.path.join(directory,f"images_{index}.jpg")
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded image_{index}.jpg")  



# With multiprocessing
def download_images_multiprocessing():
    start_time = time.time()    
    processes = []
    for i in range(5):
        process = multiprocessing.Process(target=download_image, args=(i,))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()


    end_time = time.time()
    print(f"Multiprocessing download time: {end_time - start_time:.2f} seconds")


if __name__=="__main__":
    download_images_multiprocessing()


