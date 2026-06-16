
- Webkit 26.4   (playwright webkit v2306) 
	- webkit的版本，playwright补丁版本
	- webkitgtk2.53.3：gtk版本
- WebKit 26.4  (playwright webkit v2276)

- `https://cdn.playwright.dev/dbazure/download/playwright`
	- `builds/webkit/2276/webkit-win64.zip`
	- `builds/webkit/2306/webkit-ubuntu-24.04.zip`
	- packages\playwright-core\src\server\registry\index.ts，DOWNLOAD_PATHS
	- packages\playwright-core\browsers.json
- 跟踪webkit commit与playwright补丁版本方法
	- 查看对应browser_patches\webkit\UPSTREAM_CONFIG.sh commit时的packages\playwright-core\browsers.json里的版本
	- 但注意，跟踪revision即可，不用跟踪revisionOverrides（特定os的版本）
	- 但也不完全这样，  比如 2272（"2026-03-24 16:57:06 +0000"）-2287（ "2026-05-05 10:28:01 -0700"） 都是webkit 6b34ac51510516bd6a3ec2f5edc97413758d3ab1（"2026-03-30T18:00:14-07:00"），下个版本修改于c8604ecd97ffcc50b6c269df544b7cc36f258d3b（"2026-05-07T10:14:30-07:00"）
		- 2276 "2026-04-03 07:50:45 -0700"
		- 因此严格来说是2276版本才对，不管感觉不用这么准确，就要修改webkit base commit时的playwright webkit补丁版本即可

