document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chatForm") as HTMLFormElement;
    const chatInput = document.querySelector(".new-chat-message") as HTMLTextAreaElement;
    const chatMessagesContainer = document.getElementById("existingChatMessages") as HTMLDivElement;

    if (!chatForm || !chatInput || !chatMessagesContainer) {
        console.error("Chat form elements not found!");
        return;
    }

    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent full-page reload

        const formData = new FormData(chatForm);

        try {
            const response = await fetch("/chat/send/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": (document.querySelector("[name=csrfmiddlewaretoken]") as HTMLInputElement).value
                }
            });

            const data = await response.json();
            if (data.success) {
                console.log("Message sent successfully:", data.message);
                addMessageToUI(data.message);
                chatInput.value = ""; // Clear input after sending
            }
        } catch (error) {
            console.error("Error sending message:", error);
        }
    });

    function addMessageToUI(message: { author: string; text: string; timestamp: string }) {
        const isSent = message.author != "AI";

        let chatCard = document.createElement("div");
        chatCard.classList.add("chat-card", isSent ? "sent" : "received");

        let chatText = document.createElement("div");
        chatText.classList.add("chat-text", isSent ? "sent" : "received");
        chatText.textContent = message.text;

        let chatOwner = document.createElement("div");
        chatOwner.classList.add("chat-owner");

        let chatAvatar = document.createElement("img");
        chatAvatar.classList.add("chat-avatar");
        chatAvatar.src = isSent ? "/static/chatbot/user.png" : "/static/chatbot/ai.png";
        chatAvatar.alt = "Avatar";

        let chatInfo = document.createElement("div");
        chatInfo.classList.add("chat-info");

        let chatAuthor = document.createElement("div");
        chatAuthor.classList.add("chat-author");
        chatAuthor.textContent = message.author;

        let chatTimestamp = document.createElement("div");
        chatTimestamp.classList.add("chat-timestamp");
        chatTimestamp.textContent = message.timestamp;

        // Append elements
        chatInfo.appendChild(chatAuthor);
        chatInfo.appendChild(chatTimestamp);
        chatOwner.appendChild(chatAvatar);
        chatOwner.appendChild(chatInfo);
        chatCard.appendChild(chatText);
        chatCard.appendChild(chatOwner);

        chatMessagesContainer.appendChild(chatCard);
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight; // Auto-scroll
    }
});
