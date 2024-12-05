import { Messaging } from "@signalwire/realtime-api";
import dotenv from 'dotenv';
dotenv.config({ path: '../../.env' })

// create client
const client = new Messaging.Client({
    project: process.env.PROJECT_ID,
    token: process.env.AUTH_TOKEN,
    contexts: ["office"],
    //host: process.env.HOST // not required in production environments
});

console.log("Started successfully - waiting for a message to be received")

client.on("message.received", async (message) => {
    console.log("message.received", message);
    console.log(message.from)

    try {
        const status = await client.send({
            context: "office",
            from: process.env.FROM_NUMBER,
            to: message.from,
            body: "Hello World!",
        });
        
        console.log("Message sent successfully:", status);
    } catch (e) {
        console.error("Failed to send message:", e);
    }
});