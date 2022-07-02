<template>
  <div class="flex-grid">
    <div class="col">
      ticker+exch
    </div>
    <div class="col">
      name
    </div>
  </div>
  <div class="flex-grid">
    <div class="col-stats">
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
    </div>
    <div class="col">chart</div>
  </div>
  <div class="flex-grid">
    <div class="col">
      <dash-description></dash-description>
    </div>
  </div>
</template>

<script>
import DashDescription from "@/components/layout/DashDescription";

export default {
  name: "DashContent",
  // eslint-disable-next-line vue/no-unused-components
  components: {DashDescription},
  computed: {
    currentTicker() {
      return this.$store.getters['stock/currentTicker'];
    },
    currentName() {
      return this.$store.getters['stock/currentName'];
    },
  }
}
</script>

<style scoped>
.flex-grid {
  display: flex;
  border: 1px solid white;
}
.col {
  border: 1px solid white;
  flex: 1;
}

.col-stats {
  width: 25%;
}

</style>