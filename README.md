# MusicGenerator

to scrap the dataset call
`python scrapMusic.py n`
where n is the number of threads that you want to use
before scrapping please delete the midi folder including its contents

after scrapping the midi files, you can call
`python scrapImages.py n`
where n is the number of threads that you want to use
before scrapping images please run the scrapMusic script first

CreatingTrainingData.ipynb, makingTxtWithFirstNotes.ipynb, and resize_image.ipynb -> are for preprocessing images, makeing tct documents with notes 

ImageToTextGenerator.ipynb -> this is model for generatint text based on image 

test_slika.ipynb  -> this is code for testing model 

https://drive.google.com/file/d/14bGsH7MxTKydOdOxNM4sU8XnLr6Rdk77/view?usp=sharing -> on this link are images for resizing

https://drive.google.com/file/d/1HccziZkT3A_6PFW_7lRcqwkv6ZbXJROH/view?usp=sharing -> on this link are resized images with programm

https://drive.google.com/file/d/14bGsH7MxTKydOdOxNM4sU8XnLr6Rdk77/view?usp=sharing -> on this link are images for testing

https://drive.google.com/file/d/1MECXvMhtc5b8hkMqBRibt4Yc0jEr_6U5/view?usp=sharing -> link for model for generating music from image

Za pokretanje generatora muzike na osnovu par nota pokrenuti generate.py iz gpt-2simple, input staviti u "tekst" varijablu, da bi produzili pesmu povecati broj iteracija
