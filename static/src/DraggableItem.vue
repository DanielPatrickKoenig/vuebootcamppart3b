<template>
  <div class="sizing-handle-container">
    <div class="sizing-content" v-bind:style="'left:' + position.left.toString() + 'px; top:' + position.top.toString() + 'px; width:' + size.width + 'px; height:' + size.height + 'px;'">
      <slot name="content"></slot>
    </div>
    <div v-if="!disabled" class="sizing-handle" v-on:mousedown="onDown" v-bind:style="'left:' + position.left.toString() + 'px; top:' + position.top.toString() + 'px; width:' + size.width + 'px; height:' + size.height + 'px; background-color:' + bg + '; box-shadow: 0 0 0 1px ' + border">
    </div>
    <div class="sizing-releaser" v-on:mouseup="onUp" v-on:mousemove="onMove" v-bind:style="'z-index:' + zIndex"></div>
  </div>
</template>
<script>
import {EventBus} from './EventBus.js'
export default {
  data () {
    return {
      zIndex: this.inactivez,
      position: {
        left: this.coords.left,
        top: this.coords.top
      },
      offset: {
        x: 0,
        y: 0
      }
    }
  },
  props: ['coords', 'size', 'dragid', 'activez', 'inactivez', 'bg', 'border', 'disabled'],
  methods: {
    onDown: function (e) {
      var self = this
      e.currentTarget.parentNode.children[2].style.display = 'block'
      self.$data.zIndex = this.activez
      self.$data.offset.x = e.currentTarget.getBoundingClientRect().left - e.pageX
      self.$data.offset.y = e.currentTarget.getBoundingClientRect().top - e.pageY
      EventBus.$emit('draggable-element-down', {dragid: this.dragid, position: self.$data.position})
    },
    onUp: function (e) {
      var self = this
      e.currentTarget.parentNode.children[2].style.display = 'none'
      self.$data.zIndex = this.inactivez
      EventBus.$emit('draggable-element-up', {dragid: this.dragid, position: self.$data.position})
    },
    onMove: function (e) {
      var self = this
      self.$data.position.left = e.pageX - e.currentTarget.parentNode.getBoundingClientRect().left + self.$data.offset.x
      self.$data.position.top = e.pageY - e.currentTarget.parentNode.getBoundingClientRect().top + self.$data.offset.y
      EventBus.$emit('draggable-element-move', {dragid: this.dragid, position: self.$data.position})
    }
  },
  watch: {
    coords: function (val, oldVal) {
      var self = this
      self.$data.position = this.coords
    }
  }
}
</script>
<style lang="scss">
.sizing-handle-container{
  position: relative;
  > div{
    user-select: none;
    -moz-user-select: none;
    -khtml-user-select: none;
    -webkit-user-select: none;
    -o-user-select: none;
  }
  > div.sizing-handle{
    position: absolute;
    z-index:50;
  }
  > div.sizing-content{
    position: absolute;
    z-index:40;
  }
  > div.sizing-releaser{
    position: fixed;
    left:0;
    top: 0;
    right: 0;
    bottom: 0;
    background-color: transparent;
    display: none;
  }
}
</style>


