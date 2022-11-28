const eval = require("./interactor")
const tmi = require("tmi.js");

// Define configuration options
const opts = {
  identity: {
    username: "imraggedy",
    password: "",
  },
  channels: ["imraggedy"],
};

offences = {}
min_offences = 3
// Create a client with our options
const client = new tmi.client(opts);

// Register our event handlers (defined below)
client.on("message", onMessageHandler);
client.on("connected", onConnectedHandler);

// Connect to Twitch:
client.connect();

function tracker(id){
  if (id in offences){
    offences[id]+=1
  }
  else{
    offences[id]=1
  }
}

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
     resp = await eval.getEvaluation(commandName)
     if(resp=='del'){
        client.deletemessage(opts.channels[0], context.id);
        tracker(context['user-id'])
      }
      if(resp=='warn'){
        client.say(target, `Please keep the chat civil @${context.username}`);
        tracker(context['user-id'])
      }
      if(offences[context['user-id']]>min_offences){
        client.say(target,  `@${context.username}, You have been timed out for 30s`);
        client.timeout(target,context.username,30,"Repeated Offence")
      }
  }
}

// Called every time the bot connects to Twitch chat
function onConnectedHandler(addr, port) {
  console.log(`* Connected to ${addr}:${port}`);
}
