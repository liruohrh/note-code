

```yaml
# 解决DNS泄露问题，代理目标的DNS查询应该走代理，否则走了本地ISP
dns:
  enable: true
  listen: ':53'
  prefer-h3: false
  respect-rules: false
  use-hosts: false
  use-system-hosts: false
  ipv6: true
  enhanced-mode: 'fake-ip'
  # 不直接响应真实ip是为了避免一个IP多域名以及缓存问题而实现的一对一绑定
  fake-ip-range: '198.18.0.1/16'
  fake-ip-filter-mode: 'blacklist'
  fake-ip-filter:
    - '*.lan'
    - '*.local'
    - '*.arpa'
    - 'time.*.com'
    - 'ntp.*.com'
    - 'time.*.com'
    - '+.market.xiaomi.com'
    - 'localhost.ptlogin2.qq.com'
    - '*.msftncsi.com'
    - 'www.msftconnecttest.com'
  # default-nameserver解析dns服务器ip，nameserver用于直连、proxy-server-nameserver用于代理
  default-nameserver:
    - 'system'
    - '223.6.6.6'
    - '8.8.8.8'
    - '2400:3200::1'
    - '2001:4860:4860::8888'
  proxy-server-nameserver:
    - 'https://doh.pub/dns-query'
    - 'https://dns.alidns.com/dns-query'
    - 'tls://223.5.5.5'
  nameserver:
    - '8.8.8.8'
    - 'https://doh.pub/dns-query'
    - 'https://dns.alidns.com/dns-query'
  fallback-filter:
    geoip: true
    geoip-code: 'CN'
    ipcidr:
      - '240.0.0.0/4'
      - '0.0.0.0/32'
    domain:
      - '+.google.com'
      - '+.facebook.com'
      - '+.youtube.com'
  fallback: []
  direct-nameserver: []
  direct-nameserver-follow-policy: false



proxy-groups:
  - name: "auto"
    # 间隔测试且选择最低延迟节点
    # 可固定, 当固定节点不alive时，则依然使用url-test算法
    type: url-test
    proxies:
      - proxyName
    # 仅当 当前节点 old > new + tolerance 时才切换节点
    # tolerance: 150
    url: "https://cp.cloudflare.com/generate_204"
    # 当健康检查返回状态码与期望值不符时，认为节点不可用
    # expected-status: 204
    # healthCheck 间隔时间
    interval: 300
    # lazy时仅当代理组在间隔touch之间不超过这个间隔时间才 healthCheck
	# lazy: true

  - name: "fallback-auto"
    # 按顺序选第一个alive的
    # 可固定, 当固定节点不alive时，取消固定，本次则使用第一个
    type: fallback
    proxies:
      - proxyName
    url: "https://cp.cloudflare.com/generate_204"
    interval: 300

  # load-balance 将按照算法随机选择节点
  - name: "load-balance"
    type: load-balance
    proxies:
      - ss1
      - ss2
      - vmess1
    url: "https://cp.cloudflare.com/generate_204"
    interval: 300
  # strategy: consistent-hashing # 可选 round-robin 和 sticky-sessions
  # select 用户自行选择节点
  - name: Proxy
    type: select
    # disable-udp: true
    proxies:
      - ss1
      - ss2
      - vmess1
      - auto
    # default-selected: ss1 # 默认选择的节点（该项为空或者设置的节点名不存在时，默认选择组中第一个节点）

  - name: UseProvider
    type: select
    filter: "HK|TW" # 正则表达式，过滤 provider1 中节点名包含 HK 或 TW
    use:
      - provider1
    proxies:
      - Proxy
      - DIRECT
    # empty-fallback: COMPATIBLE # 设置当组为空时的回退proxy（这里不支持填写代理组，只支持填写proxy名称）

```