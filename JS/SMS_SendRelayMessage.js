import { Messaging } from "@signalwire/realtime-api";
import "dotenv/config.js";

// create client
const client = new Messaging.Client({
    project: process.env.PROJECT_ID,
    token: process.env.AUTH_TOKEN,
    contexts: ["office"],
    // host: process.env.ST_HOST // only when testing on staging
});

// send a message
try {
    const status = await client.send({
        context: "office",
        from: process.env.FROM_NUMBER,
        to: process.env.PERSONAL_NUMBER,
        body: "Hello World!",
        media: null
    })

    console.log(status)
} catch (e) {
    console.error(e)
}
