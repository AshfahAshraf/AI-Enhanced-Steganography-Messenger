# AI-Enhanced-Steganography-Messenger
This project is all about secure communication in the digital age. We built a tool that lets people hide secret messages inside AI-generated images, making it really hard for anyone to even know there’s a hidden message.

Instead of using regular images, we used Stable Diffusion (via Hugging Face) to create custom images from text prompts. Then, we applied LSB steganography to embed the message, and AES encryption to keep the message secure even if someone extracts it.

It works like this:

Type a prompt → get a unique image.

Add your secret message → it gets encrypted and hidden in the image.

Share the image.

The recipient uses a key to safely decode the hidden message.

We built the whole thing in Python, designed a user-friendly interface with PyQt, and learned a lot about combining AI, cryptography, and secure design.

🛠 Tech Stack:
Python

AES Encryption

Hugging Face (Stable Diffusion)

PyQt

LSB Steganography
