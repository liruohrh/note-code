
# Perfs


- doh
	- network.trr.custom_uri：doh服务器，必须设置
	- network.trr.default_provider_uri：默认是https://mozilla.cloudflare-dns.com/dns-query
	- |network.trr.mode
		- 0：自动
		- 2：DOH失败用Do53
		- 3：仅用DOH
		- 5：关闭