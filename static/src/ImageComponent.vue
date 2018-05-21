<template>
  <div v-bind:style="'background-size:cover;background-position:center;background-repeat:no-repeat;background-image:url(' + src + ')'" style="width:100%; height:100%;" />
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
