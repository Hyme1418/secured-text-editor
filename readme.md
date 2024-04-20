# Secured Text Editor
A text editor that able to do the main functions of a normal text editor, eg., add, delete, modify. Besides these functions, it will be embedded with encryption/decryption functions. The encryption and decryption function is performed automatically once saving or opening a text file.

## How do we implement it?
We are using Fernet which is the symmetric encryption algorithm to implement this project.

How to encrypt?
```
The key is b'cBfZ1TQZFmyn-MiOH8pVFa-qaayGh3QNtcQF6zP6Knk='
Original text: Hello, World!
Encrypted text: b'gAAAAABmIS5DYd7BSZ8DtEP0RdI7J-tof5kO_pBx_0xoFmfPo2z07KbhZFtzDxYHEQgGbrKz1gykfQMw8IUtQC2KraXlplKdjA=='
Decrypted text: Hello, World!
```
1. Using Fernet to generate the secret key which is b'cBfZ1TQZFmyn-MiOH8pVFa-qaayGh3QNtcQF6zP6Knk=' for this test.
2. Translate text for example Hello world to UTF-8 encoding and then encrypt with Fernet key so we will get the encrypted text.

## How to use
Exactly, you can run with `python main.py` to run
> or you can build a .exe file for easy use. 

## Build the .exe file command
`pyinstaller --onefile --windowed --icon=icon.ico main.py`


## Team member
1. Sirasit Puangpathanachai 6488133
2. Thanawat Jarusuthirug 6488178
