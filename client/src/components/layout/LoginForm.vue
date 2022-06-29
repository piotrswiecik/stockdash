<template>
  <form @submit.prevent>
    <h3>Login form</h3>
    <div class="form-control">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" v-model.trim="enteredUsername" @blur="validateField">
      <p class="validation-error" v-if="!enteredUsernameValid">Username must not be blank</p>
    </div>
    <div class="form-control">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" v-model.trim="enteredPassword" @blur="validateField">
      <p class="validation-error" v-if="!enteredPasswordValid">Password must contain at least 8 characters</p>
    </div>
    <button name="login-submit" @click="login">Login</button>
  </form>
</template>

<script>
export default {
  name: "LoginForm",
  data() {
    return {
      enteredUsername: '',
      enteredPassword: '',
      enteredUsernameValid: true,
      enteredPasswordValid: true,
    };
  },
  methods: {
    validateField(event) {
      // check if data was entered && if password is 8+ chars
      if (event.target.name === 'username') {
        this.enteredUsernameValid = this.enteredUsername !== '';
      }
      else if (event.target.name === 'password') {
        this.enteredPasswordValid = this.enteredPassword !== '' && this.enteredPassword.length >= 8;
      }
    },
    async login() {
      // attempt login with credentials provided in login form
      // console.log('validating');
      // await this.validateField(event);
      if (!this.enteredUsernameValid || !this.enteredPasswordValid) {
        return;
      }
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
.validation-error {
  color: red;
}
</style>