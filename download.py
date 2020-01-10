from imutils import paths
import argparse
import requests
import cv2
import os


def main(urls, outputs):
    rows = open(urls).read().strip().split("\n")
    total = 0
    # loop the URLs
    for url in rows:
        try:
            # try to download the image
            r = requests.get(url, timeout=60)
            # save the image to disk
            img_num = os.path.sep.join([outputs, "{}.jpg".format(str(total).zfill(8))])
            f = open(img_num, "wb")
            f.write(r.content)
            f.close()
            print(f"Downloaded: {img_num}")
            total += 1
            # handle if any exceptions are thrown during the download process so it doesn't die
        except:
            print(f"Skipping: {img_num}")

    for image_path in paths.list_images(outputs):
        delete = False
        try:
            image = cv2.imread(image_path)
            if image is None:
                delete = True
        except:
            print("Except")
            delete = True
        # check to see if the image should be deleted
        if delete:
            print(f"Deleting {image_path}")
            os.remove(image_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--urls", required=True, help="path to file containing image URLs")
    ap.add_argument("-o", "--output", required=True, help="path to output directory of images")
    args = vars(ap.parse_args())
    main(args["urls"], args["output"])
