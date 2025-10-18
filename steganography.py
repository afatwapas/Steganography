import numpy as np
from PIL import Image

# ------------------ Embed Function ------------------
def embed_data(image_path, secret_message, output_path):
    """
    Embed a secret message into an image using  LSB steganography.
    """
    # Load image and convert to RGB numpy array
    image = Image.open(image_path).convert('RGB')
    data = np.array(image, dtype=np.uint8)

    # Add delimiter and convert message to binary
    secret_message += "###"
    binary_data = ''.join(format(ord(char), '08b') for char in secret_message)
    total_bits = len(binary_data)

    # Flatten pixel data
    flat_data = data.flatten()

    if total_bits > len(flat_data):
        raise ValueError("Message too large to fit in the image!")

    # Convert binary data to numpy array of bits
    bit_array = np.array(list(binary_data), dtype=np.uint8)

    # Modify least significant bits (ensure uint8 arithmetic)
    flat_data[:total_bits] = (flat_data[:total_bits] & 0b11111110) | bit_array
    flat_data = np.clip(flat_data, 0, 255).astype(np.uint8)

    # Reshape and save
    encoded_data = flat_data.reshape(data.shape)
    encoded_img = Image.fromarray(encoded_data)
    encoded_img.save(output_path)

    print(f"[✅] Secret message embedded successfully!\nSaved as: {output_path}")


# ------------------ Extract Function ------------------
def extract_data(image_path):
    """
    Extract a hidden message from an image using  LSB decoding.
    """
    image = Image.open(image_path).convert('RGB')
    data = np.array(image, dtype=np.uint8)

    # Extract least significant bits
    bits = data.flatten() & 1

    # Reconstruct bytes from bits
    bytes_ = ["".join(map(str, bits[i:i + 8])) for i in range(0, len(bits), 8)]
    message = "".join(chr(int(b, 2)) for b in bytes_)

    # Stop at delimiter
    end_index = message.find("###")
    if end_index == -1:
        raise ValueError("No hidden message found or image not encoded with this tool.")
    return message[:end_index]



if __name__ == "__main__":
    print("  Steganography Tool ")
    task = input("Type 'embed' to hide a message or 'extract' to retrieve one: ").strip().lower()

    try:
        if task == "embed":
            image_path = input("Enter input image path (PNG recommended): ").strip()
            secret_message = input("Enter the secret message to embed: ").strip()
            output_path = input("Enter output image path (e.g., stego.png): ").strip()
            embed_data(image_path, secret_message, output_path)

        elif task == "extract":
            image_path = input("Enter the path of the stego image: ").strip()
            hidden_message = extract_data(image_path)
            print(f"\n Extracted Message: {hidden_message}")

        else:
            print("[❌] Invalid input. Please type 'embed' or 'extract'.")

    except FileNotFoundError:
        print("[❌] File not found. Please check the image path.")
    except ValueError as e:
        print(f"[⚠️] {e}")
    except Exception as e:
        print(f"[❌] Unexpected error: {e}")
