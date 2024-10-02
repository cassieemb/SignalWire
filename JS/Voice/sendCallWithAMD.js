import { Voice } from "@signalwire/realtime-api";
import dotenv from 'dotenv';
dotenv.config({ path: './../.env' })

const client = new Voice.Client({
    project: process.env.PROJECT_ID,
    token: process.env.AUTH_TOKEN,
    contexts: ["office"],
});

try {
    // create call
    const call = await client.dialPhone({
        from: process.env.FROM_NUMBER,
        to: process.env.PERSONAL_NUMBER,
        timeout: 30
    });
    
    console.log('The call has been answered!', call.id)
    detectAMD(call)

    // start speaking to callee while AMD is processing and gather dtmf to begin playback
    const prompt = await call.promptTTS({text: "Hello Parent of Houston ISD. Press any key now to hear an important message about your student. This is an important message regarding your student's upcoming school events. This message is important for end of year grades and graduation.",
        digits: {
            max: 1,
            digitTimeout: 5
        },
    });

    // handle dtmf input
    const digits = await prompt.ended();
    if (digits) {
        await call.playAudio({
            url: "https://cdn.signalwire.com/default-music/welcome.mp3",
        });
    }
} catch (e) {
    console.error(e)
}

async function detectAMD(call){
    try {
        const detect = await call.detectAnsweringMachine({timeout: 8, waitForBeep: true})
        const result = await detect.waitForResult();
        const event = result.detect.params.event
        console.log(event)
        switch(event) {
            case "HUMAN":
                console.log("Received human, carry on")
                break;
            case "finished":
                console.log("Detection complete")
                break;
            case "MACHINE":
                console.log("Received machine, execute machine instructions")
                await call.playTTS({text: "You're a machine"})
                await call.playAudio({
                    url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                });
                break;
            default:
                console.log("Unknown Event: ", event)
        }
    } catch (e) {
        console.error(e)
    }
}
