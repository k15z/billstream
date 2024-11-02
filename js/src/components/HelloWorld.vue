<template>
  <v-container class="fill-height">
    <v-responsive class="align-centerfill-height mx-auto" max-width="900">

      <div class="text-center">
        <h1 class="text-h2 font-weight-bold">The Agent Toolkit</h1>
        <h3 class="text-h5 font-weight-light mt-4">
          Connect your wallet and allow your AI agents to pay for themselves.
        </h3>
      </div>

      <div class="py-4" />

      <VCodeBlock :code="code" language="python" highlightjs></VCodeBlock>

      <div class="py-4" />

      <div class="text-center">
        <h3 class="text-h5 font-weight-light mt-4 mb-8">
            Any tool. Any network. Any scale.
        </h3>
        <v-btn>Explore</v-btn>
      </div>

    </v-responsive>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import VCodeBlock from '@wdns/vue-code-block';

const prompt = ref("");
const wallet = ref("");
const code = computed(() => `import openai
from agenttk import AgentToolkit

tools = AgentToolkit(
    wallet=` + wallet.value + `(
      api_key="...",
      password="..."
    )
)

assistant = client.beta.assistants.create(
    name="Generic Assistant",
    instructions="A helpful assistant that can use any tool to solve any problem.",
    model="gpt-4-1106-preview",
    tools=tools.find_tools("` + prompt.value + `", N=3)
)`)

function changeTarget(newPrompt: string, target: any) {
  // every 100 ms add a new character?
  for (let i = 0; i < newPrompt.length; i++) {
    setTimeout(() => {
      target.value = newPrompt.slice(0, i + 1);
    }, i * 50);
  }
  // return estimated time + how long to hold on screen
  return (newPrompt.length * 50) + 1000;
}

const promptRotations = [
  "find the weather in SF",
  "solve a math problem",
  "order me uber eats",
  "what stocks are up today?",
  "breaking election news"
]

const walletRotations = [
  "PrivyWallet",
  "CrossMintWallet",
  "LightsparkWallet",
  "CoinbaseWallet",
]


let index = 0;
const rotate = () => {
  let x = walletRotations[index % walletRotations.length];
  let time = changeTarget(x, wallet);

  let y = promptRotations[index % promptRotations.length];
  let time2 = changeTarget(y, prompt);

  index += 1;

  setTimeout(rotate, Math.max(time, time2));
}

rotate()
</script>
