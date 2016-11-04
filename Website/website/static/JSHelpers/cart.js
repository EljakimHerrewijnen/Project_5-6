
function storedata(product)
{
    localStorage.setItem("product", product);
}

function getshoppingcart()
{
    var product = localStorage.getItem("product");
    console.log(product);
    var productobject = JSON.parse(product);
}
