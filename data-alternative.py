import csv

# Define the data for Solana ecosystem Twitter accounts
accounts = [
    # Solana Founders & Core Contributors
    {"Group Name": "Solana Founders & Core Contributors", "Twitter Link": "https://x.com/aeyakovenko", "Name": "Anatoly Yakovenko", "Note": "Co-founder of Solana, creator of the Proof of History consensus"},
    {"Group Name": "Solana Founders & Core Contributors", "Twitter Link": "https://x.com/0xMert_", "Name": "Mert Mumtaz", "Note": "Co-founder of Helius, Solana researcher, former Coinbase engineer"},
    {"Group Name": "Solana Founders & Core Contributors", "Twitter Link": "https://x.com/rogerw Solana", "Name": "Roger Wang", "Note": "Co-founder of Solana, former Stripe engineer"},
    {"Group Name": "Solana Founders & Core Contributors", "Twitter Link": "https://x.com/kevinheas noted", "Name": "Kevin Heasler", "Note": "Early Solana contributor, infrastructure builder"},
    
    # Solana Foundation & Official Accounts
    {"Group Name": "Solana Foundation & Official", "Twitter Link": "https://x.com/solana", "Name": "Solana", "Note": "Official Solana blockchain account"},
    {"Group Name": "Solana Foundation & Official", "Twitter Link": "https://x.com/SolanaFndn", "Name": "Solana Foundation", "Note": "Non-profit dedicated to Solana decentralization and growth"},
    {"Group Name": "Solana Foundation & Official", "Twitter Link": "https://x.com/solana_devs", "Name": "Solana Developers", "Note": "Official Solana developer account"},
    {"Group Name": "Solana Foundation & Official", "Twitter Link": "https://x.com/SuperteamDAO", "Name": "Superteam DAO", "Note": "Solana's global builder community and grant program"},
    
    # DeFi Project Founders & Leaders
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/weremeow", "Name": "Meow", "Note": "Founder of Jupiter, Solana's leading DEX aggregator"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/JupiterExchange", "Name": "Jupiter Exchange", "Note": "Solana's largest DEX aggregator by volume"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/RaydiumProtocol", "Name": "Raydium", "Note": "Leading Solana AMM and liquidity provider"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/Raydium", "Name": "Raydium Team", "Note": "Official Raydium protocol account"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/orca_so", "Name": "Orca", "Note": "User-friendly Solana DEX"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/KaminoFinance", "Name": "Kamino Finance", "Note": "Solana lending and liquidity protocol"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/marginfi", "Name": "Marginfi", "Note": "Solana lending protocol"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/DriftProtocol", "Name": "Drift Protocol", "Note": "Solana perpetuals DEX"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/ZetaMarkets", "Name": "Zeta Markets", "Note": "Solana options and derivatives platform"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/PythNetwork", "Name": "Pyth Network", "Note": "Solana-based oracle network"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/jito_sol", "Name": "Jito", "Note": "Solana MEV and liquid staking solution"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/MarinadeFinance", "Name": "Marinade Finance", "Note": "Solana liquid staking protocol"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/Lifinity_io", "Name": "Lifinity", "Note": "Solana AMM with oracle pricing"},
    {"Group Name": "DeFi Project Leaders", "Twitter Link": "https://x.com/MeteoraAG", "Name": "Meteora", "Note": "Solana dynamic AMM protocol"},
    
    # Wallets & Consumer Apps
    {"Group Name": "Wallets & Consumer Apps", "Twitter Link": "https://x.com/phantom", "Name": "Phantom", "Note": "Leading Solana wallet, multi-chain support"},
    {"Group Name": "Wallets & Consumer Apps", "Twitter Link": "https://x.com/BChillman", "Name": "Brandon Millman", "Note": "CEO & Founder of Phantom Wallet"},
    {"Group Name": "Wallets & Consumer Apps", "Twitter Link": "https://x.com/solflare_wallet", "Name": "Solflare", "Note": "Popular Solana wallet"},
    {"Group Name": "Wallets & Consumer Apps", "Twitter Link": "https://x.com/Backpack", "Name": "Backpack", "Note": "Solana wallet from Mad Lads team"},
    {"Group Name": "Wallets & Consumer Apps", "Twitter Link": "https://x.com/StepFinance_", "Name": "Step Finance", "Note": "Solana portfolio management dashboard"},
    
    # NFT & Marketplace Builders
    {"Group Name": "NFT & Marketplaces", "Twitter Link": "https://x.com/MagicEden", "Name": "Magic Eden", "Note": "Leading multi-chain NFT marketplace"},
    {"Group Name": "NFT & Marketplaces", "Twitter Link": "https://x.com/tensor_hq", "Name": "Tensor", "Note": "Solana NFT trading platform"},
    {"Group Name": "NFT & Marketplaces", "Twitter Link": "https://x.com/metaplex", "Name": "Metaplex", "Note": "Solana NFT protocol and standards"},
    {"Group Name": "NFT & Marketplaces", "Twitter Link": "https://x.com/drip_haus", "Name": "dTeleport", "Note": "Solana NFT platform"},
    {"Group Name": "NFT & Marketplaces", "Twitter Link": "https://x.com/AuroryProject", "Name": "Aurory", "Note": "Solana NFT gaming project"},
    {"Group Name": "NFT & Marketplaces", "Twitter Link": "https://x.com/GenesysGo", "Name": "Genesys Go", "Note": "Degods and Solana NFT creator"},
    
    # Infrastructure & Developer Tools
    {"Group Name": "Infrastructure & Dev Tools", "Twitter Link": "https://x.com/heliuslabs", "Name": "Helius Labs", "Note": "Solana RPC and developer infrastructure"},
    {"Group Name": "Infrastructure & Dev Tools", "Twitter Link": "https://x.com/jump_firedancer", "Name": "Jump Firedancer", "Note": "Solana validator client by Jump"},
    {"Group Name": "Infrastructure & Dev Tools", "Twitter Link": "https://x.com/solanalabs", "Name": "Solana Labs", "Note": "Core Solana development company"},
    {"Group Name": "Infrastructure & Dev Tools", "Twitter Link": "https://x.com/anchorlang", "Name": "Anchor", "Note": "Solana smart contract development framework"},
    {"Group Name": "Infrastructure & Dev Tools", "Twitter Link": "https://x.com/clockwork_xyz", "Name": "Clockwork", "Note": "Solana automation protocol"},
    {"Group Name": "Infrastructure & Dev Tools", "Twitter Link": "https://x.com/streamflow_fi", "Name": "Streamflow", "Note": "Solana token vesting and streaming"},
    {"Group Name": "Infrastructure & Dev Tools", "Twitter Link": "https://x.com/solanafm", "Name": "SolanaFM", "Note": "Solana blockchain explorer"},
    {"Group Name": "Infrastructure & Dev Tools", "Twitter Link": "https://x.com/solanabeach_io", "Name": "Solana Beach", "Note": "Solana validator explorer"},
    
    # Data & Analytics
    {"Group Name": "Data & Analytics", "Twitter Link": "https://x.com/birdeye_so", "Name": "BirdEye", "Note": "Solana token analytics and tracking"},
    {"Group Name": "Data & Analytics", "Twitter Link": "https://x.com/bonfida", "Name": "Bonfida", "Note": "Solana DNS and data services"},
    {"Group Name": "Data & Analytics", "Twitter Link": "https://x.com/openbookdex", "Name": "OpenBook", "Note": "Solana-based orderbook DEX"},
    
    # Gaming & Consumer Projects  
    {"Group Name": "Gaming & Consumer", "Twitter Link": "https://x.com/Stepnofficial", "Name": "STEPN", "Note": "Solana move-to-earn gaming app"},
    {"Group Name": "Gaming & Consumer", "Twitter Link": "https://x.com/ParallelColony", "Name": "Parallel", "Note": "Solana NFT trading card game"},
    {"Group Name": "Gaming & Consumer", "Twitter Link": "https://x.com/oreSupply", "Name": "ORE", "Note": "Solana mining protocol"},
    {"Group Name": "Gaming & Consumer", "Twitter Link": "https://x.com/helium", "Name": "Helium", "Note": "Decentralized wireless network on Solana"},
    {"Group Name": "Gaming & Consumer", "Twitter Link": "https://x.com/Hivemapper", "Name": "Hivemapper", "Note": "Decentralized mapping on Solana"},
    {"Group Name": "Gaming & Consumer", "Twitter Link": "https://x.com/rendernetwork", "Name": "Render Network", "Note": "GPU rendering on Solana"},
    
    # Community & BD
    {"Group Name": "Community & BD", "Twitter Link": "https://x.com/superteam", "Name": "Superteam", "Note": "Solana builder community hub"},
    {"Group Name": "Community & BD", "Twitter Link": "https://x.com/SuperteamEarn", "Name": "Superteam Earn", "Note": "Solana bounties and grants platform"},
    {"Group Name": "Community & BD", "Twitter Link": "https://x.com/SolanaSensei", "Name": "Solana Sensei", "Note": "Solana OG and educator"},
    {"Group Name": "Community & BD", "Twitter Link": "https://x.com/SolanaCollectiv", "Name": "Solana Collective", "Note": "Content creators in Solana ecosystem"},
    {"Group Name": "Community & BD", "Twitter Link": "https://x.com/OrangeDAOxyz", "Name": "Orange DAO", "Note": "YC alumni Web3 investment DAO"},
    {"Group Name": "Community & BD", "Twitter Link": "https://x.com/SquadsProtocol", "Name": "Squads", "Note": "Solana multi-sig wallet for teams"},
    {"Group Name": "Community & BD", "Twitter Link": "https://x.com/MayanFinance", "Name": "Mayan Finance", "Note": "Solana cross-chain bridge"},
    
    # Investors & VCs
    {"Group Name": "Investors & VCs", "Twitter Link": "https://x.com/colosseumorg", "Name": "Colosseum", "Note": "Solana-focused venture capital"},
    {"Group Name": "Investors & VCs", "Twitter Link": "https://x.com/alliancedao", "Name": "AllianceDAO", "Note": "Y Combinator's Web3 accelerator"},
    {"Group Name": "Investors & VCs", "Twitter Link": "https://x.com/BuidlerDAO", "Name": "BuidlerDAO", "Note": "Web3 investment DAO"},
    
    # Additional Key Figures
    {"Group Name": "Key Individuals", "Twitter Link": "https://x.com/therealchaseeb", "Name": "Chase", "Note": "Solana builder and ecosystem contributor"},
    {"Group Name": "Key Individuals", "Twitter Link": "https://x.com/a2kdefi", "Name": "Adam", "Note": "Exchange Art founder, Solana NFT pioneer"},
    {"Group Name": "Key Individuals", "Twitter Link": "https://x.com/joemccann", "Name": "Joe McCann", "Note": "Solana investor and ecosystem supporter"},
    {"Group Name": "Key Individuals", "Twitter Link": "https://x.com/Parcl", "Name": "Parcl", "Note": "Solana real estate price discovery"},
    {"Group Name": "Key Individuals", "Twitter Link": "https://x.com/GooseFX1", "Name": "GooseFX", "Note": "Solana options protocol"},
    {"Group Name": "Key Individuals", "Twitter Link": "https://x.com/solblaze_org", "Name": "SolBlaze", "Note": "Solana liquid staking"},
    {"Group Name": "Key Individuals", "Twitter Link": "https://x.com/tradewithPhoton", "Name": "Photon", "Note": "Solana trading terminal"},
    {"Group Name": "Key Individuals", "Twitter Link": "https://x.com/bonk_inu", "Name": "Bonk", "Note": "Solana community meme token"},
]

import os

# Write to CSV file
os.makedirs('output', exist_ok=True)
with open('output/solana_twitter_accounts.csv', 'w', newline='') as csvfile:
    fieldnames = ['Group Name', 'Twitter Link', 'Name', 'Note']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for account in accounts:
        writer.writerow(account)

print(f"CSV file created with {len(accounts)} accounts")