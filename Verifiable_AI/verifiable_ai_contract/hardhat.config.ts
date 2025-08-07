import type { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox-viem";
require("hardhat-gas-reporter");
import "@nomicfoundation/hardhat-ethers";


const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.27",
    settings: {
      optimizer: {
        enabled: true,
        runs: 50,
      },
    },
  },
  networks: {
    hardhat: {
      hardfork: "berlin",
    },
  },
  gasReporter: {
    enabled: true,
    currency: "USD",
    coinmarketcap: "",
    token: "ETH",
    showTimeSpent: true,
    excludeContracts: [],
  },
};

export default config;
