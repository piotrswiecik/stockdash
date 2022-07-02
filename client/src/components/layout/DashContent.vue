<template>
  <div class="container">
    <div>Ticker: {{ currentTicker }} Name: {{ currentName }} </div>
  </div>
  <div class="container">
    <div class="dash-content-left-bar">
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>
      <p>STATS</p>

    </div>
    <div class="dash-content-right-field">
      <div class="item-chart">
        <p>chart</p>
        <p>chart</p>
        <p>chart</p>
        <p>chart</p>
        <p>chart</p>
        <p>chart</p>
        <p>chart</p>
        <p>chart</p>
        <p>chart</p>
        <p>chart</p>


      </div>
      <div class="item-description">
        <dash-description></dash-description>
      </div>
    </div>

  </div>
</template>

<script>
import DashDescription from "@/components/layout/DashDescription";

export default {
  name: "DashContent",
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
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.dash-content-right-field {
  display: flex;
  flex-wrap: nowrap;
  flex-direction: column;
  flex-grow: 4;
}

.dash-content-left-bar {
  height: 100%;
  flex-grow: 1;
}

.item-chart {
  flex-grow: 6;
}

.item-description {
  flex-grow: 2;
}

</style>