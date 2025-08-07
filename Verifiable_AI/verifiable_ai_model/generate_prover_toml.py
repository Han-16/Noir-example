import os
import json
import toml


def load_weights(path: str):
    with open(path, "r") as f:
        data = json.load(f)
    return data["scale"], data["params"]


def load_input(path: str):
    with open(path, "r") as f:
        data = json.load(f)
    return data["x"], data["y"]


def to_str_array(arr):
    return [str(v) for v in arr]


def to_str_2d_array(arr2d):
    return [[str(v) for v in row] for row in arr2d]


def generate_prover_data(x, y, scale, params, commitment):
    return {
        "x": to_str_array(x),
        "y": str(y),
        "scale": str(scale),

        "w1": to_str_2d_array(params["0.weight"]),
        "b1": to_str_array(params["0.bias"]),

        "w2": to_str_2d_array(params["2.weight"]),
        "b2": to_str_array(params["2.bias"]),

        "w3": to_str_2d_array(params["4.weight"]),
        "b3": to_str_array(params["4.bias"]),
        "commitment": str(commitment)
    }


def save_toml(data, path):
    with open(path, "w") as f:
        toml.dump(data, f)
    print(f"✅ Prover.toml saved to: {path}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    weights_path = os.path.join(base_dir, "./mock/quantized_weights.json")
    input_path = os.path.join(base_dir, "./mock/input.json")
    output_path = os.path.join(base_dir, "../verifiable_ai_circuit/Prover.toml")

    scale, params = load_weights(weights_path)
    x, y = load_input(input_path)
    # commitment = generate_commitment(params)
    commitment = 0x18166bc733f1dd898c2a61e1c6ec826191fc05be2e5f98289bab3d0ad4717750
    prover_data = generate_prover_data(x, y, scale, params, commitment)
    save_toml(prover_data, output_path)


if __name__ == "__main__":
    main()
