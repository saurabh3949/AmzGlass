## Amazon Glass
Parse Amazon product pages using Python to get the following attributes:

* Title
* Brand
* Product description
* Tech specs
* Price
* Image URL (to be added)
* Category


## Usage
    git clone https://github.com/saurabh3949/AmzGlass.git
    cd AmzGlass
    pip install -r requirements.txt

Now copy all the product HTML to data folder and run:

    scrapy crawl amazon -o output.json

to generate the extracts in `output.json`


In case of any bugs, please email me at saurabh3949@gmail.com
