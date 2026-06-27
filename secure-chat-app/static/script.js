var socket = io();

// Generate AES key
let aesKey = new TextEncoder().encode("12345678901234567890123456789012");

// Encrypt message
async function encryptMessage(message) {
    let enc = new TextEncoder();
    let encoded = enc.encode(message);

    let cryptoKey = await window.crypto.subtle.importKey(
        "raw", aesKey, "AES-GCM", false, ["encrypt"]
    );

    let iv = crypto.getRandomValues(new Uint8Array(12));

    let ciphertext = await window.crypto.subtle.encrypt(
        { name: "AES-GCM", iv: iv },
        cryptoKey,
        encoded
    );

    return {
        iv: Array.from(iv),
        data: Array.from(new Uint8Array(ciphertext))
    };
}

// Decrypt message
async function decryptMessage(encrypted) {
    let cryptoKey = await window.crypto.subtle.importKey(
        "raw", aesKey, "AES-GCM", false, ["decrypt"]
    );

    let iv = new Uint8Array(encrypted.iv);
    let data = new Uint8Array(encrypted.data);

    let decrypted = await window.crypto.subtle.decrypt(
        { name: "AES-GCM", iv: iv },
        cryptoKey,
        data
    );

    return new TextDecoder().decode(decrypted);
}

// Send message
async function sendMessage() {
    let username = document.getElementById("username").value;
    let msg = document.getElementById("message").value;

    if (!username || !msg) {
        alert("Enter username and message");
        return;
    }

    let encryptedMsg = await encryptMessage(msg);

    let payload = {
        user: username,
        message: encryptedMsg
    };

    socket.send(JSON.stringify(payload));

    // Clear input
    document.getElementById("message").value = "";
}

// Receive message
socket.on('message', async function(msg) {
    let data = JSON.parse(msg);

    let decryptedText = await decryptMessage(data.message);

    let li = document.createElement("li");

    let myName = document.getElementById("username").value;

    if (data.user === myName) {
        li.innerText = "You: " + decryptedText;
    } else {
        li.innerText = data.user + ": " + decryptedText;
    }

    let chatBox = document.getElementById("chat");
    chatBox.appendChild(li);

    // Auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;
});
