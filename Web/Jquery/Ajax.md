```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Juqery</title>
    <script src="https://code.jquery.com/jquery-1.12.3.min.js"></script>
    <!-- <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script> -->
</head>

<body>

    <script>
        $(document).ready(function () {
            $.ajax({ url: "/res.txt", type: "GET" })
                //每次参数都是 响应体（如果contentType=application/json则自动反序列化）, errorCode(基本是"success"), xhr
                .done((...args) => console.log("/res.txt: done", args))
                .done(e => console.log("/res.txt: done2"))
                .always((...args) => console.log("/res.txt: always", args))
                .always(e => console.log("/res.txt: always2"))
                .success((...args) => console.log("/res.txt: success", args))
                .success(e => console.log("/res.txt: success2"))
                .complete((...args) => console.log("/res.txt: complete", args))
                //每次参数都是 xhr, errorCode(基本是"success")
                .complete(e => console.log("/res.txt: complete2"));
            $.ajax({ url: "/res", type: "GET" })
                //每次参数都是 xhr, errorCode, Error
                .error((...args) => console.log("error:  /res.txt: error", args))
                .fail((...args) => console.log("error:  /res.txt: fail", args))
                .always((...args) => console.log("error:  /res.txt: always", args))
                //每次参数都是 xhr, errorCode
                .complete((...args) => console.log("error:  /res.txt: complete", args));

            //回调不能是async函数，如果是async则无法被执行
            $.ajax({ url: "/res.txt", type: "GET" })
                .done((...args) => {
                    console.log("/res: done", args);
                })
                .error((...args) => {
                    console.log("/res: error", args);
                })
                .done(async (...args) => {
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    console.log("/res: async, done", args);
                })
                .error(async (...args) => {
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    console.log("/res: async, error", args);
                })
                .always(async (...args) => {
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    console.log("/res: async, always", args);
                });

            //正确执行async的方法
            async function ajax() {
                return $.ajax(...arguments)
            }
            ajax({ url: "/res.txt", type: "GET" })
                .then(async function (res) {
                    //因为Promise仅接收第一个参数，因此参数仅仅只是响应体（如果contentType=application/json则自动反序列化）
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    console.log("async: right way", typeof res, arguments, res);
                });
            ajax({ url: "/res", type: "GET" })
                .catch(function (e) {
                    //因为Promise仅接收第一个参数，因此参数仅仅只是xhr
                    console.log("async: error", e, arguments);
                });

            async function ajax2() {
                return new Promise((resolve, reject) => {
                    $.ajax(...arguments)
                        .done(function () { resolve(arguments) })
                        .fail(function () { reject(arguments) });
                });
            }
            ajax2({ url: "/res.txt", type: "GET" })
                .then(async function () {
                    //参数仅仅只是响应体（如果contentType=application/json则自动反序列化）
                    await new Promise(resolve => setTimeout(resolve, 2000));
                    console.log("ajax2: right way", ...arguments);
                });
            ajax2({ url: "/res", type: "GET" })
                .catch(function () {
                    //参数仅仅只是xhr
                    console.log("ajax2: error", ...arguments);
                });
        });
    </script>
</body>

</html>
```