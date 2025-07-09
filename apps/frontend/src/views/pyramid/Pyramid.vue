<template>
  <div class="grid">
    <div class="col-12">
      <div class="card" style="overflow-x: auto">
        <TournamentBracket :bracketSize="32" v-model="pairs" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import TournamentBracket from "@/views/pyramid/components/TournamentBracket.vue";

// Estructura de datos para la pirámide.
// Para un bracket de 16 (8 partidas en R1), tenemos 3 partidas y 5 byes.
// Total de competidores: (3 * 2) + 5 = 11. Los 5 espacios restantes quedarán vacíos.
const pairs = ref({
  // Partidas que se juegan en la primera ronda
  round1: [
    {
      first_competitor: { name: "1", score: 3 },
      second_competitor: { name: "2", score: 1 },
    },
    {
      first_competitor: { name: "3" },
      second_competitor: { name: "4" },
    },
    {
      first_competitor: { name: "5" },
      second_competitor: { name: "6" },
    },
    {
      first_competitor: { name: "7" },
      second_competitor: { name: "8" },
    },
    {
      first_competitor: { name: "9" },
      second_competitor: { name: "10" },
    },
    {
      first_competitor: { name: "11" },
      second_competitor: { name: "12" },
    },
    {
      first_competitor: { name: "14" },
      second_competitor: { name: "15" },
    },
  ],
  // Competidores que avanzan directamente a la segunda ronda (byes)
  byes: [
    {
      first_competitor: { name: "13" },
      second_competitor: null,
    },
    // { name: "Ana" },
    // { name: "Maria" },
    // { name: "Pedro" },
    // { name: "Luis" },
    // { name: "Miguel" },
    // { name: "Miguel" },
    // { name: "Miguel" },
    // { name: "Miguel" },
    // { name: "Miguel" },
    // { name: "Javier" },
  ],
});
</script>
