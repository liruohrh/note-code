```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <div id="app">index</div>
    <div>
        <a href="/">index</a>
    </div>
    <div>
        <a href="/a">a</a>
    </div>
    <div>
        <a href="/b">b</a>
    </div>
</body>
<script>
    function goto(href) {
        history.pushState("key=" + href, "", href);
        if (href === "/") {
            document.querySelector('#app').innerHTML = "index";
        } else if (href === "/a") {
            document.querySelector('#app').innerHTML = "a";
        } else if (href === "/b") {
            document.querySelector('#app').innerHTML = "b";
        } else {
            document.querySelector('#app').innerHTML = "404";
        }
        console.log("goto", href, "state", history.state, history.state === "key=" + href);
    }
    document.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function (e) {
            e.preventDefault();
            const url = new URL(e.target.href);
            goto(url.pathname + url.hash + url.search);
        });
    });
    window.addEventListener('load', function (e) {
        // 获取当前的URL
        var url = location.pathname + location.search;
        goto(url);
    });
    window.addEventListener('popstate', function (e) {
        // 获取当前的URL
        var url = location.pathname + location.search;
        console.log("popstate", url, e);
        goto(url);
    });
</script>

</html>
```