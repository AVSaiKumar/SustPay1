from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import b64decode, b64encode

def sign_message(message, private_key_path='private_key.pem'):
    # Load private key from the PEM file
    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    # Sign the message using ECDSA
    signature = private_key.sign(
        message.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )

    # Convert the DER representation to base64 for easy storage or transmission
    signature_base64 = b64encode(signature).decode('utf-8')

    return signature_base64

def verify_signature(message, signature_base64, public_key_path='public_key.pem'):
    # Load public key from the PEM file
    with open(public_key_path, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    # Decode the base64 signature
    signature = b64decode(signature_base64)

    # Verify the message and signature using ECDSA
    try:
        public_key.verify(
            signature,
            message.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        print("Signature verification succeeded.")
    except Exception as e:
        print("Signature verification failed:", e)

if __name__ == "__main__":
    # Message to sign
    pk=input("senders public key here ")
    amount=int(input("balance here"))
    index=int(input("index here"))
    message_to_sign = pk+"-"+str(amount)+"-"+str(index)

    # Create the ECDSA signature using the private key
    signature = sign_message(message_to_sign)

    print("Original Data:", message_to_sign)
    print("ECDSA Signature (DER Representation):", signature)

    # Verify the signature using the public key
    verify_signature(message_to_sign, signature)

