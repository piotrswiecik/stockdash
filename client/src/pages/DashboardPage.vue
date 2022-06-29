<template>
  <dash-header></dash-header>
  <dash-content></dash-content>
  <dash-footer></dash-footer>
</template>

<script>
import DashHeader from "@/components/layout/DashHeader";
import DashFooter from "@/components/layout/DashFooter";
import DashContent from "@/components/layout/DashContent";

export default {
  name: "Dashboard",
  components: { DashFooter, DashContent, DashHeader },
}
</script>

<style scoped>

</style>