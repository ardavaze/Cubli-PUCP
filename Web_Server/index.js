let intervalId
let start = false
let freno = false
let ip_rasp
function comenzar(){
    if (start){
        enviarDatos("start","0",1800,function() {
            document.getElementById('btnVelocidad').disabled = true
            document.getElementById('btnAngulo').disabled = true
            document.getElementById('ip_host').disabled=false
            document.getElementById('btnStart').textContent="Comenzar"
            document.getElementById('btnStart').style.backgroundColor="green"
            clearInterval(intervalId);
            document.getElementById('velocidad').innerText = "0";
            document.getElementById('angulo').innerText = "0";
            start=!start;
        })
    }
    else{
        ip_rasp=document.getElementById('ip_host').value
        if(ip_rasp != ""){
            enviarDatos("start","1",1800,function() {
                document.getElementById('btnVelocidad').disabled = false
                document.getElementById('btnAngulo').disabled = false
                document.getElementById('btnStart').textContent="Detener"
                document.getElementById('btnStart').style.backgroundColor="rgb(189, 0, 0)"
                document.getElementById('ip_host').disabled=true
                intervalId=setInterval(obtenerDatos,1000)
                start=!start;
            })
        }
        else{
            alert("Ingrese una ip")
        }
    }
}
function frenado(){
    if (freno){
        enviarDatos("freno","0",700,function() {
            document.getElementById('btnFreno').style.backgroundColor="green";
            freno=!freno;
        })
    }
    else{
        enviarDatos("freno","1",700,function() {
            document.getElementById('btnFreno').style.backgroundColor="rgb(189, 0, 0)";
            freno=!freno;
        })
    }
    
}

function enviarDatosVelocidad() {
    enviarDatos("velocidad",document.getElementById("velocidadInput").value,500,function() {})
}

function enviarDatosAngulo(){

}

function obtenerDatos() {
    recibirDatos("velocidad","velocidad",600)
    recibirDatos("angulo","angulo",600);
}

function enviarDatos(tipo_dato,dato,tiempoEspera,funcion){
    const xhr = new XMLHttpRequest();
    const velocidadInput = dato
    xhr.timeout=tiempoEspera
    // Configura la solicitud POST
    xhr.open("POST", "http://"+ip_rasp+"/"+tipo_dato, true);
	xhr.setRequestHeader("Content-Type", "text/plain");
	body = dato
    xhr.send(body + "\r\n");

    // Maneja la respuesta
    xhr.onreadystatechange = function() {		
        if (xhr.readyState === 4 && xhr.status === 200) {
            funcion()
        }
    };
	xhr.onerror=xhr.abort
}
function recibirDatos(tipo_dato,elementId,tiempoEspera){
    const xhr = new XMLHttpRequest();
    xhr.timeout=tiempoEspera
    xhr.open("GET", "http://"+ip_rasp+"/"+tipo_dato, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById(elementId).innerText = xhr.responseText;
        }
    };
    xhr.send();
    xhr.onerror=xhr.abort
}