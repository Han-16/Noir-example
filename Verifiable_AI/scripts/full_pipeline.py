import os
import subprocess
import json
import shutil
import toml
import random
import sys
from web3 import Web3


def run_model_inference(sample_index=None):
    print("\n📦 Running quantized model inference...")
    if sample_index is None:
        sample_index = random.randint(1, 10000)
    print(f"➡️ Using sample index: {sample_index}")

    base_dir = os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(base_dir, "../verifiable_ai_model/quantized_model_inference.py")
    subprocess.run([sys.executable, script_path, str(sample_index)], check=True)


def generate_prover_toml():
    print("\n🛠️ Generating Prover.toml...")
    base_dir = os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(base_dir, "../verifiable_ai_model/generate_prover_toml.py")
    subprocess.run([sys.executable, script_path], check=True)


def run_proof_generation():
    print("\n🧠 Generating proof with Nargo & bb...")
    base_dir = os.path.abspath("./verifiable_ai_circuit")

    subprocess.run(["nargo", "execute"], cwd=base_dir, check=True)

    prove_cmd = [
        "bb", "prove",
        "-b", "./target/verifiable_ai_circuit.json",
        "-w", "./target/verifiable_ai_circuit.gz",
        "-o", "./target",
        "--oracle_hash", "keccak",
        "--output_format", "bytes_and_fields"
    ]
    subprocess.run(prove_cmd, cwd=base_dir, check=True)


def extract_proof_hex():
    print("\n🔍 Extracting proof in hex format...")
    target_dir = os.path.abspath("./verifiable_ai_circuit/target")
    proof_path = os.path.join(target_dir, "proof")

    with open(proof_path, "rb") as f:
        proof_bytes = f.read()

    proof_hex = "0x" + proof_bytes.hex()
    return proof_hex


def generate_proof_json(proof_hex):
    print("\n📄 Writing proof.json...")
    circuit_target_dir = os.path.abspath("./verifiable_ai_circuit/target")
    verifier_proof_path = os.path.abspath("./verifiable_ai_contract/test/mock/proof.json")

    with open(os.path.join(circuit_target_dir, "public_inputs_fields.json"), "r") as f:
        public_inputs = json.load(f)

    proof_json = {
        "proof": proof_hex,
        "public_input": public_inputs
    }

    os.makedirs(os.path.dirname(verifier_proof_path), exist_ok=True)
    with open(verifier_proof_path, "w") as f:
        json.dump(proof_json, f, indent=2)
    print(f"✅ proof.json written to: {verifier_proof_path}")

def send_verify_transaction():
    print("\n🚀 Sending verify transaction to Verifier contract...")

    # Set up paths
    base_dir = os.path.abspath(os.path.dirname(__file__))
    contract_info_path = os.path.join(base_dir, "../verifiable_ai_contract/test/mock/deployed_address.json")
    proof_path = os.path.join(base_dir, "../verifiable_ai_contract/test/mock/proof.json")
    abi_path = os.path.join(base_dir, "../verifiable_ai_contract/artifacts/contracts/Verifier.sol/HonkVerifier.json")

    # Connect to local RPC
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    if not w3.is_connected():
        raise RuntimeError("❌ Could not connect to local RPC node")

    # Load contract address, ABI, and proof data
    with open(contract_info_path, "r") as f:
        contract_address_raw = json.load(f)["address"]
        contract_address = Web3.to_checksum_address(contract_address_raw)

    with open(abi_path, "r") as f:
        abi = json.load(f)["abi"]

    with open(proof_path, "r") as f:
        proof_data = json.load(f)
        proof = proof_data["proof"]
        public_input = proof_data["public_input"]

    # Create contract instance
    contract = w3.eth.contract(address=contract_address, abi=abi)

    # Call view function
    print("🔍 Calling verify() to check proof validity...")
    result = contract.functions.verify(proof, public_input).call()
    if result:
        print("✅ Proof is valid!")
    else:
        print("❌ Proof is invalid!")



def main():
    sample_index = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run_model_inference(sample_index)
    generate_prover_toml()
    run_proof_generation()
    proof_hex = extract_proof_hex()
    generate_proof_json(proof_hex)
    send_verify_transaction()


if __name__ == "__main__":
    main()
