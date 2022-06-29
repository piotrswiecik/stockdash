<template>
  <form @submit.prevent>
    <p>Login form</p>
    <button @click="testToDash">Login</button>
  </form>
</template>

<script>
export default {
  name: "LoginForm",
  methods: {
    testToDash() {
      this.$router.push({name: 'dashboard'});
    },
  },
}
</script>

<style scoped>

</style>