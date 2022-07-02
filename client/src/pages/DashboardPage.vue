<template>
  <div class="flex-grid">
    <div class="col"><dash-header></dash-header></div>
  </div>
  <div class="flex-grid">
    <div class="col-navi">
      <dash-navi></dash-navi>
    </div>
    <div class="col">
      <dash-content></dash-content>
    </div>
  </div>
  <div class="flex-grid">
    <div class="col">
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

  // eslint-disable-next-line vue/no-unused-components
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
.flex-grid {
  display: flex;
  border: 1px solid white;
}
.col {
  flex: 1;
  border: 1px solid white;
}

.col-navi {
  width: 20%!important;
}

</style>