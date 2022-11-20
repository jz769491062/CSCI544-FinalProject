const eval = require("./interactor")
const tmi = require("tmi.js");

// Define configuration options
const opts = {
  identity: {
    username: "imraggedy",
    password: "3vc0guoktcs2jdwixghgjjwlzbrmm0",
  },
  channels: ["imraggedy"],
};

// Create a client with our options
const client = new tmi.client(opts);

// Register our event handlers (defined below)
client.on("message", onMessageHandler);
client.on("connected", onConnectedHandler);

// Connect to Twitch:
client.connect();

// Called every time a message comes in
async function onMessageHandler(target, context, msg, self) {
  if (self) {
    return;
  } // Ignore messages from the bot

  // Remove whitespace from chat message
  const commandName = msg.trim();

  switch(commandName){
    case "!who":
      client.say(target, `This is the pacifier!`);
      console.log(`* Executed ${commandName} command`);
      break;
    case "!clear":
      client.clear(opts.channels[0]);
      break;
    default:
      console.log(`* User said: ${commandName}`);
      console.log(`${context.id}`);

      if(await eval.getEvaluation(commandName) == 'fail'){
        client.deletemessage(opts.channels[0], context.id);
      } 
  }
}

// Called every time the bot connects to Twitch chat
function onConnectedHandler(addr, port) {
  console.log(`* Connected to ${addr}:${port}`);
}
