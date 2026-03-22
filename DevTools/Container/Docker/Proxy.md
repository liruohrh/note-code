
```bash

# wsl2 get windows host
HOST_IP=$(ip route show default | awk '{ print $3 }')

sudo mkdir -p /etc/systemd/system/docker.service.d/
cat <<EOF | sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf
[Service]
Environment="HTTP_PROXY=http://${HOST_IP}:7890"
Environment="HTTPS_PROXY=http://${HOST_IP}:7890"
Environment="NO_PROXY=localhost,127.0.0.1"
EOF

echo "reloading systemctl daemon..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
echo "restarting docker daemon..."
sudo systemctl restart docker

echo "lookuping docker proxy env..."
systemctl show --property=Environment docker

echo "to cancel proxy, delete /etc/systemd/system/docker.service.d/http-proxy.conf"
```