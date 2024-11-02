<template>
    <v-container style="height: 100vh;">
        <v-row>
            <v-col cols=12>
                <v-text-field v-model="search" label="Search" variant="underlined" />
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12" md="4" v-for="service in filteredServices" :key="service.name">
                <v-card height="100%">
                    <v-card-item>
                        <v-card-title>{{ service.name }}</v-card-title>
                        <v-card-subtitle>{{ service.subtitle }}</v-card-subtitle>
                    </v-card-item>
                    <v-card-text class="mb-12 pb-12">
                        <span v-html="service.description"></span>
                        <div class="mt-4 text-right d-flex justify-space-between"
                            style="position: absolute; bottom: 16px; left: 16px; right: 16px;">
                            <v-chip color="primary">
                                {{ service.category }}
                            </v-chip>
                            <v-chip color="secondary">
                                Cost: ${{ service.cost_per_request }}
                            </v-chip>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const search = ref("");
const services = ref([
    {
        name: "LinkedIn",
        subtitle: "Search for LinkedIn profiles and send messages.",
        description: "The <code>linkedin_01</code> tool allows your agent to search for LinkedIn profiles and send messages on your behalf",
        cost_per_request: 0.05,
        category: "Social",
    },
    {
        name: "NYTimes",
        subtitle: "Search for articles from the New York Times.",
        description: "The <code>nytimes_01</code> tool allows your agent to search for articles from the New York Times.",
        cost_per_request: 0.01,
        category: "News",
    },
    {
        name: "Weather",
        subtitle: "Get the current weather in any city.",
        description: "The <code>weather_01</code> tool allows your agent to get the current weather in any city.",
        cost_per_request: 0.001,
        category: "Weather",
    },
    {
        name: "Stocks",
        subtitle: "Get stock prices and news.",
        description: "The <code>stocks_01</code> tool allows your agent to get stock prices and news.",
        cost_per_request: 0.005,
        category: "Finance",
    },
    {
        name: "Crypto",
        subtitle: "Get crypto prices and news.",
        description: "The <code>crypto_01</code> tool allows your agent to get crypto prices and news.",
        cost_per_request: 0.005,
        category: "Finance",
    },
    {
        name: "Gmail",
        subtitle: "Send and read emails through Gmail.",
        description: "The <code>gmail_01</code> tool enables your agent to send and read emails through your Gmail account with proper authentication.",
        cost_per_request: 0.03,
        category: "Communication",
    },
    {
        name: "Calendar",
        subtitle: "Manage calendar events and schedules.",
        description: "The <code>calendar_01</code> tool allows your agent to create, modify and check calendar events across multiple platforms.",
        cost_per_request: 0.02,
        category: "Productivity",
    },
    {
        name: "Spotify",
        subtitle: "Control music playback and playlists.",
        description: "The <code>spotify_01</code> tool lets your agent control music playback, create playlists, and search for songs on Spotify.",
        cost_per_request: 0.02,
        category: "Entertainment",
    },
    {
        name: "Maps",
        subtitle: "Get directions and location information.",
        description: "The <code>maps_01</code> tool enables your agent to find directions, calculate distances, and get location details.",
        cost_per_request: 0.015,
        category: "Navigation",
    },
    {
        name: "Twitter",
        subtitle: "Post tweets and monitor trends.",
        description: "The <code>twitter_01</code> tool allows your agent to post tweets, monitor trends, and engage with Twitter content.",
        cost_per_request: 0.04,
        category: "Social",
    },
    {
        name: "Wikipedia",
        subtitle: "Search and retrieve Wikipedia articles.",
        description: "The <code>wikipedia_01</code> tool lets your agent search and extract information from Wikipedia articles.",
        cost_per_request: 0.005,
        category: "Knowledge",
    },
    {
        name: "Amazon",
        subtitle: "Search products and track prices.",
        description: "The <code>amazon_01</code> tool enables your agent to search products, track prices, and monitor availability on Amazon.",
        cost_per_request: 0.03,
        category: "Shopping",
    },
    {
        name: "Slack",
        subtitle: "Send messages and manage channels.",
        description: "The <code>slack_01</code> tool allows your agent to send messages, manage channels, and interact with Slack workspaces.",
        cost_per_request: 0.025,
        category: "Communication",
    },
    {
        name: "GitHub",
        subtitle: "Manage repositories and issues.",
        description: "The <code>github_01</code> tool lets your agent create issues, manage repositories, and monitor GitHub activities.",
        cost_per_request: 0.02,
        category: "Development",
    }
]);

const filteredServices = computed(() => {
    return services.value.filter(service =>
        service.name.toLowerCase().includes(search.value.toLowerCase()) ||
        service.category.toLowerCase().includes(search.value.toLowerCase()) ||
        service.description.toLowerCase().includes(search.value.toLowerCase())
    );
});
</script>
