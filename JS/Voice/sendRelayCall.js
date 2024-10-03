import { Voice } from "@signalwire/realtime-api";
import EventEmitter from 'events';
import dotenv from 'dotenv';
dotenv.config({ path: '../../.env' })

const client = new Voice.Client({
    project: process.env.PROJECT_ID,
    token: process.env.AUTH_TOKEN,
    contexts: ["office"],
    /*debug: {
      logWsTraffic: true,
     },*/
    // host: process.env.HOST // not required in production environments
});

const call = await client.dialPhone({
    from: process.env.FROM_NUMBER,
    to: process.env.PERSONAL_NUMBER,
});

await call.playTTS({ text: "This call will be recorded." });

// Print out the URL of the recording, as soon as the recording ends.
call.on("recording.ended", (recording) => {
  console.log("Recording URL:", recording);
});

// Start recording
const recording = await call.recordAudio({
  direction: "both",
  endSilenceTimeout: 0,
  terminators: "",
});
console.log("Recording id:", recording.id);

