async function writeLog(message) {

    console.log("writeLog fired");

    const response = await fetch("/logEndpoint", {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: message
    });
}

//name saver for login screen
async function saveName() {
    let time = Date.now();
    let username = sessionStorage.getItem("username")

    writeLog(username + " logged in at " + time);
    console.log(username + "logged in at " + time)
}

//action logger
async function actionLogger(action) {
    let time = Date.now();
    let username  = sessionStorage.getItem("username")

    writeLog(username + " clicked the  " + action + " button.");
    console.log(username + " clicked the  " + action + " button.")
}