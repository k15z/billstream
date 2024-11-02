<template>
  <div id="s1" />
  <Hero />
  <div id="s2" />
  <HelloWorld @explore="explore" />
  <div id="s3" />
  <Explore />
</template>

<script lang="ts" setup>
import { onMounted } from 'vue';

function explore() {
  const explore = document.getElementById("explore");
  (explore as any).scrollIntoView({ behavior: "smooth" });
}

function scrollToSection(direction: 'up' | 'down') {
  const sections = ['s1', 's2', 's3'];
  const currentSection = sections.find(id => {
    const element = document.getElementById(id);
    const rect = element?.getBoundingClientRect();
    return rect && rect.top >= 0 && rect.top <= window.innerHeight;
  });

  if (!currentSection) return;

  const currentIndex = sections.indexOf(currentSection);
  let targetIndex;

  if (direction === 'up') {
    targetIndex = Math.max(0, currentIndex - 1);
  } else {
    targetIndex = Math.min(sections.length - 1, currentIndex + 1);
  }

  const targetElement = document.getElementById(sections[targetIndex]);
  targetElement?.scrollIntoView({ behavior: 'smooth' });
}

onMounted(() => {
  window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
      scrollToSection('up');
    } else if (e.key === 'ArrowRight') {
      scrollToSection('down');
    }
  });
});

</script>
