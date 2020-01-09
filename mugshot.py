from PIL import Image
from matplotlib import image
from matplotlib import pyplot


def main():
    _image = Image.open('pictures/1.jpg')
    print(_image.format)
    print(_image.mode)
    print(_image.size)

    # load and display an image with Matplotlib
    # load image as pixel array
    data = image.imread('pictures/1.jpg')
    # summarize shape of the pixel array
    print(data.dtype)
    print(data.shape)
    # display the array of pixels as an image
    pyplot.imshow(data)
    pyplot.show()


if __name__ == '__main__':
    main()
