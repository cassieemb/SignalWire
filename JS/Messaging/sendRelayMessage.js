import { Messaging } from "@signalwire/realtime-api";
import dotenv from 'dotenv';
dotenv.config({ path: './../.env' })

// create client
const client = new Messaging.Client({
    project: process.env.PROJECT_ID,
    token: process.env.AUTH_TOKEN,
    contexts: ["office"],
    //host: process.env.HOST // not required in production environments
});

// send a message
try {
    const status = await client.send({
        context: "office",
        from: process.env.FROM_NUMBER,
        to: process.env.PERSONAL_NUMBER,
        body: "Hello World!",
    })

    console.log(status)
    process.exit()
} catch (e) {
    console.error(e)
    process.exit()
}
