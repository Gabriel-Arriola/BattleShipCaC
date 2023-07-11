const gridContainer = document.querySelector('.grid-container');

if (gridContainer != null){
    // Crear la matriz de 4x4
    for (let i = 0; i < 10; i++) {
        for (let j = 0; j < 10; j++) {
            const gridItem = document.createElement('div');
            gridItem.className = 'grid-item';
            // Agregar evento de clic al div
            gridItem.addEventListener('click', function () {
                sessionStorage.setItem('coordenada', this.id);
                if (sessionStorage.getItem("userid") == null) {
                    alert("Debes iniciar sesión para jugar!");
                }
                else if (sessionStorage.getItem("partida") == null) {
                    alert("Debes iniciar una partida para jugar!");
                }
                else
                    disparo();
            });

            // Asignar un ID numérico incremental
            gridItem.id = i.toString().concat(j.toString());

            gridContainer.appendChild(gridItem);
        }
    }
}

const register = async () => {
    let usrname = document.getElementById("registerUsername").value;
    let passwd = document.getElementById("registerPassword").value;
    let mail = document.getElementById("registerEmail").value; 
    try {
        const respuesta = await axios.post('https://arriolagabriel.pythonanywhere.com/register', {
            params: {
                username: usrname,
                email: mail,
                password: passwd
            },
        })
        console.log(respuesta.data);
        sessionStorage.setItem('userid', respuesta.data.user_id);
        alert('Usuario registrado exitosamente... \n Bienvenido a bordo! ' + usrname);
        location.href = './index.html';
    } catch (error) {
        console.log("PROBLEMA", error.response.status);
        if(error.response.status == 409)
            alert("ERROR, usuario o email ya registrado.");
        else
            alert("ERROR, intenta nuevamente.");
    }
}

const login = async () => {
    let usrname = document.getElementById("login_username").value;
    let passwd = document.getElementById("login_password").value;
    try {
        const respuesta = await axios.post('https://arriolagabriel.pythonanywhere.com/login', {
            params: {
                username: usrname,
                password: passwd
            },
        })
        console.log(respuesta.data);
        sessionStorage.setItem('userid', respuesta.data.user_id);
        alert("Bienvenido " + usrname);
        location.href = './index.html';

    } catch (error) {
        console.log("PROBLEMA", error.response.status);
        alert("ERROR, usuario no registrado");
    }
}

const logout = async () => {
    if(sessionStorage.getItem('userid') != null){
        try {
            const respuesta = await axios.post('https://arriolagabriel.pythonanywhere.com/logout', {
            }).then(() => {
                alert("Nos vemos pronto!");
                sessionStorage.removeItem('userid')
                sessionStorage.removeItem('barcos')
                sessionStorage.clear()
            });
        } catch (error) {
            console.log(error);
        }
    }
}

const crear_tablero_usuario = async () => {
    if (sessionStorage.getItem("userid") == null) {
        alert("Debes iniciar sesión para jugar!");
    }
    else {
        if (sessionStorage.getItem('barcos') > 0)
            borrar_tablero();
        try {
            const respuesta = await axios.post('https://arriolagabriel.pythonanywhere.com/tablero/usuario', {
                params: {
                    user_id: sessionStorage.getItem('userid')
                },
            })
            sessionStorage.setItem('barcos', respuesta.data.barcos);
            sessionStorage.setItem('partida', respuesta.data.partida);
            sessionStorage.setItem('disparos', 1);
            sessionStorage.setItem('coordenada', '');
        } catch (error) {
            console.log(error);
        }
    }
}

const borrar_tablero = async () => {
    if (sessionStorage.getItem("partida") != null) {
        try {
            const respuesta = await axios.delete('https://arriolagabriel.pythonanywhere.com/tablero/borrar', {
                data: {
                    partida: sessionStorage.getItem('partida')
                },
            })
                .then(() => alert('Partida Eliminada'));
            sessionStorage.removeItem('partida');
            sessionStorage.setItem('barcos', 0);
            location.href = './play.html';
        } catch (error) {
            console.log(error);
        }
    }
}

const ver_tablero_usuario = async () => {
    try {
        const respuesta = await axios.get('https://arriolagabriel.pythonanywhere.com/tablero', {
            params: {
                partida: '3'
            }
        })

        console.log(respuesta);
    } catch (error) {
        console.log(error);
    }
}

const disparo = async () => {
    try {
        const respuesta = await axios.put('https://arriolagabriel.pythonanywhere.com/tablero/disparo', {
            params: {
                barcos: sessionStorage.getItem('barcos'),
                disparos: sessionStorage.getItem('disparos'),
                user_id: sessionStorage.getItem('userid'),
                partida: sessionStorage.getItem('partida'),
                coordenada: sessionStorage.getItem('coordenada')
            }
        })
        console.log(respuesta.data);
        sessionStorage.setItem('disparos', Number(sessionStorage.getItem('disparos')) + 1);
        sessionStorage.setItem('barcos', respuesta.data.barcos);

        if (respuesta.data.golpe == 'miss') {
            elemento = document.getElementById(sessionStorage.getItem('coordenada'))
            elemento.setAttribute("class", "miss")
            elemento.innerHTML = `<img src="./img/no-sign-cross-png.webp" height="60" alt="MISS">`;
        }
        else if (respuesta.data.golpe == 'hit') {
            elemento = document.getElementById(sessionStorage.getItem('coordenada'))
            elemento.setAttribute("class", "hit")
            elemento.innerHTML = `<img src="./img/barco-tablero.png" height="60" alt="HIT">`;
        }

        if (respuesta.data.estado == 'Finished')
            alert('fin del juego')
    } catch (error) {
        console.log(error);
    }
}

const ping = async () => {
    try {
        const respuesta = await axios.get('https://arriolagabriel.pythonanywhere.com/ping')

        console.log(respuesta);
    } catch (error) {
        console.log(error);
    }
}


window.onload = init();

function init() {
   // ping();
}
