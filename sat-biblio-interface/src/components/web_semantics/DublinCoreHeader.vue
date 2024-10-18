<script>

import Teleport from 'vue2-teleport';
import {DublincCore} from "@/services/objectManager";
export default {
  name: "DublinCoreHeader",
  components: {Teleport},
  props: {
      dublinCore: {
        type: DublincCore,
      }
    },
  methods: {
    isValid(value) {
      return value.length > 0;
    }
  }

}
</script>

<template>
  <Teleport to="head">
    <component :is="'link'" rel="schema.DC" href="http://purl.org/dc/elements/1.1/" />
    <component v-if="isValid(dublinCore.contributor)" :is="'meta'" name="DC.contributor" :content="dublinCore.contributor"></component>
    <component v-if="isValid(dublinCore.coverage)" :is="'meta'" name="DC.coverage" :content="dublinCore.coverage"></component>
    <component v-if="isValid(dublinCore.creator)" :is="'meta'" name="DC.creator" :content="dublinCore.creator"></component>
    <component v-if="isValid(dublinCore.date)" :is="'meta'" name="DC.date" :content="dublinCore.date"></component>
    <component v-if="isValid(dublinCore.description)" :is="'meta'" name="DC.description" :content="dublinCore.description"></component>
    <component v-if="isValid(dublinCore.format)" :is="'meta'" name="DC.format" :content="dublinCore.format"></component>
    <component v-if="isValid(dublinCore.identifier)" :is="'meta'" name="DC.identifier" :content="dublinCore.identifier"></component>
    <component v-if="isValid(dublinCore.language)" :is="'meta'" name="DC.language" :content="dublinCore.language"></component>
    <component v-if="isValid(dublinCore.publisher)" :is="'meta'" name="DC.publisher" :content="dublinCore.publisher"></component>
    <component v-if="isValid(dublinCore.relation)" :is="'meta'" name="DC.relation" :content="dublinCore.relation"></component>
    <component v-if="isValid(dublinCore.rights)" :is="'meta'" name="DC.rights" :content="dublinCore.rights"></component>
    <component v-if="isValid(dublinCore.subject)" :is="'meta'" name="DC.subject" :content="dublinCore.subject"></component>
    <component v-if="isValid(dublinCore.source)" :is="'meta'" name="DC.source" :content="dublinCore.source"></component>
    <component v-if="isValid(dublinCore.title)" :is="'meta'" name="DC.title" :content="dublinCore.title"></component>
    <component v-if="isValid(dublinCore.type)" :is="'meta'" name="DC.type" :content="dublinCore.type"></component>
  </Teleport>

</template>

<style scoped>

</style>