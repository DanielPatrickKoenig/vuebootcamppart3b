<template>
  <img v-bind:src="src" style="width:100%; height:100%;" />
</template>
<script>
export default {
  data () {
    return {
    }
  },
  props: ['src']
}
</script>
