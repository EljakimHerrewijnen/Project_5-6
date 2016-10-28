function SendCommand(){
    window.alert("sometext");
    return $.ajax({
        url: "http://localhost:5555/API/Database.py",
        type: 'get_all',
        dataType: "python",
        success: function(response){
           output = response;
           alert(output);}
    }).done(function(data){
        console.log(data);
        alert(data);
    }); 
}