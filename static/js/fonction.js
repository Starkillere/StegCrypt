function afficherPassword() { 
    var input = document.getElementById("password");
    if (input.type === "password") { 
        input.type = "text"; 
    } 
    else { 
        input.type = "password"; 
    }  
};

function loadFile(event, image, id="") {
    var fileName = document.getElementById(id).value;
    var idxDot = fileName.lastIndexOf(".") + 1;
    var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
    if (extFile=="jpg" || extFile=="jpeg" || extFile=="png"){
        if (image === 1){
            var output = document.getElementById('output1');

        }
        else if (image === 2) {
            var output = document.getElementById('output2');
        }
        output.src = URL.createObjectURL(event.target.files[0]);
        output.onload = function() {
          URL.revokeObjectURL(output.src)
        }
    }
    else{
        alert("Attention vous avez charger un fichier autre qu'une image de type png ; jpg ;  jpeg");
        file.value = "";
    }
};

function send(ids) {
    document.getElementById('input').value = ids;
};

function capitalize(str) {
    const lower = str.toLowerCase()
    return (str.charAt(0).toUpperCase() + lower.slice(1))
};

function traitement(data) {
    var listdata = data.split(",")
    return (listdata);
};


function preview(event) {
    var output = document.getElementById('output1');
    var platform = capitalize(document.getElementById("platforme").value);
    
    if (data.indexOF(platform) !== -1){
        output.src = "/static/images/logo/"+platform.value+"png"
    };

};


function changer(nb) 
{   
    var amodifier = document.getElementsByClassName("inputTable")
    var validerButton =  document.getElementById("valider");
    var sender = document.getElementById("mode");
    var but_button = document.getElementsByClassName("m_v_t");
    if (nb === 1) {
        for (let i = 0; i < but_button.length; i++) {
            but_button[i].style.display = "none";
        };
        for (let i = 0; i < amodifier.length; i++) {
            amodifier[i].disabled = false;
        };
        validerButton.style.display = "block";
        sender.value = "MODIFIER";
        document.getElementById("supprimer").disabled = true;
        document.getElementById("modifier").disabled = true;
    }

    else {
        sender.value = "ADD";
    };
};

function goingMode(nb)
{
    var champs =  document.getElementById("mode")
    if (nb === 2) {
        var username = document.getElementById("username");
        var mail = document.getElementById("mail")
        mail.disabled = false;
        username.disabled = false;
        document.getElementById("modifier").style.display = "none";
        document.getElementById("supprimer").style.display = "none";
        document.getElementById("new_password").style.display = "none";
        document.getElementById("valider").style.display = "block";
        document.getElementById("annuler").style.display = "block";
        champs.value = "MODIFIER";
    }

    else if (nb === 3) {
        document.getElementById("modifier").style.display = "none";
        document.getElementById("supprimer").style.display = "none";
        document.getElementById("new_password").style.display = "none";
        document.getElementById("valider").style.display = "block";
        document.getElementById("annuler").style.display = "block";
        champs.value = "DELT";
    }
    else if (nb === 4) {
        champs.value = "CHANGE_PASSWORD";
    }

    else if (nb === 1) {
        champs.value = "annuler"
    }
}

function validateFileType(id){
    var file = document.getElementById(id);
    var fileName = document.getElementById(id).value;
    var idxDot = fileName.lastIndexOf(".") + 1;
    var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
    if (extFile=="jpg" || extFile=="jpeg" || extFile=="png"){
        //TO DO
    }else{
        alert("Attention vous avez charger un fichier autre qu'une image de type png ; jpg ;  jpeg");
        file.value = "";
    }   
};