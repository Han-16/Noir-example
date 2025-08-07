import { loadFixture } from "@nomicfoundation/hardhat-toolbox-viem/network-helpers";
import { expect } from "chai";
import hre from "hardhat";
import path from "path";
import fs from "fs";

describe("HonkVerifier Deployment", function () {
  async function deployHonkVerifierFixture() {
    const [deployer] = await hre.viem.getWalletClients();
    const publicClient = await hre.viem.getPublicClient();

    const honkVerifier = await hre.viem.deployContract("HonkVerifier");

    return {
      honkVerifier,
      deployer,
      publicClient,
    };
  }

  it("should deploy HonkVerifier contract successfully", async function () {
    const { honkVerifier } = await loadFixture(deployHonkVerifierFixture);

    console.log("✅ Deployed HonkVerifier at:", honkVerifier.address);
  });
});



describe("HonkVerifier Verify", function () {
  async function deployHonkVerifierFixture() {
    const [deployer] = await hre.viem.getWalletClients();
    const publicClient = await hre.viem.getPublicClient();

    const honkVerifier = await hre.viem.deployContract("HonkVerifier");

    return {
      honkVerifier,
      deployer,
      publicClient,
    };
  }

  it.only("should verify proof using Proof.json", async function () {
    const { honkVerifier } = await loadFixture(deployHonkVerifierFixture);

    const proofPath = path.join(__dirname, "./mock/proof.json");
    const proofData = JSON.parse(fs.readFileSync(proofPath, "utf-8"));

    const proof = proofData.proof as `0x${string}`;
    if (typeof proof !== "string" || !proof.startsWith("0x")) {
      throw new Error("❌ Invalid proof format in Proof.json (must be 0x-prefixed hex string)");
    }

    const publicInputs = proofData.public_input as `0x${string}`[];
    if (
      !Array.isArray(publicInputs) ||
      !publicInputs.every((input) => typeof input === "string" && input.startsWith("0x") && input.length === 66)
    ) {
      throw new Error("❌ public_input must be an array of 0x-prefixed 32-byte hex strings");
    }

    const result = await honkVerifier.read.verify([proof, publicInputs]);

    console.log("✅ Verify result:", result);
    expect(result).to.be.true;
  });
});