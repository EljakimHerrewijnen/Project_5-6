
/*
function* GetOrder() {
    var products = yield* getProducts();
    products = products.next(products);
    while (!products.done) {
        yield;
        products = products.value.next();
    }
    console.log(products.value);
}

function waitFor(func) {
    var b = func.next();
    if (!b.done) {
        window.setTimeout(waitFor, 300, func);
    }
}

function* getProducts() {
    var call = apiCall("GET", "http://localhost:5555/API/Products");
    var result = call.next();
    if (result.done) {
        return ob[id] = result;
    } else {
        yield self;
    }
}

function* apiCall(type, url) {
    var req = new XMLHttpRequest();
    req.open(type, url, true);
    req.responseType = "json";
    req.send();
    while (req.readyState != 4) {
        console.log("yielded");
        yield false;
        
    }
    console.log(req.response);
    return req.response;
}

waitFor(GetOrder());*/

function* apiCall(type, url) {
    var req = new XMLHttpRequest();
    req.open(type, url, true);
    req.responseType = "json";
    req.send();
    while (req.readyState != 4) {
        yield false;
    }
    return req.response;
} 

function* test() {
    var result = yield login();
    console.log(result);
    result = yield apiCall("GET", "http://localhost:5555/API/Products");
}

function* login() {
    var req = new XMLHttpRequest();
    req.open('POST', '/api/login', true);
    req.setRequestHeader("Content-Type", "application/json");
    req.responseType = "json";
    req.send("{username: test, password: test}");
    while (req.readyState != 4) {
        yield false;
    }
    return req.response;
}

function AsyncGenerator(generator) {
    var stack = [];
    function pushStack(generator, result) {
        stack.push({"generator" : generator, "result" : result});
    }

    function updateResult(result) {
        currentStackItem().result = result;
    }

    function popStack() {
        stack.pop();
    }

    function step(value) {
        var currentItem = currentStackItem();
        var x = currentItem.generator.next(value)
        updateResult(x);
    }

    function currentStackItem() {
        return stack[stack.length-1]
    }

    function execute() {
        if (stack.length < 1) return;
        var currentItem = currentStackItem();
        var result = currentItem.result;
        if (stack.length == 1 && result.done) return result.value;

        if (result.done) {
            popStack();
            step(result.value);
            execute();
        } else {
            if (result.value.next) {
                pushStack(result.value, result.value.next());
            }
            step(result.value);
            window.setTimeout(execute, 0);
        }
    }
    pushStack(generator, generator.next());
    execute();
}

AsyncGenerator(test())