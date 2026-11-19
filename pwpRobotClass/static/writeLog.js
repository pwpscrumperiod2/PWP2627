console.log("WriteLog loaded")

async function writeLog(message) {

    console.log("writeLog fired");

    const response = await fetch("/logEndpoint", {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: message
    });

    await console.log(response.json())
}

//logs login to log.txt
async function loginLogger() {
    let time = Date.now();
    const username = sessionStorage.getItem("username")

    writeLog("[" + time + "] " + username + " logged in.");
    console.log("[" + time + "] " + username + " logged in.");
}

//saves name to session storage
async function saveName() {
    sessionStorage.setItem("username", document.getElementById("username").value)
}

//action logger
async function actionLogger(action) {
    let time = Date.now();
    let username  = sessionStorage.getItem("username")

    writeLog("[" + time + "] " + username + " clicked the  " + action + " button.");
    console.log("[" + time + "] " + username + " clicked the  " + action + " button.")
}