<template>
    <div id="app">
        <div class="header">Financial corpus</div>
        <Search/>
    </div>
</template>

<script>
    import Search from './components/Search.vue'

    export default {
        name: 'app',
        components: {
            Search
        }
    }
</script>

<style>
    body {
        background-color: #E1E2E1;
    }

    #app {
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
        color: #333333;
        padding: 5em 18em 3em;
    }

    .header {
        color: #666161;
        font-size: 3em;
        margin-bottom: 3rem;
    }
</style>
