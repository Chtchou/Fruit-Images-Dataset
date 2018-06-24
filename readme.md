We built here a basic classifier regarding the Fruits - 360 Data from Kaggle.
For this we use the fastai library which is running with the PyTorch backend. Fastai is to PyTorch, what Keras is to TensorFlow : a wrapper to simplify the basic tasks and accelerate analysis.

Fastai can be installed from the following link :https://github.com/fastai
Then it is necessary to create a simlink to the fastai repository to be able to use library.

The Dataset can be found on Github: 
https://github.com/Horea94/Fruit-Images-Dataset
or on Kaggle :
https://www.kaggle.com/moltean/fruits

*Note* The dataset is regularly updated with new fruits. For reproductibility purpose we added on the github, the version of the dataset used for our classification.
Therefore the process for classifying the fruits images remaining identical, and is not dependant of the number of image classes.

# Fruits-360: A dataset of images containing fruits #

A high-quality, dataset of images containing fruits. The following fruits are included: 
Apples (different varieties: Golden, Golden-Red, Granny Smith, Red, Red Delicious), Apricot, Avocado, Avocado ripe, Banana (Yellow, Red), Cactus fruit, Cantaloupe (2 varieties), Carambula, Cherry (different varieties, Rainier), Clementine, Cocos, Dates, Granadilla, Grape (Pink, White, White2), Grapefruit (Pink, White), Guava, Huckleberry, Kiwi, Kaki, Kumsquats, Lemon (normal, Meyer), Lime, Litchi, Mandarine, Mango, Maracuja, Nectarine, Orange, Papaya, Passion fruit, Peach, Pepino, Pear (different varieties, Abate, Monster, Williams), Pineapple, Pitahaya Red, Plum, Pomegranate, Quince, Raspberry, Salak, Strawberry, Tamarillo, Tangelo.

## Dataset properties ##

Total number of images: 42345.

Training set size: 31688 images.

Validation set size: 10657 images.

Number of classes: 64 (fruits).

Image size: 100x100 pixels.

Filename format: image_index_100.jpg (e.g. 32_100.jpg) or r_image_index_100.jpg (e.g. r_32_100.jpg) or r2_image_index_100.jpg. "r" stands for rotated fruit. "r2" means that the fruit was rotated around the 3rd axis. "100" comes from image size (100x100 pixels).

Different varieties of the same fruit (apple for instance) are stored as belonging to different classes.

## Repository structure ##

Folders [Training](Training) and [Validation](Validation) contain all images with white backgrounds only.

Folder [test-multiple_fruits](test-multiple_fruits) contains images with multiple fruits. Some of them are partially covered by other fruits. This is an excelent test for real-world detection.

Folder [src](src) contains the python code for training the neural network. It uses the TensorFlow library.

Folder [src/utils](src/utils) contains the C++ code used for extracting the fruits from the background. 


## Citation##

Horea Muresan, [Mihai Oltean](https://mihaioltean.github.io), Fruit recognition from images using deep learning, Technical Report, Babes-Bolyai University, 2017

## How the dataset was created ##

Fruits were planted in the shaft of a low speed motor (3 rpm) and a short movie of 20 seconds was recorded. 

A Logitech C920 camera was used for filming the fruits. This is one of the best webcams available.

Behind the fruits we placed a white sheet of paper as background. 

However due to the variations in the lighting conditions, the background was not uniform and we wrote a dedicated algorithm which extract the fruit from the background. This algorithm is of flood fill type: 
we start from each edge of the image and we mark all pixels there, then we mark all pixels found in the neighborhood of the already marked pixels for which the distance between colors is less than a prescribed value. We repeat the previous step until no more pixels can be marked.

All marked pixels are considered as being background (which is then filled with white) and the rest of pixels are considered as belonging to the object.

The maximum value for the distance between 2 neighbor pixels is a parameter of the algorithm and is set (by trial and error) for each movie.

