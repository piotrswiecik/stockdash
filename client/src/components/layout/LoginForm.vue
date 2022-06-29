<template>
  <form @submit.prevent>
    <h3>Login form</h3>
    <div class="form-control">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" v-model.trim="enteredUsername" @blur="validateFields">
    </div>
    <div class="form-control">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" v-model.trim="enteredPassword" @blur="validateFields">
    </div>
    <button @click="login">Login</button>
  </form>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      enteredUsername: '',
      enteredPassword: '',
    };
  },
  methods: {
    validateFields(event) {
      // check if anything was entered && if password is 8+ chars
      console.log('validating form, trigger = ' + event.target.name);
    },
    async login() {
      // attempt login with credentials provided in login form
      // this.$router.push({name: 'dashboard'});
      console.log('received login data: ' + this.enteredUsername + ' ' + this.enteredPassword);
      console.log('forwarding to vuex');
      try {
        const loginResponse = await this.$store.dispatch('auth/loginRequest', {
          username: this.enteredUsername,
          password: this.enteredPassword,
        });
        console.log('auth request ok, returned: ' + loginResponse);
      } catch(err) {
        console.log('authentication handler returned error: ' + err);
      }
    },
  },
}
</script>

<style scoped>

</style>