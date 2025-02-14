// document.addEventListener("DOMContentLoaded", () => {
//     const chatForm = document.getElementById("chatForm") as HTMLFormElement;
//     const chatInput = document.querySelector(".new-chat-message") as HTMLTextAreaElement;
//     const chatMessagesContainer = document.getElementById("existingChatMessages") as HTMLDivElement;

//     if (!chatForm || !chatInput || !chatMessagesContainer) {
//         console.error("Chat form elements not found!");
//         return;
//     }

//     chatForm.addEventListener("submit", async (event) => {
//         event.preventDefault(); // Prevent full-page reload

//         const formData = new FormData(chatForm);

//         try {
//             const response = await fetch("/chat/send/", {
//                 method: "POST",
//                 body: formData,
//                 headers: {
//                     "X-CSRFToken": (document.querySelector("[name=csrfmiddlewaretoken]") as HTMLInputElement).value
//                 }
//             });

//             const data = await response.json();
//             if (data.success) {
//                 console.log("Message sent successfully:", data.message);
//                 addMessageToUI(data.message);
//                 chatInput.value = ""; // Clear input after sending
//             }
//         } catch (error) {
//             console.error("Error sending message:", error);
//         }
//     });

//     function addMessageToUI(message: { author: string; text: string; timestamp: string }) {
//         const isSent = message.author != "AI";

//         let chatCard = document.createElement("div");
//         chatCard.classList.add("chat-card", isSent ? "sent" : "received");

//         let chatText = document.createElement("div");
//         chatText.classList.add("chat-text", isSent ? "sent" : "received");
//         chatText.textContent = message.text;

//         let chatOwner = document.createElement("div");
//         chatOwner.classList.add("chat-owner");

//         let chatAvatar = document.createElement("img");
//         chatAvatar.classList.add("chat-avatar");
//         chatAvatar.src = isSent ? "/static/chatbot/user.png" : "/static/chatbot/ai.png";
//         chatAvatar.alt = "Avatar";

//         let chatInfo = document.createElement("div");
//         chatInfo.classList.add("chat-info");

//         let chatAuthor = document.createElement("div");
//         chatAuthor.classList.add("chat-author");
//         chatAuthor.textContent = message.author;

//         let chatTimestamp = document.createElement("div");
//         chatTimestamp.classList.add("chat-timestamp");
//         chatTimestamp.textContent = message.timestamp;

//         // Append elements
//         chatInfo.appendChild(chatAuthor);
//         chatInfo.appendChild(chatTimestamp);
//         chatOwner.appendChild(chatAvatar);
//         chatOwner.appendChild(chatInfo);
//         chatCard.appendChild(chatText);
//         chatCard.appendChild(chatOwner);

//         chatMessagesContainer.appendChild(chatCard);
//         chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight; // Auto-scroll
//     }
// });
import { marked } from "marked";

document.addEventListener("DOMContentLoaded", () => {
    const chatMessagesContainer = document.getElementById("existingChatMessages");

    if (chatMessagesContainer) {
        // Scroll to the bottom when the page loads
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chatForm") as HTMLFormElement;
    const chatInput = document.querySelector(".new-chat-message") as HTMLTextAreaElement;
    const chatMessagesContainer = document.getElementById("existingChatMessages") as HTMLDivElement;
    const chatSubmitButton = chatForm.querySelector("button[type='submit']") as HTMLButtonElement;


    if (!chatForm || !chatInput || !chatMessagesContainer) {
        console.error("Chat form elements not found!");
        return;
    }

    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent full-page reload
        chatSubmitButton.disabled = true; // Disable submit button
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

                // Start AI response stream
                streamAIResponse(data.message.text);
            } else {
                chatSubmitButton.disabled = false; // Enable submit
            }
        } catch (error) {
            chatSubmitButton.disabled = false; // Enable submit button
            console.error("Error sending message:", error);
        }
    });

    function addMessageToUI(message: { author: string; text: string; timestamp: string }): HTMLDivElement {
        const isSent = message.author !== "AI";

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

        return chatCard; // Return the message bubble for streaming updates
    }


    async function streamAIResponse(userInput: string) {
        const eventSource = new EventSource(`/chat/stream_ai/?text=${encodeURIComponent(userInput)}`);
        let aiMessageContainer: HTMLDivElement | null = null;
        let accumulatedText = "";

        eventSource.onmessage = async (event) => {
            const data = JSON.parse(event.data).text;
            // const data = JSON.parse(event.data);
            // console.log("raw event:", event);
            // console.log("AI response streaming:", data);

            if (!aiMessageContainer) {
                // Create an AI message bubble immediately
                // aiMessageContainer = addMessageToUI({ author: "AI", text: "", timestamp: data.timestamp });
                aiMessageContainer = addMessageToUI({ author: "AI", text: "", timestamp: "12:00" });


                // Get the chat-text div inside the newly created bubble
                let chatText = aiMessageContainer.querySelector(".chat-text") as HTMLDivElement;
                if (chatText) {
                    chatText.textContent = data; // Initialize text
                    // chatText.innerHTML = await marked.parse(data);
                }
            } else {
                // Append new text dynamically
                let chatText = aiMessageContainer.querySelector(".chat-text") as HTMLDivElement;
                if (chatText) {
                    chatText.textContent += data; // Append words
                    // chatText.innerHTML += await marked.parse(data);
                }
            }
            accumulatedText += data; // Accumulate text
            // Auto-scroll to bottom
            chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
        };

        eventSource.onerror = async (error) => {
            chatSubmitButton.disabled = false; // Enable submit button
            if (eventSource.readyState === EventSource.CLOSED) {
                console.log("SSE Connection Closed Normally.");
            } else {
                console.error("SSE Connection Error:", error);
            }
            eventSource.close();
            // change the chatText to markdown
            if (aiMessageContainer) {
                let chatText = aiMessageContainer.querySelector(".chat-text") as HTMLDivElement;
                if (chatText) {
                    chatText.innerHTML = await marked.parse(accumulatedText); // 🔹 Render full Markdown
                }
            }
        };
    }

});
