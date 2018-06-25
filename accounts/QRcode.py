#Run 'pip install pyqrcode' if pyqrcode is not already installed

import pyqrcode

def QRgenerator(str1):
	str1 = str(str1)
	url = pyqrcode.create(str1)
	url.svg("QRcode.svg", scale=8)


