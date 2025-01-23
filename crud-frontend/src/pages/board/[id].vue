<template>
  <Board :project-id="id" />
</template>

<script setup>
import { useRoute } from 'vue-router'
import Board from '@/components/Board.vue'

const route = useRoute()
const id = route.params.id
</script>
