<template>
  <p>{{ description }}</p>
</template>

<script>
export default {
  name: "DashDescription",
  computed: {
    description() {
      return this.$store.getters['stock/currentDescription'];
    },
  },
}
</script>

<style scoped>

</style>