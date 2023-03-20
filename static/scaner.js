async function pass(){
    var ticket_id = document.getElementById("ticket_id").innerHTML;
    var people_to_pass=document.getElementById("people_to_pass").innerHTML;
    formdata = new FormData;
    formdata.append("ticket_id",ticket_id);
    formdata.append("people_to_pass", people_to_pass);
    fetch(API_URL+"/api/checkin",{
        method: 'POST',
        body: formdata
    });
    resume();
}

async function validate(decodedText){
    let result = await httpGet(API_URL+`/api/validate?key=${decodedText}`,decodedText);
    return result;
}

