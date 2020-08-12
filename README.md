### Movie Barcode Generator Web App

This Web app takes reference from the repository by Author: Erol Recep(https://github.com/erolrecep)
Title : moviebarcode[https://github.com/erolrecep/moviebarcode].

This web app was developed to visualize aBarcode generator and is deployed on Heroku and hosted at https://mbcodegen.herokuapp.com/. 

You can test it by providing either a YouTube video URL, Video ID or both as an input to generate a barcode.

Note: This Web app can take both Video IDs and URLs respectively.

 
## Setup

When you clone this repository, open Command Prompt in the same folder the repository will be downloaded into.

Navigate to the downloaded repository (cd barcodegen)

Create a Virtual environment to install all required packages by installing the requirements.txt:

$conda create --name barcodegen
$conda activate barcodegen
$(barcodegen) conda install -r requirements.txt

run app.py ( This should run after properly installing flask and its dependencies)

Go to the https Flask link that comes up on your computer to access the webapp

Input your Video URL and Generate Barcode from your local computer to ensure it is working properly.


