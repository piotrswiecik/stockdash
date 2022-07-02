<template>
  <div class="flex-grid flex-header">
    <div class="col-wide"><h2>StockDash</h2></div>
    <div class="col"><a href="#" @click="logout">Logout</a></div>
  </div>
</template>

<script>
export default {
  name: "DashHeader",
  methods: {
    logout() {
      this.$store.dispatch('auth/logoutRequest');
    },
  }
}
</script>

<style scoped>
.flex-grid {
  display: flex;
  border: 1px solid white;
}
.flex-header {
  align-items: center;
  border: 1px solid white;
}
.col {
  flex: 1;
}
.col-wide {
  width: 80%!important;
  border: 1px solid white;
}
</style>