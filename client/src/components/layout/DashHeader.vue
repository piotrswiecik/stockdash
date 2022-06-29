<template>
  <div class="container">
    <div class="item-left">
      <h2>StockDash</h2>
    </div>
    <div class="item-right">
      <p>test</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "DashHeader"
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: flex-start;
  width: 500px;
}

.item-left {
  flex-grow: 4;
}

.item-right {
  flex-grow: 1;
}
</style>