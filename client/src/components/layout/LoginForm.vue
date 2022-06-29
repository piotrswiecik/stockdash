<template>
  <form @submit.prevent @keydown.enter="login">
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
    <button type="button" name="login-submit" @click="login">Login</button>
  </form>
  <div class="login-error" v-if="loginError">
    <p>{{ this.loginError }}</p>
  </div>
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
      loginError: null,
    };
  },
  beforeMount() {
    this.enteredUsername = '';
    this.enteredPassword = '';
    this.enteredUsernameValid = true;
    this.enteredPasswordValid = true;
    this.loginError = null;
  },
  methods: {
    validateField(event) {
      // check if data was entered && if password is 8+ chars
      if (event.target.name === 'username') {
        console.log(event);
        this.enteredUsernameValid = this.enteredUsername !== '';
      }
      else if (event.target.name === 'password') {
        this.enteredPasswordValid = this.enteredPassword !== '' && this.enteredPassword.length >= 8;
      }
    },
    async login(event) {
        this.validateField(event);
      // attempt login with credentials provided in login form
      if (!this.enteredUsernameValid || !this.enteredPasswordValid) {
        return;
      }
      try {
        // eslint-disable-next-line no-unused-vars
        const loginResponse = await this.$store.dispatch('auth/loginRequest', {
          username: this.enteredUsername,
          password: this.enteredPassword,
        });
        await this.$router.replace({name: 'dashboard'});
      } catch(err) {
        this.loginError = err.message === 'Authentication failed!' ? err.message : 'Authentication failed!';
      }
    },
  },
}
</script>

<style scoped>
.validation-error {
  color: red;
}

.login-error {
  color: red;
}
</style>