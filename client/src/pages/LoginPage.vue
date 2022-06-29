<template>
  <div class="container">
    <div class="filler"></div>
    <div class="form-box"><login-form></login-form></div>
    <div class="filler"></div>
  </div>
</template>

<script>
import LoginForm from "@/components/layout/LoginForm";

export default {
  name: "LoginPage",
  components: { LoginForm },
}
</script>

<style scoped>
.container {
  display: flex;
  align-self: center;
  align-content: center;
}

.filler {
  flex-grow: 5;
}

.form-box {
  flex-grow: 2;
}
</style>