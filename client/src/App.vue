<template>
  <p>Test vuex: {{ test }}</p>
</template>

<script>

export default {
  name: 'App',
  computed: {
    test() {
      return this.$store.state.test;
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
