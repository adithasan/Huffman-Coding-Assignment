# Huffman-Coding-Assignment
Assignment I did on Huffman Coding for an assignment.

Running the Compressor

Once you have implemented the util.compress function, you will be able to run the compress.py script to compress files. 
For example, to add a new file somefile.pdf to be served by the web server, copy it to the wwwroot/ directory, 
change to that directory, and run

python3 ../compress.py somefile.pdf

This will generate somefile.pdf.huf and you will be able to access the decompressed version at the URL 
http://localhost:8000/somefile.pdf. You should download the decompressed file and compare it to the original 
using the cmp command, to make sure there are no differences.


Running the Web Server

Once you have implemented the decompress function, you will be able to run the webserver.py script to serve compressed files. 
To try this out, change to the wwwroot/ directory included with the assignment and run
python3 ../webserver.py
Then open the url http://localhost:8000 in your web browser. If all goes well, you should see a web page 
including an image. Compressed versions of the web page and the image are stored as index.html.huf and 
huffman.bmp.huf in the wwwroot/ directory. The web server is using your decompress function to decompress 
these files and serve them to your web browser.

