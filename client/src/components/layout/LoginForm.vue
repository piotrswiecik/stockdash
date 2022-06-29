<template>
  <form @submit.prevent @keydown.enter="login">
    <h3>StockDash login</h3>
    <div class="form-control">
      <label for="username">Username</label>
      <input type="text" id="username" name="username" v-model.trim="enteredUsername" @blur="validateField"
      placeholder="Login">
    </div>
    <div class="form-control">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" v-model.trim="enteredPassword" @blur="validateField"
      placeholder="Password">
    </div>
    <button class="login-button" type="button" name="login-submit" @click="login">Login</button>
  </form>
  <div class="validation-error" v-if="!enteredUsernameValid">
    <p>Username must not be blank</p>
  </div>
  <div class="validation-error" v-if="!enteredPasswordValid">
    <p>Password must contain at least 8 characters</p>
  </div>
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
form {
  background: rgb(250,204,21);
  background: linear-gradient(90deg, rgba(250,204,21,1) 0%, rgba(249,117,22,1) 100%);
  border-radius: 20px;
  padding: 20px;
}

input {
  padding: 8px;
  margin: 12px;
  border:0;
  border-bottom:1px solid #eee;
  border-radius: 4px;
  box-shadow: 3px 3px 2px rgba(0,0,0,0.07);;
}

.validation-error {
  color: red;
}

.login-error {
  color: red;
}

.login-button {
  appearance: none;
  background-color: #FAFBFC;
  border: 1px solid rgba(27, 31, 35, 0.15);
  border-radius: 6px;
  box-shadow: rgba(27, 31, 35, 0.04) 0 1px 0, rgba(255, 255, 255, 0.25) 0 1px 0 inset;
  box-sizing: border-box;
  color: #24292E;
  cursor: pointer;
  display: inline-block;
  font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  list-style: none;
  margin-top: 8px;
  padding: 6px 16px;
  position: relative;
  transition: background-color 0.2s cubic-bezier(0.3, 0, 0.5, 1);
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: middle;
  white-space: nowrap;
  word-wrap: break-word;
}

.login-button:hover {
  background-color: #F3F4F6;
  text-decoration: none;
  transition-duration: 0.1s;
}

.login-button:disabled {
  background-color: #FAFBFC;
  border-color: rgba(27, 31, 35, 0.15);
  color: #959DA5;
  cursor: default;
}

.login-button:active {
  background-color: #EDEFF2;
  box-shadow: rgba(225, 228, 232, 0.2) 0 1px 0 inset;
  transition: none 0s;
}

.login-button:focus {
  outline: 1px transparent;
}

.login-button:before {
  display: none;
}

.login-button::-webkit-details-marker {
  display: none;
}
</style>

