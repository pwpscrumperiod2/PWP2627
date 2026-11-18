const logElement = document.getElementById("user-log");

async function showLog() {
	var logResponse = await fetch("log.txt");
	var logText = await logResponse.text();

	logElement.textContent = logText;

}

showLog();
setInterval(showLog,1000);