<template>
  <HelloWorld @explore="explore" />
  <div id="explore" />
  <Explore />
</template>

<script lang="ts" setup>
function explore() {
  const explore = document.getElementById("explore");
  (explore as any).scrollIntoView({ behavior: "smooth" });
}
</script>
