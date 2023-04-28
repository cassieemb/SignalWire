import { Voice } from "@signalwire/realtime-api";
import "dotenv/config.js";

const client = new Voice.Client({
    project: process.env.PROJECT_ID,
    token: process.env.AUTH_TOKEN,
    contexts: ["office"]
    // host: process.env.ST_HOST // only needed on staging
});

const call = await client.dialPhone({
  from: process.env.FROM_NUMBER,
  to: process.env.PERSONAL_NUMBER,
});

await call.playTTS({
  text: "Thank you for answering this Relay Dial test!",
});
