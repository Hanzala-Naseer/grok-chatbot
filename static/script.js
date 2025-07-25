document.addEventListener("DOMContentLoaded", () => {
  const chatContainer = document.getElementById("chat-container");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const loadingOverlay = document.getElementById("loadingOverlay");

  // Hide loader when page loads
  window.onload = () => {
    loadingOverlay.style.display = "none";
    input.focus();
  };

  // Enter key sends message, Shift+Enter adds newline
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.dispatchEvent(new Event("submit"));
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userText = input.value.trim();
    if (!userText) return;

    addMessage("You", userText, "user-message");
    input.value = "";

    const typingMsg = addMessage("Bot", "Typing...", "bot-message typing");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText }),
      });

      const data = await res.json();
      typingMsg.remove();
      addMessage("Bot", data.response || "Error: " + data.error, "bot-message");
    } catch (err) {
      typingMsg.remove();
      addMessage("Bot", "Failed to connect.", "bot-message");
    }
  });

  function addMessage(sender, text, className) {
    const msg = document.createElement("div");
    msg.className = `message ${className}`;
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatContainer.appendChild(msg);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return msg;
  }
});
