<template>
  <ul class="check-one">
    <li v-for="(c, i, k) in choices" :key="k" v-bind:class="c.value" v-bind:style="c.selected ? '' : 'opacity:.5;'">
      <label style="width:100%; display:block;">
        <input type="radio" v-model="c.selected" v-bind:value="c.value" v-bind:name="rname" v-on:change="onCheckChange" />
        <span v-text="c.text">
        </span>
      </label>
    </li>
  </ul>
</template>
<script>
  import {EventBus} from './EventBus.js'
  export default {
    name: 'check-one',
    props: ['choices'],
    data () {
      return {
        rname: 'name' + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join('')
      }
    },
    methods: {
      onCheckChange: function (e) {
        EventBus.$emit('check-one-option-checked', e.currentTarget)
      }
    }
  }
</script>
<style>
</style>
