async function fill(){
    let data=document.getElementById('filler').value
    console.log(data)

    const name_re = new RegExp('[А-Яа-яЁё]+ [А-Яа-яЁё]+ *[А-Яа-яЁё]*')
    const phone_re = new RegExp('[\+]?[(]?[0-9]{3}[)]?[-\\s\.]?[0-9]{3}[-\\s\.]?[0-9]{4,6}')
    const email_re = new RegExp('[\\w.!#$%&\'*+-/=?^_`{|}~]+@\\w+.\\w+')
    let full_name=name_re.exec(data)
    let phone=phone_re.exec(data)
    let email=email_re.exec(data)

    console.log(full_name)
    console.log(phone)

    console.log(email)
    if (full_name!=null){
      let name_array=full_name[0].split(' ')
      document.getElementById('surname').value=name_array[0]
      document.getElementById('name').value=name_array[1]
      document.getElementById('patronymic').value=name_array[2]
    }
    
    document.getElementById('phone').value=phone
    document.getElementById('email').value=email


  }

  async function pass(){
    
      var name=document.getElementById('name').value
      var surname=document.getElementById('surname').value
      var patronymic=document.getElementById('patronymic').value
      var phone=document.getElementById('phone').value
      var email=document.getElementById('email').value

      formdata = new FormData;
      formdata.append("name",name);
      formdata.append("surname", surname);
      formdata.append("patronymic",patronymic);
      formdata.append("phone", phone);
      formdata.append("email", email);

      const response = await fetch(API_URL+"/api/generate",{
        method: 'POST',
        body: formdata
      });
      const blob = await response.blob()
      console.log(blob)
      try {
        await navigator.clipboard.write([new ClipboardItem({'image/png':blob})])
        document.getElementById("clipboard_status").innerHTML = "Скопировано в буфер обмена"
        document.getElementById("clipboard_status").className = "buttonnn"
      } catch(err){
        
      }
      var img_url=URL.createObjectURL(blob)
      document.getElementById('ticket').src=img_url
  }
  
  
