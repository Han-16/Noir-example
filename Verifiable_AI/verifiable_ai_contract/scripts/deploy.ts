import hre from "hardhat"
import fs from "fs"
import path from "path"

async function main() {
  const [deployer] = await hre.viem.getWalletClients()
  const publicClient = await hre.viem.getPublicClient()

  const verifier = await hre.viem.deployContract("HonkVerifier")
  console.log("✅ HonkVerifier deployed at:", verifier.address)

  const outputPath = path.join(__dirname, "../test/mock/deployed_address.json")
  fs.writeFileSync(outputPath, JSON.stringify({ address: verifier.address }, null, 2))
  console.log("📁 Address saved to:", outputPath)
}

main().catch((err) => {
  console.error("❌ Deployment failed:", err)
  process.exit(1)
})