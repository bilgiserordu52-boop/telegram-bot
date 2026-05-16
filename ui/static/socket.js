const socket = io();

socket.on("connect", () => {
    console.log("🟢 Connected to AI runtime");
});

socket.on("ai_reply", (data) => {

    const log = document.getElementById("live");

    if (log) {

        const item = document.createElement("div");

        item.innerHTML =
        "👤 " + data.user_id +
        "<br>💬 " + data.text +
        "<br>🤖 " + data.reply +
        "<hr>";

        log.prepend(item);
    }
});
