#!/bin/bash
# need chmod +
echo -e SECRET_KEY="$(openssl rand -hex 32)" >> .env;
source .venv/bin/activate;
pip freeze >> requirements.txt;
deactivate;
sudo docker network create -d bridge market_backend;
sudo docker compose up;
sudo docker stop $(sudo docker ps -a -q);
sudo docker rm $(sudo docker ps -a -q);
sudo docker rmi $(sudo docker images --format="{{.Repository}} {{.ID}}" |
                  grep "^backmarket" | cut -d' ' -f2);
sudo docker network rm "market_backend";
sudo rm -r dump/;
sudo rm requirements.txt;
echo "$(sed '$d' .env)" > .env;