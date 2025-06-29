```bash
PROXY_PORT=7890
WIN_HOST=$(ip route show | grep -i default | awk '{ print $3}')
export WIN_HOST=$WIN_HOST
export http_proxy=http://$WIN_HOST:$PROXY_PORT
export https_proxy=http://$WIN_HOST:$PROXY_PORT
export all_proxy=socks5h://$WIN_HOST:$PROXY_PORT
```