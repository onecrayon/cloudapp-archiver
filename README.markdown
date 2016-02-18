# archive-cloudapp.py

This script downloads all files in your CloudApp account for archival purposes.

## Installation

    git clone --recursive git://github.com/onecrayon/cloudapp-archiver.git

## Usage example

    mkdir archive
    cd cloudapp-archiver/
    ./archive-cloudapp.py -u YOU@EMAIL.COM -p PASSWORD -o ../archive

If you prefer, you can use the long-form option flags `--password`, `--user`, and `--output` instead. The script will organize your files into folders by date and stub with the final file inside (e.g. `archive/2016-02-17/Jc9e/hedgehog-running.gif`).

Shortened links are output as `.url` files, which are simple text files you can open with most major browsers.

The script is safe to run multiple times (or re-run over time); if it encounters an existing stub folder, it will skip trying to download that file.

## MIT License

Copyright (c) 2016 Ian Beck

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
