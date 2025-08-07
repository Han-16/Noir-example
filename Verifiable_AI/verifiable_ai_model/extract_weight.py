import os
import json
import torch
import numpy as np


MODEL_PATH = os.path.join(os.path.dirname(__file__), "./mock/MNIST.pth")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "./mock/quantized_weights.json")
SCALE = 1000


def build_model():
    return torch.nn.Sequential(
        torch.nn.Linear(784, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 10),
    )


def load_model_weights(model, path):
    state_dict = torch.load(path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model


def quantize_weights(model, scale):
    quantized = {}
    for name, param in model.named_parameters():
        arr = param.detach().numpy()
        quantized[name] = (arr * scale).astype(int).tolist()
    return quantized


def save_weights_json(params, scale, output_path):
    data = {
        "scale": scale,
        "params": params
    }
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Quantized weights saved to: {output_path}")


def main():
    model = build_model()
    model = load_model_weights(model, MODEL_PATH)
    quantized_params = quantize_weights(model, SCALE)
    save_weights_json(quantized_params, SCALE, OUTPUT_PATH)


if __name__ == "__main__":
    main()
