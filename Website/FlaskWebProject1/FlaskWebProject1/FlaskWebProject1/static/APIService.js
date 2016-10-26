function GetAll(converter) {
    return $.ajax({
        url: "http://localhost:5555/API/Products",
        contentType: 'application/json',
        datatype: 'json'
    });
}
x = GetAll(null);
console.log(x);