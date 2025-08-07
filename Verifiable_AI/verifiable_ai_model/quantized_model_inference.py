import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
import random


def load_weights(path: str):
    with open(path, "r") as f:
        data = json.load(f)
    return data["scale"], data["params"]


def linear_layer(x, w, b, scale, apply_relu=True):
    outputs = []
    for weights, bias in zip(w, b):
        acc = sum(xi * wi for xi, wi in zip(x, weights))
        acc = acc // scale + bias
        outputs.append(max(0, acc) if apply_relu else acc)
    return outputs


def inference(x_int, params, scale):
    x1 = linear_layer(x_int, params["0.weight"], params["0.bias"], scale)
    x2 = linear_layer(x1, params["2.weight"], params["2.bias"], scale)
    logits = linear_layer(
        x2, params["4.weight"], params["4.bias"], scale, apply_relu=False
    )
    return np.argmax(logits)


def visualize_image(image, label):
    plt.imshow(image.squeeze(), cmap="gray")
    plt.title(f"Label: {label}")
    plt.axis("off")
    plt.show()


def save_input_json(x_int, label, save_path):
    input_data = {
        "x": x_int.tolist(),
        "y": int(label)
    }
    with open(save_path, "w") as f:
        json.dump(input_data, f, indent=2)
    print(f"📁 input.json saved to: {save_path}")


def main(sample_index=None):
    if sample_index is None:
        sample_index = random.randint(1, 10000)

    # Load weights
    base_dir = os.path.dirname(__file__)
    weight_path = os.path.join(base_dir, "./mock/quantized_weights.json")
    input_path = os.path.join(base_dir, "./mock/input.json")

    scale, params = load_weights(weight_path)

    # Load dataset
    dataset = MNIST(root="./", train=False, download=True, transform=ToTensor())
    x_img, label = dataset[sample_index]
    # visualize_image(x_img, label)
    # Preprocess input
    x = x_img.view(-1).numpy()
    x_int = (x * scale).astype(int)

    # Inference
    pred = inference(x_int, params, scale)
    print(f"예측값: {pred}, 실제값: {label}")

    # Save input.json
    save_input_json(x_int, pred, input_path)


if __name__ == "__main__":
    index = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(index)