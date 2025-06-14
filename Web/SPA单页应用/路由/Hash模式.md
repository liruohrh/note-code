
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
        <a href="#">index</a>
    </div>
    <div>
        <a href="#a">a</a>
    </div>
    <div>
        <a href="#b">b</a>
    </div>
</body>
<script>
    function goto(url) {
        if (!url) {
            document.querySelector('#app').innerHTML = 'index';
        } else if (hash === 'a') {
            document.querySelector('#app').innerHTML = 'a';
        } else if (hash === 'b') {
            document.querySelector('#app').innerHTML = 'b';
        } else {
            document.querySelector('#app').innerHTML = '404';
        }
    }
    window.addEventListener('hashchange', function () {
        goto(location.hash.substring(1));
    });
    window.addEventListener('load', function (e) {
        goto(location.hash.substring(1));
    });
</script>

</html>
```