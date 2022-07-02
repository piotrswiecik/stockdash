<template>
  <div class="container">
    <div class="dash-page-header">
      <dash-header></dash-header>
    </div>
  </div>
  <div class="container">
    <div class="dash-page-navi">
      <dash-navi></dash-navi>
    </div>
    <div class="dash-page-content">
      <dash-content></dash-content>
    </div>
  </div>
  <div class="container">
    <div class="dash-page-footer">
      <dash-footer></dash-footer>
    </div>
  </div>
</template>

<script>
import DashHeader from "@/components/layout/DashHeader";
import DashFooter from "@/components/layout/DashFooter";
import DashContent from "@/components/layout/DashContent";
import DashNavi from "@/components/layout/DashNavi";

export default {
  name: "Dashboard",
  data() {
    return {
      currentStock: 'XOM', // todo de-hardcode
    }
  },
  components: { DashFooter, DashContent, DashHeader, DashNavi },
  // lifecycle hook auto-triggers data request
  // for now - default company is XOM
  // todo later on - introduce favorites / default starting stock - or maybe save last viewed?
  beforeMount() {
    // loading the first stock in session
    this.$store.dispatch('stock/getApiData');
  },
  beforeUpdate() {
    // when another stock is selected
  },
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-evenly;
  align-items: flex-start;
  gap: 20px;
  border: 1px solid black;
}

.dash-page-header {
  align-self: flex-start;
}

.dash-page-navi {
  align-self: flex-start;
  flex-grow: 1;
}

.dash-page-content {
  align-self: center;
  flex-grow: 3;
}

</style>