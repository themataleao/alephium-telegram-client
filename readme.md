# Alephium telegram docker service

This service will send you a message to a dedicated telegram bot whenever you earn money with your mining rig.
Just enter your credentials in the scheduler.py file and start the scheduled service with the follwoing command:

```bash
docker-compose -f docker-compose.yml -f docker-compose.gpu-miner.yml -f docker-compose.scheduler.yml up
```
or you could also use the start-docker-node.sh script. Give it access with `chmod +x start-docker-node.sh``

```bash
./start-docker-node.sh
```

Enjoy the rewards.

# Alephium node and miner installation guide

1. Download Nvidia-docker
2. install docker-compose
3. Run `git clone https://github.com/alephium/alephium.git`
4. Go to `alephium/docker/` directory
5. Run `docker-compose up -d` to run the node
6. Open the swagger ui in a browser http://127.0.0.1:12973/docs
7. Create miner wallet at the swagger endpoint `/wallets` with the `isMiner` in the json:
```json
{
    "password": "123456",
    "walletName": "bar",
    "isMiner": true
}
```
8. Go to wallets/bar/addresses and get your mining addresses
```json
{
  "activeAddress": "18xRk6dY3ozPpSmdKqA7xYgncB6mR5QtgV512N6FU2mPr",
  "addresses": [
    "1HA4d4YpHZwbCvCMwFiXATzSj2M5BJSL8wt3XSR7PaXGk",
    "18cRGxiEMvhCBMZTA9FhFX1LXkRYaVM4BvBE971uUQ6zt",
    "18zntGYAHjbo6EPoe3aWQdfVF4twxQwPLn3bGq5tzG4Mq",
   "18xRk6dY3ozPpSmdKqA7xYgncB6mR5QtgV512N6FU2mPr"
  ]
}
```
9. Add the addresses to your user-mainnet.conf in the docker directory. It should look then something like (Keep addresses in same order as above):
```conf
alephium.api.network-interface = “0.0.0.0"
alephium.mining.api-interface = “0.0.0.0"
alephium.mining.miner-addresses = [
  "1HA4d4YpHZwbCvCMwFiXATzSj2M5BJSL8wt3XSR7PaXGk",
  "18cRGxiEMvhCBMZTA9FhFX1LXkRYaVM4BvBE971uUQ6zt",
  "18zntGYAHjbo6EPoe3aWQdfVF4twxQwPLn3bGq5tzG4Mq",
  "18xRk6dY3ozPpSmdKqA7xYgncB6mR5QtgV512N6FU2mPr"
]
```
9. Run `docker-compose down` in the docker directory to stop the node
10. Run `docker-compose -f docker-compose.yml -f docker-compose.gpu-miner.yml up` to start the node and the gpu miner
11. Wait until the clique is synced. The gpu miner should start automatically
12. You could add the -d flag to the docker-compose statements. (Good for debugging)
13. Enjoy!