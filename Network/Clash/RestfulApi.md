


# 简单控制

```js
(async () => {
  const clash = {
    _baseUrl: "http://localhost:9097",
    _token: "123456",
    proxies: [],
    rootProxy: null,
    nowProxy: null,
    fasterProxy: null,
    async _fetch(path, options = {}) {
      return fetch(`${this._baseUrl}${path}`, {
        ...options,
        method: options.method || "GET",
        headers: {
          ...options.headers,
          Authorization: `Bearer ${this._token}`,
        },
      }).then(async res => {
        if (res.status >= 400) {
          const contentLength = Number(res.headers.get("Content-Length"));
          if (contentLength > 0) {
            throw new Error(
              JSON.stringify({
                status: res.status,
                statusText: res.statusText,
                contentLength,
                body: await res.text(),
              })
            );
          }
          throw new Error(res.statusText);
        }
        return res;
      });
    },
    async listProxies() {
      const res = await this._fetch("/proxies");
      const { proxies } = await res.json();
      // Direct,Reject,Selector
      const otherTypes = ["Direct", "Reject", "Selector"];
      const noTypes = ["URLTest", "Fallback", "REJECT-DROP", "LoadBalance", "Relay", "Dns", "PassRule", "Pass"];
      const _proxies = [];
      let rootProxy;
      let history = [];
      for (const key of Object.keys(proxies)) {
        const proxy = proxies[key];
        if (["GLOBAL", "COMPATIBLE"].includes(key) || noTypes.includes(proxy.type)) {
          continue;
        }
        if (proxy.type === "Selector") {
          // must one
          rootProxy = proxy;
          continue;
        }
        if (!proxy.alive) {
          continue;
        }
        const _hs = proxy.history?.filter(e => e.delay).sort(this._sortHistory) || [];
        if (_hs.length > 0) {
          proxy.lastTestHistory = _hs[0];
          if (!otherTypes.includes(proxy.type)) {
            history.push({ ..._hs[0], proxy });
          }
        }
        proxy.area = this._area(proxy);
        _proxies.push(proxy);
      }
      if (_proxies.length === 0) {
        throw new Error("no proxy found");
      }
      if (!rootProxy) {
        throw new Error("rootProxy not found");
      }
      // faster with area or random
      history = history.sort(this._sortHistory);
      let fasterProxyName = "";
      if (history.length > 0) {
        let target = history.find(e => e.proxy.area);
        fasterProxyName = target ? target.name : history[0].proxy.name;
      }
      function simpleProxy(p) {
        if (!p) {
          return p;
        }
        return {
          name: p.name,
          area: p.area,
          lastTestHistory: p.lastTestHistory,
        };
      }
      this.fasterProxy = simpleProxy(
        fasterProxyName
          ? _proxies.find(e => e.name === fasterProxyName)
          : _proxies[Math.ceil(Math.random() * _proxies.length)]
      );

      this.proxies = _proxies.map(simpleProxy);
      this.rootProxy = simpleProxy(rootProxy);
      this.nowProxy = simpleProxy(_proxies.find(e => e.name === rootProxy.now));
      return this.proxies;
    },
    _areaPatterns: [
      { pattern: /港|(hk)/i, area: "香港" },
      { pattern: /台|(tw)/i, area: "台湾" },
      { pattern: /(澳门)|(mac)/i, area: "澳门" },
      { pattern: /新|(sg)/i, area: "新加坡" },
      { pattern: /日|(jp)/i, area: "日本" },
      { pattern: /韩|(kr)/i, area: "韩国" },
      { pattern: /美|(us)/i, area: "美国" },
      { pattern: /英|(gb)/i, area: "英国" },
      { pattern: /法|(fr)/i, area: "法国" },
      { pattern: /德|(de)/i, area: "德国" },
      { pattern: /意|(it)/i, area: "意大利" },
      { pattern: /西|(es)/i, area: "西班牙" },
      { pattern: /波|(pl)/i, area: "波兰" },
      { pattern: /俄|(ru)/i, area: "俄罗斯" },
      { pattern: /印|(in)/i, area: "印度" },
    ],
    _sortHistory(a, b) {
      const aDate = new Date(a.time);
      const bDate = new Date(b.time);
      const diff = Math.floor((bDate - aDate) / 1000);
      if (diff < 60 * 5) {
        return a.delay - b.delay;
      }
      return -diff;
    },
    _area(proxy) {
      const name = proxy.name;
      const pattern = this._areaPatterns.find(e => e.pattern.test(name));
      return pattern?.area || "";
    },
    async healthCheck() {
      await this._fetch(`/providers/proxies/${this.rootProxy.name}/healthcheck`, { method: "GET" });
    },
    async setProxy(name) {
      await this._fetch(`/proxies/${this.rootProxy.name}`, { method: "PUT", body: JSON.stringify({ name: name }) });
    },
    // for ai to list proxy at first time or long time space to set proxy
    async checkAndListProxies() {
      await this.healthCheck();
      await this.listProxies();
      if (!this.nowProxy) {
        await this.setProxy(this.fasterProxy.name);
        await this.listProxies();
      }
    },
  };
  await clash.listProxies();
  console.log("proxies.length", clash.proxies.length);
  console.log("rootProxy", clash.rootProxy.name);
  console.log("nowProxy", clash.nowProxy?.name, clash.nowProxy?.lastTestHistory);
  console.log("fasterProxy", clash.fasterProxy.name, clash.fasterProxy.lastTestHistory);
  if (!clash.nowProxy) {
    await clash.healthCheck();
    await clash.setProxy(clash.fasterProxy.name);
    await clash.listProxies();
    console.log("after setProxy, nowProxy", clash.nowProxy?.name, clash.nowProxy?.lastTestHistory);
  }
})();
```