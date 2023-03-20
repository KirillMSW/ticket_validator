async function void_ticket(){
          
    var ticket_id=document.getElementById('ticket_id').value
    

    formdata = new FormData;
    formdata.append("ticket_id",ticket_id);

    const response = await fetch(API_URL+"/api/void",{
      method: 'POST',
      body: formdata
    });
    let text = await response.text()
    if (text == "OK"){
        document.getElementById("no_such_ticket").style.display = "none";
        document.getElementById("success").style.display = "initial";
    }
    else{
        document.getElementById("success").style.display = "none";
        document.getElementById("no_such_ticket").style.display = "initial";
    }
}